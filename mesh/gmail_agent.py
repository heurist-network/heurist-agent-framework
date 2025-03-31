import google.auth 
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import os, pickle
import datetime
from langchain_google_genai import ChatGoogleGenerativeAI 
import json
from dotenv import load_dotenv
import re
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from rich.console import Console
from rich.panel import Panel
console = Console()

load_dotenv()
GEMINI_API_KEY=os.getenv('GEMINI_API_KEY')



SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]


def get_gmail_service():
    creds=None

    #  load token if exists
    if os.path.exists("token.pickle"):
        print("Found token.pickle...")
        with open("token.pickle","rb") as token:
            creds = pickle.load(token)
        

    # authenticate if cred are invalid
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("Refreshing expired token....")
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        
        # Save credentials for future use
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    return build("gmail", "v1", credentials=creds)


# Convert datetime to Gmail API's format
def get_date_query(days=3):
    date = (datetime.datetime.now(datetime.UTC) - datetime.timedelta(days=days)).strftime("%Y/%m/%d")
    return f"after:{date}"


def clean_email_body(body):
    if not body:
        return ""
    
    # Remove leading/trailing spaces
    body = body.strip()

    # Normalize multiple spaces/newlines
    body = re.sub(r'\s+', ' ', body)
    body = re.sub(r'\n+', ' ', body).strip()

    # Remove unnecessary special characters if needed
    body = re.sub(r'[^\x20-\x7E]', '', body)  # Removes non-printable ASCII chars

    return body

# Fetch unread emails (with optional time window)
def fetch_unread_emails(service, scan_days=None):
    query = "is:unread"
    if scan_days:
        query += f" {get_date_query(scan_days)}"
    
    results = service.users().messages().list(userId="me", labelIds=["INBOX"], q=query).execute()
    messages = results.get("messages", [])
    
    email_data = []
    for msg in messages:
        msg_data = service.users().messages().get(userId="me", id=msg["id"]).execute()
        # snippet = msg_data.get("snippet", "No content")
        headers = msg_data.get("payload", {}).get("headers", [])
        subject = next((h["value"] for h in headers if h["name"] == "Subject"), "No Subject")
        sender = next((h["value"] for h in headers if h["name"] == "From"), "Unknown Sender")
        recipient = next((h["value"] for h in headers if h["name"] == "To"), "Unknown Recipient")
        snippet = clean_email_body(msg_data.get("snippet", "No content"))

        email_data.append({
            "id": msg["id"],
            "sender": sender,
            "to":recipient,
            "subject": subject,
            "body": snippet
        })

    return email_data

def clean_agent_response(response):
    if hasattr(response, "content"):  # Ensure response has content
        response_text = response.content  # Extract text
    else:
        return {"subject": "Error", "body": "Invalid AI response.", "confidence": 0}

    # Remove markdown JSON wrapper (```json ... ```a)
    try:
        cleaned_text=clean_email_body(re.sub(r"```json\s*|\s*```", "", response_text.strip()))
        return json.loads(cleaned_text)  # Convert cleaned text to dictionary
    except json.JSONDecodeError:
        return {"subject": "Error", "body": "Could not parse response.", "confidence": 0}    

def generate_ai_response(email_content):
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest", google_api_key=GEMINI_API_KEY)
    input_json = json.dumps({
        "subject": email_content["subject"],
        "sender": email_content["sender"],
        "body": email_content["body"]
    })
    prompt = f'''
        You are an AI email assistant. Analyze the following email subject and content (body of email) and understand its semantics and type and according to 
        that generate a structured response for reply of that email. Take care email may be formal or informal hence generate reply
        according to that. Also the json structure of the reply has been given. Follow that for reply: .
        Then, rate your confidence (0-100%) based on the clarity of the email you had.
        The whole email is here :
        INPUT EMAIL (JSON):
        {input_json}
        
        RESPONSE FORMAT (JSON):
        {{
            "subject": "<Generated Subject>",
            "body": "<Generated Reply>",
            "confidence": <Confidence Score (0-1)>
        }}
        Stop response here.
    '''
    # Generate response from Gemini
    try:
        response = llm.invoke(prompt)
        clean_response=clean_agent_response(response)
        return clean_response
    except:
        return {"subject": "Error", "body": "Could not generate response.", "confidence": 0}


# Send Email Reply
def send_email_reply(service, email_id, reply_text,recipient,owner):
    """
    Sends an AI-generated reply to an email.
    :param service: Gmail API service object
    :param email_id: The original email ID (to reply to)
    :param ai_response: JSON containing "subject" and "body"
    """
    subject = reply_text.get("subject", "Re: No Subject")
    body = reply_text.get("body", "No response generated.")
    message = MIMEMultipart()
    message["Subject"] = subject
    message["To"] = recipient  # Replace with actual recipient
    message["From"] = owner  # Replace with your email
    # Attach email body
    message.attach(MIMEText(body, "plain"))

    # Encode email in Base64
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode("utf-8")
    message_data={"raw":raw_message}
    # Send email using Gmail API
    try:
        service.users().messages().send(userId="me", body=message_data).execute()
        service.users().messages().modify(
            userId="me",
            id=email_id,
            body={"removeLabelIds": ["UNREAD"]}
        ).execute()
        console.print(Panel(f"✅ [bold green]Reply sent to {recipient}[/bold green]", title="Success", style="green"))
    except Exception as e:
        console.print(Panel(f"❌ [bold red]Failed to send email.[/bold red]\nError: {str(e)}", title="Error", style="red"))

def extract_email_sender(sender):
    match = re.search(r"<(.*?)>", sender)
    return match.group(1) if match else None

def main(scan_days=3):
    service=get_gmail_service()
    emails= fetch_unread_emails(service,scan_days)

    if not emails:
        print("No new emails found")
    
    for email in emails[:1]:
        print(f"Processing emails: {email}...")
        email_for_llm = {k: v for k, v in email.items() if k != "id"}

        ai_response = generate_ai_response(email)
        recipient=extract_email_sender(email["sender"])
        send_email_reply(service,email["id"],ai_response,recipient,email['to'])

        # print(ai_response)
        



if __name__=="__main__":
    main()    













'''
How to use it 
Gmail Agent for you : InboxGenie

## Setting up the Environment for gmail service
    Go to console.cloud.googe.com
    Create a new google cloud project
    Create a client OAuth2.0 for desktop app
    Change the data access settings according to the email you want to give access to it.

## Setting up the GEMINI API KEY from
    Go to https://aistudio.google.com/ and create a new API Key.
    Copy the API Key secret and paste it into .env (replace current example.env with .env and paste there with given variable name in example.env)
    Have given example of it in the example.env file.

    Just make sure to download  the requirements from the above imports. 

## Running the agent
    Here is agent.py file:
    Run python agent.py
    Changing configuration
    Inside the agent.py in main there is parameter of scan_days which is for scanning the emails based on days. (Kind of it is window size for emails to be scanned.)
    Tweak it according to your need.
    What this agent will do ?
    It will reply to that email and give confidence ratio with which llm has given response to the email.
    After replying to the email, it will automatically mark the message unread.
    I am thinking of adding more functionalities to it.
    If you have any suggestion you can comment it, I will integrate it.

'''
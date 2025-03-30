import json
import asyncio
import requests
from mesh.duckduckgo_search_agent import DuckDuckGoSearchAgent

API_KEY = "IITM-hackday"
# BASE_URL = "https://llm-gateway.heurist.xyz/v1/chat/completions"
BASE_URL = "https://3.84.183.11/v1/chat/completions"



def query_heurist_llm(prompt, model="meta-llama/llama-3.3-70b-instruct", temperature=0.7, max_tokens=1024):
    """Query the specified LLM for an answer."""
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": temperature,
        "stream": False,
        "max_tokens": max_tokens
    }
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    print("Payload :",payload)
    # response = requests.post(BASE_URL, json=payload, headers=headers)
    response = requests.request("POST", BASE_URL, json=payload, headers=headers,verify=False)

    if response.status_code == 200:
        return response.json().get("choices", [{}])[0].get("message", {}).get("content", "No response")
    else:
        return f"Error: {response.status_code}, {response.text}"


async def search_duckduckgo(query, max_results=3):
    """Fetch search results using Heurist's DuckDuckGoSearchAgent."""
    agent = DuckDuckGoSearchAgent()
    response = await agent.search_web(query, max_results=max_results)
    
    if response.get("status") == "success":
        return response["data"].get("results", [])
    return [{"title": "No results", "link": "", "snippet": "No relevant information found."}]


def query_deepseek_llm(question, llm_answer, duckduckgo_results):
    """Use DeepSeek LLM to compare the answer with DuckDuckGo search results."""
    comparison_prompt = f"""
    The LLM answered: "{llm_answer}"
    DuckDuckGo search results provided the following snippets:
    {json.dumps(duckduckgo_results, indent=2)}

    Based on these, classify the LLM's response as one of the following:
    - "Correct" if it matches DuckDuckGo results
    - "Uncertain" if there's partial confirmation
    - "Hallucinated" if it's not supported at all
    Provide only the classification as output.
    """
    
    return query_heurist_llm(comparison_prompt, model="deepseek/deepseek-r1")


async def main():
    """Main execution function for the LLM verification agent."""
    question = "Wht is the capital of india?"  # Example question
    llm_answer = query_heurist_llm(question)
    print("LLM Answer:", llm_answer)
    
    duckduckgo_results = await search_duckduckgo(question)
    print("DuckDuckGo Results:", json.dumps(duckduckgo_results, indent=2))
    
    deepseek_verification = query_deepseek_llm(question, llm_answer, duckduckgo_results)
    print("DeepSeek Comparison:", deepseek_verification)


if __name__ == "__main__":
    asyncio.run(main())
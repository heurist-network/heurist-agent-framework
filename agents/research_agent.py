import asyncio
import json
import os
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional, TypedDict

import dotenv

from core.clients.search_client import SearchClient
from core.llm import call_llm
from core.utils.text_splitter import trim_prompt

os.environ.clear()
dotenv.load_dotenv(override=True)

HEURIST_BASE_URL = os.getenv("HEURIST_BASE_URL")
HEURIST_API_KEY = os.getenv("HEURIST_API_KEY")
LARGE_MODEL_ID = os.getenv("LARGE_MODEL_ID")
LARGER_MODEL_ID = os.getenv("LARGER_MODEL_ID", "mistralai/mixtral-8x22b-instruct")
SMALL_MODEL_ID = os.getenv("SMALL_MODEL_ID")


def system_prompt() -> str:
    """Creates the system prompt with current timestamp."""
    now = datetime.now().isoformat()
    return f"""You are an expert researcher. Today is {now}. Follow these instructions when responding:
    - You may be asked to research subjects that is after your knowledge cutoff, assume the user is right when presented with news.
    - The user is a highly experienced analyst, no need to simplify it, be as detailed as possible and make sure your response is correct.
    - Be highly organized.
    - Suggest solutions that I didn't think about.
    - Be proactive and anticipate my needs.
    - Treat me as an expert in all subject matter.
    - Mistakes erode my trust, so be accurate and thorough.
    - Provide detailed explanations, I'm comfortable with lots of detail.
    - Value good arguments over authorities, the source is irrelevant.
    - Consider new technologies and contrarian ideas, not just the conventional wisdom.
    - You may use high levels of speculation or prediction, just flag it for me.
    IMPORTANT: MAKE SURE YOU RETURN THE JSON ONLY, NO OTHER TEXT OR MARKUP AND A VALID JSON.
    DONT ADD ANY COMMENTS OR MARKUP TO THE JSON. Example NO # or /* */ or /* */ or // or any other comments or markup.
    MAKE SURE YOU RETURN THE JSON ONLY, JSON SHOULD BE PERFECTLY FORMATTED. ALL KEYS SHOULD BE OPENED AND CLOSED.
    """


class SearchResponse(TypedDict):
    data: List[Dict[str, str]]


class ResearchResult(TypedDict):
    learnings: List[str]
    visited_urls: List[str]


@dataclass
class SerpQuery:
    query: str
    research_goal: str


async def generate_feedback(query: str) -> List[str]:
    """Generates follow-up questions to clarify research direction."""
    prompt = f"Given this research topic: {query}, generate 3-5 follow-up questions to better understand the user's research needs. Return the response as a JSON object with a 'questions' array field."
    response = call_llm(
        base_url=HEURIST_BASE_URL,
        api_key=HEURIST_API_KEY,
        model_id=LARGER_MODEL_ID,
        system_prompt=system_prompt(),
        user_prompt=prompt,
    )

    if not response:
        return "Sorry, I couldn't process your message.", None

    else:  # Add null check
        try:
            result = response["content"].replace("```json", "").replace("```", "").strip()
            result = json.loads(result)
            questions = result.get("questions", [])
            return questions
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON response: {e}")
            print(f"Raw response: {response}")
            return []


# Initialize SearchClient
search_client = SearchClient(client_type="firecrawl", api_key=os.environ.get("FIRECRAWL_KEY", ""), rate_limit=1)


async def generate_serp_queries(
    query: str, num_queries: int = 3, learnings: Optional[List[str]] = None
) -> List[SerpQuery]:
    """Generate SERP queries based on user input and previous learnings."""

    prompt = f"""Given the following prompt from the user, generate a list of SERP queries to research the topic. Return a JSON object with a 'queries' array field containing {num_queries} queries (or less if the original prompt is clear). Each query object should have 'query' and 'research_goal' fields. Make sure each query is unique and not similar to each other: <prompt>{query}</prompt>"""

    example_response = """\n
    IMPORTANT: MAKE SURE YOU FOLLOW THE EXAMPLE RESPONSE FORMAT AND ONLY THAT FORMAT WITH THE CORRECT QUERY AND RESEARCH GOAL.
    {
        "queries": [
            {
                "query": "QUERY 1",
                "research_goal": "RESEARCH GOAL 1"
            },
            {
                "query": "QUERY 2",
                "research_goal": "RESEARCH GOAL 2"
            },
            {
                "query": "QUERY 3",
                "research_goal": "RESEARCH GOAL 3"
            }
        ]
    }
    """
    prompt += example_response
    if learnings:
        prompt += f"\n\nHere are some learnings from previous research, use them to generate more specific queries: {' '.join(learnings)}"

    response = call_llm(
        base_url=HEURIST_BASE_URL,
        api_key=HEURIST_API_KEY,
        model_id=LARGER_MODEL_ID,
        system_prompt=system_prompt(),
        user_prompt=prompt,
        temperature=0.1,
    )

    if not response:
        return "Sorry, I couldn't process your message.", None

    else:
        try:
            result = response["content"].replace("```json", "").replace("```", "").strip()
            result = json.loads(result)
            queries = result.get("queries", [])
            return [SerpQuery(**q) for q in queries][:num_queries]
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON response: {e}")
            print(f"Raw response: {response}")
            return []


async def process_serp_result(
    query: str,
    search_result: SearchResponse,
    num_learnings: int = 3,
    num_follow_up_questions: int = 3,
) -> Dict[str, List[str]]:
    """Process search results to extract learnings and follow-up questions."""
    contents = [trim_prompt(item.get("markdown", ""), 25_000) for item in search_result["data"] if item.get("markdown")]

    contents_str = "".join(f"<content>\n{content}\n</content>" for content in contents)

    prompt = (
        f"Given the following contents from a SERP search for the query <query>{query}</query>, "
        f"generate a list of learnings from the contents. Return a JSON object with 'learnings' "
        f"and 'followUpQuestions' arrays. Include up to {num_learnings} learnings and "
        f"{num_follow_up_questions} follow-up questions. The learnings should be unique, "
        "concise, and information-dense, including entities, metrics, numbers, and dates.\n\n"
        f"IMPORTANT: MAKE SURE THE INFORMATION YOU USE IS FROM CONTENT AND NOT OTHER SOURCES. MAKE SURE IT IS ACTUALLY RELEVANT TO THE QUERY."
        f"IMPORTANT: DON'T MAKE ANY INFORMATION UP, IT MUST BE FROM THE CONTENT. ONLY USE THE CONTENT TO GENERATE THE LEARNINGS AND FOLLOW UP QUESTIONS."
        f"<contents>{contents_str}</contents>"
    )
    example_response = """\n
    IMPORTANT: MAKE SURE YOU FOLLOW THE EXAMPLE RESPONSE FORMAT AND ONLY THAT FORMAT WITH THE CORRECT LEARNINGS AND FOLLOW UP QUESTIONS.
    {
        "learnings": [
            "LEARNING 1",
            "LEARNING 2",
            "LEARNING 3"
        ],
        "followUpQuestions": [
            "FOLLOW UP QUESTION 1",
            "FOLLOW UP QUESTION 2",
            "FOLLOW UP QUESTION 3"
        ]
    }
    """
    prompt += example_response
    response = call_llm(
        base_url=HEURIST_BASE_URL,
        api_key=HEURIST_API_KEY,
        model_id=LARGE_MODEL_ID,
        system_prompt=system_prompt(),
        user_prompt=prompt,
        temperature=0.1,
    )

    if not response:
        return "Sorry, I couldn't process your message.", None

    else:
        try:
            result = response["content"].replace("```json", "").replace("```", "").strip()
            result = json.loads(result)

            return {
                "learnings": result.get("learnings", [])[:num_learnings],
                "followUpQuestions": result.get("followUpQuestions", [])[:num_follow_up_questions],
            }
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON response: {e}")
            print(f"Raw response: {response}")
            return {"learnings": [], "followUpQuestions": []}


async def write_final_report(prompt: str, learnings: List[str], visited_urls: List[str]) -> str:
    """Generate final report based on all research learnings."""

    print("learnings: ", learnings)
    learnings_string = trim_prompt(
        "\n".join([f"<learning>\n{learning}\n</learning>" for learning in learnings]),
        150_000,
    )

    user_prompt = (
        f"Given the following prompt from the user, write a final report on the topic using "
        f"the learnings from research. Return a JSON object with a 'reportMarkdown' field "
        f"containing a detailed markdown report (aim for 3+ pages). Include ALL the learnings "
        f"from research:\n\n<prompt>{prompt}</prompt>\n\n"
        f"Here are all the learnings from research:\n\n<learnings>\n{learnings_string}\n</learnings>"
    )

    response = call_llm(
        base_url=HEURIST_BASE_URL,
        api_key=HEURIST_API_KEY,
        model_id=LARGER_MODEL_ID,
        system_prompt=system_prompt(),
        user_prompt=user_prompt,
        temperature=0.1,
    )

    if not response:
        return "Sorry, I couldn't process your message.", None

    else:
        try:
            result = response["content"].replace("```json", "").replace("```", "").strip()
            result = json.loads(result)
            report = result.get("reportMarkdown", "")

            # Append sources
            urls_section = "\n\n## Sources\n\n" + "\n".join([f"- {url}" for url in visited_urls])
            return report + urls_section
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON response: {e}")
            print(f"Raw response: {response}")
            return "Error generating report"


async def deep_research(
    query: str,
    breadth: int,
    depth: int,
    concurrency: int,
    learnings: List[str] = None,
    visited_urls: List[str] = None,
) -> ResearchResult:
    """
    Main research function that recursively explores a topic.

    Args:
        query: Research query/topic
        breadth: Number of parallel searches to perform
        depth: How many levels deep to research
        learnings: Previous learnings to build upon
        visited_urls: Previously visited URLs
    """
    learnings = learnings or []
    visited_urls = visited_urls or []

    # Generate search queries
    serp_queries = await generate_serp_queries(query=query, num_queries=breadth, learnings=learnings)

    # Create a semaphore to limit concurrent requests
    semaphore = asyncio.Semaphore(concurrency)

    async def process_query(serp_query: SerpQuery) -> ResearchResult:
        async with semaphore:
            try:
                # Search for content
                result = await search_client.search(serp_query.query, timeout=15000)

                # Collect new URLs
                new_urls = [item.get("url") for item in result["data"] if item.get("url")]

                # Calculate new breadth and depth for next iteration
                new_breadth = max(1, breadth // 2)
                new_depth = depth - 1

                new_learnings = await process_serp_result(
                    query=serp_query.query,
                    search_result=result,
                    num_follow_up_questions=new_breadth,
                )

                all_learnings = learnings + new_learnings["learnings"]
                all_urls = visited_urls + new_urls

                # If we have more depth to go, continue research
                if new_depth > 0:
                    print(f"Researching deeper, breadth: {new_breadth}, depth: {new_depth}")

                    next_query = f"""
                    Previous research goal: {serp_query.research_goal}
                    Follow-up research directions: {" ".join(new_learnings["followUpQuestions"])}
                    """.strip()

                    return await deep_research(
                        query=next_query,
                        breadth=new_breadth,
                        depth=new_depth,
                        concurrency=concurrency,
                        learnings=all_learnings,
                        visited_urls=all_urls,
                    )

                return {"learnings": all_learnings, "visited_urls": all_urls}

            except Exception as e:
                if "Timeout" in str(e):
                    print(f"Timeout error running query: {serp_query.query}: {e}")
                else:
                    print(f"Error running query: {serp_query.query}: {e}")
                return {"learnings": [], "visited_urls": []}

    # Process all queries concurrently
    results = await asyncio.gather(*[process_query(query) for query in serp_queries])

    # Combine all results
    all_learnings = list(set(learning for result in results for learning in result["learnings"]))

    all_urls = list(set(url for result in results for url in result["visited_urls"]))

    return {"learnings": all_learnings, "visited_urls": all_urls}

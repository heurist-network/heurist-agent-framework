import asyncio
import json
import logging
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple, TypedDict

from core.utils.text_splitter import trim_prompt

logger = logging.getLogger(__name__)


@dataclass
class ResearchQuery:
    query: str
    research_goal: str


class ResearchResult(TypedDict):
    learnings: List[str]
    visited_urls: List[str]
    follow_up_questions: List[str]
    analyses: List[Dict]


class ResearchWorkflow:
    """Research workflow combining interactive and autonomous research patterns with advanced analysis"""

    def __init__(self, llm_provider, tool_manager, firecrawl_client):
        self.llm_provider = llm_provider
        self.tool_manager = tool_manager
        self.firecrawl = firecrawl_client
        self._last_request_time = 0

    async def process(
        self, message: str, personality_provider=None, chat_id: str = None, workflow_options: Dict = None, **kwargs
    ) -> Tuple[Optional[str], Optional[str], Optional[Dict]]:
        """Main research workflow processor with enhanced depth and analysis"""

        # Set default options
        options = {
            "interactive": False,  # Whether to ask clarifying questions first
            "breadth": 3,  # Number of parallel searches
            "depth": 2,  # How deep to go in research
            "concurrency": 3,  # Max concurrent requests
            "temperature": 0.7,
            "raw_data_only": False,  # Whether to return only raw data without report
        }

        if workflow_options:
            options.update(workflow_options)

        try:
            if options["interactive"]:
                # Interactive research flow with clarifying questions
                questions = await self._generate_questions(message)
                # Here we'd typically wait for user response, but for now we'll proceed
                enhanced_query = f"{message}\nConsidering questions: {', '.join(questions)}"
            else:
                enhanced_query = message

            # Conduct deep research
            research_result = await self._deep_research(
                query=enhanced_query,
                breadth=options["breadth"],
                depth=options["depth"],
                concurrency=options["concurrency"],
            )

            if options["raw_data_only"]:
                return None, None, research_result

            # Generate final report
            report = await self._generate_report(
                original_query=message, research_result=research_result, personality_provider=personality_provider
            )

            return report, None, research_result

        except Exception as e:
            logger.error(f"Research workflow failed: {str(e)}")
            return f"Research failed: {str(e)}", None, None

    async def _generate_questions(self, query: str) -> List[str]:
        """Generate clarifying questions for research"""
        prompt = f"""Given this research topic: {query}, generate 3-5 follow-up questions to better understand the research needs.
        Return ONLY a JSON array of strings containing the questions."""

        response, _, _ = await self.llm_provider.call(
            system_prompt=self._get_system_prompt(), user_prompt=prompt, temperature=0.7
        )

        try:
            cleaned_response = response.replace("```json", "").replace("```", "").strip()
            questions = json.loads(cleaned_response)
            return questions if isinstance(questions, list) else []
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing questions JSON: {e}")
            return []

    async def _generate_search_queries(
        self, query: str, num_queries: int = 3, learnings: List[str] = None
    ) -> List[ResearchQuery]:
        """Generate intelligent search queries based on input topic and previous learnings"""
        learnings_text = "\n".join([f"- {learning}" for learning in learnings]) if learnings else ""

        prompt = f"""Given the following prompt from the user, generate a list of SERP queries to research the topic.
        Return a JSON object with a 'queries' array field containing {num_queries} queries (or less if the original prompt is clear).
        Each query object should have 'query' and 'research_goal' fields.
        Make sure each query is unique and not similar to each other:

        <prompt>{query}</prompt>

        {f"Previous learnings to consider:\n{learnings_text}" if learnings_text else ""}
        """
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
        response, _, _ = await self.llm_provider.call(
            system_prompt=self._get_system_prompt(), user_prompt=prompt, temperature=0.3
        )
        try:
            cleaned_response = response.replace("```json", "").replace("```", "").strip()
            result = json.loads(cleaned_response)
            queries = result.get("queries", [])
            return [ResearchQuery(**q) for q in queries][:num_queries]
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing query JSON: {e}")
            logger.debug(f"Raw response: {response}")
            return [ResearchQuery(query=query, research_goal="Main topic research")]

    async def _process_search_result(
        self, query: str, search_result: Dict, num_learnings: int = 5, num_follow_up_questions: int = 3
    ) -> Dict:
        """Process search results to extract learnings and follow-up questions with enhanced validation"""
        contents = [
            trim_prompt(item.get("markdown", ""), 25000)
            for item in search_result.get("data", [])
            if item.get("markdown")
        ]

        if not contents:
            return {"learnings": [], "follow_up_questions": [], "analysis": "No search results found to analyze."}

        contents_str = "".join(f"<content>\n{content}\n</content>" for content in contents)

        prompt = f"""Analyze these search results for the query: <query>{query}</query>

        <contents>{contents_str}</contents>

        Provide a detailed analysis including key findings, main themes, and recommendations for further research.
        Return as JSON with 'analysis', 'learnings', and 'follow_up_questions' fields.

        IMPORTANT: MAKE SURE YOU RETURN THE JSON ONLY, NO OTHER TEXT OR MARKUP AND A VALID JSON.
        DONT ADD ANY COMMENTS OR MARKUP TO THE JSON. Example NO # or /* */ or /* */ or // or ``` or JSON or any other comments or markup.
        MAKE SURE YOU RETURN THE JSON ONLY, JSON SHOULD BE PERFECTLY FORMATTED. ALL KEYS SHOULD BE OPENED AND CLOSED.
        USE THE FOLLOWING FORMAT FOR THE JSON:
        {{
            "analysis": "Analysis of the search results",
            "learnings": ["Learning 1", "Learning 2", "Learning 3", "Learning 4", "Learning 5"],
            "follow_up_questions": ["Question 1", "Question 2", "Question 3"]
        }}

        The learnings should be unique, concise, and information-dense, including entities, metrics, numbers, and dates.
        IMPORTANT: DON'T MAKE ANY INFORMATION UP, IT MUST BE FROM THE CONTENT. ONLY USE THE CONTENT TO GENERATE THE LEARNINGS AND FOLLOW UP QUESTIONS.
        """

        response, _, _ = await self.llm_provider.call(
            system_prompt=self._get_system_prompt(), user_prompt=prompt, temperature=0.3
        )

        try:
            cleaned_response = response.replace("```json", "").replace("```", "").strip()
            result = json.loads(cleaned_response)
            return {
                "learnings": result.get("learnings", [])[:num_learnings],
                "follow_up_questions": result.get("follow_up_questions", [])[:num_follow_up_questions],
                "analysis": result.get("analysis", "No analysis provided."),
            }
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing search result JSON: {e}")
            logger.debug(f"Raw response: {response}")
            return {"learnings": [], "follow_up_questions": [], "analysis": "Error processing search results."}

    async def _deep_research(
        self,
        query: str,
        breadth: int,
        depth: int,
        concurrency: int,
        learnings: List[str] = None,
        visited_urls: List[str] = None,
        analyses: List[Dict] = None,
    ) -> ResearchResult:
        """Conduct deep research using Firecrawl with improved handling and rate limiting"""

        learnings = learnings or []
        visited_urls = visited_urls or []
        analyses = analyses or []

        # Generate search queries using previous learnings
        search_queries = await self._generate_search_queries(query=query, num_queries=breadth, learnings=learnings)

        # Create semaphore for concurrent requests
        semaphore = asyncio.Semaphore(concurrency)

        async def process_query(research_query: ResearchQuery) -> Dict:
            async with semaphore:
                try:
                    # Add rate limiting
                    current_time = asyncio.get_event_loop().time()
                    time_since_last = current_time - self._last_request_time
                    if time_since_last < 3:  # Rate limit to prevent overloading
                        await asyncio.sleep(3 - time_since_last)
                    self._last_request_time = current_time

                    # Search using Firecrawl with timeouts and retries
                    for attempt in range(3):
                        try:
                            result = await self.firecrawl.search(research_query.query, timeout=20000, limit=5)
                            break
                        except Exception as e:
                            if attempt == 2:  # Last attempt
                                raise
                            logger.warning(f"Search attempt {attempt + 1} failed: {str(e)}")
                            await asyncio.sleep(2)  # Wait before retrying

                    # Extract URLs
                    urls = [item.get("url") for item in result.get("data", []) if item.get("url")]

                    # Process content to extract learnings
                    processed_result = await self._process_search_result(
                        query=research_query.query, search_result=result
                    )

                    new_breadth = max(1, breadth // 2)
                    new_depth = depth - 1

                    # If we have depth remaining and follow-up questions, explore deeper
                    if new_depth > 0 and processed_result["follow_up_questions"]:
                        next_query = "\n".join(
                            [
                                f"Previous research goal: {research_query.research_goal}",
                                "Follow-up questions to explore:",
                                "\n".join(f"- {q}" for q in processed_result["follow_up_questions"][:new_breadth]),
                            ]
                        )

                        deeper_results = await self._deep_research(
                            query=next_query,
                            breadth=new_breadth,
                            depth=new_depth,
                            concurrency=concurrency,
                            learnings=learnings + processed_result["learnings"],
                            visited_urls=visited_urls + urls,
                            analyses=analyses
                            + [{"query": research_query.query, "analysis": processed_result["analysis"]}],
                        )

                        return {
                            "learnings": deeper_results["learnings"],
                            "urls": deeper_results["visited_urls"],
                            "follow_up_questions": deeper_results["follow_up_questions"],
                            "analyses": deeper_results["analyses"],
                        }

                    return {
                        "learnings": processed_result["learnings"],
                        "urls": urls,
                        "follow_up_questions": processed_result["follow_up_questions"],
                        "analyses": [{"query": research_query.query, "analysis": processed_result["analysis"]}],
                    }

                except Exception as e:
                    logger.error(f"Error processing query {research_query.query}: {str(e)}")
                    return {"learnings": [], "urls": [], "follow_up_questions": [], "analyses": []}

        # Process all queries concurrently
        results = await asyncio.gather(*[process_query(q) for q in search_queries])

        # Combine results and remove duplicates
        all_learnings = learnings.copy()
        for result in results:
            all_learnings.extend(result.get("learnings", []))
        all_learnings = list(dict.fromkeys(all_learnings))

        all_urls = visited_urls.copy()
        for result in results:
            all_urls.extend(result.get("urls", []))
        all_urls = list(dict.fromkeys(all_urls))

        all_questions = []
        for result in results:
            all_questions.extend(result.get("follow_up_questions", []))

        all_analyses = analyses.copy()
        for result in results:
            all_analyses.extend(result.get("analyses", []))

        return {
            "learnings": all_learnings,
            "visited_urls": all_urls,
            "follow_up_questions": all_questions,
            "analyses": all_analyses,
        }

    async def _generate_report(
        self, original_query: str, research_result: ResearchResult, personality_provider=None
    ) -> str:
        """Generate detailed research report with source analysis"""
        learnings_str = "\n".join([f"- {learning}" for learning in research_result["learnings"]])

        # Format analyses as a JSON string for the prompt
        analyses_str = json.dumps(
            [
                {"query": analysis.get("query", ""), "analysis": analysis.get("analysis", "")}
                for analysis in research_result.get("analyses", [])
            ],
            indent=2,
        )

        system_prompt = self._get_report_system_prompt()

        prompt = f"""
        Given the following prompt from the user, write a final report on the topic using
        the learnings from research. Return a JSON object with a 'reportMarkdown' field
        containing a detailed markdown report (aim for 3+ pages). Include ALL the learnings
        from research:
        <prompt>
        {original_query}
        </prompt>

        Here are all the learnings from research:
        <learnings>
        {learnings_str}
        </learnings>

        Here are all the analyses from research:
        <analyses>
        {analyses_str}
        </analyses>

        Create a detailed markdown report that includes:
        1. Executive Summary
        2. Key Findings and Insights
        3. Detailed Analysis by Theme
        4. Gaps and Areas for Further Research
        5. Recommendations
        6. Source Analysis and Credibility Assessment

        IMPORTANT: MAKE SURE YOU RETURN THE JSON ONLY, NO OTHER TEXT OR MARKUP AND A VALID JSON.
        IMPORTANT: DONT ADD ANY COMMENTS OR MARKUP TO THE JSON. Example NO # or /* */ or /* */ or // or ``` or JSON or json or any other comments or markup.
        IMPORTANT: MAKE SURE YOU RETURN THE JSON ONLY, JSON SHOULD BE PERFECTLY FORMATTED. ALL KEYS SHOULD BE OPENED AND CLOSED.
        """

        response, _, _ = await self.llm_provider.call(system_prompt=system_prompt, user_prompt=prompt, temperature=0.3)

        try:
            cleaned_response = response.replace("```json", "").replace("```", "").strip()
            result = json.loads(cleaned_response)
            report = result.get("reportMarkdown", "Error generating report")

            # Add sources section
            sources = "\n\n## Sources\n\n" + "\n".join([f"- {url}" for url in research_result["visited_urls"]])

            return report + sources
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing report JSON: {e}")
            logger.debug(f"Raw response: {response}")

            # Fallback report generation
            return (
                f"# Research Report: {original_query}\n\n"
                + "## Key Findings\n\n"
                + "\n".join([f"- {learning}" for learning in research_result["learnings"]])
                + "\n\n## Sources\n\n"
                + "\n".join([f"- {url}" for url in research_result["visited_urls"]])
            )

    def _get_system_prompt(self) -> str:
        """Get the system prompt for research operations"""
        return """You are an expert research analyst that processes web search results.
        Analyze the content and provide insights about:
        1. Key findings and main themes
        2. Source credibility and diversity
        3. Information completeness and gaps
        4. Emerging patterns and trends
        5. Potential biases or conflicting information

        Be thorough and detailed in your analysis. Focus on extracting concrete facts,
        statistics, and verifiable information. Highlight any uncertainties or areas
        needing further research.

        Return your analysis in a clear, structured format with sections for key findings,
        detailed analysis, and recommendations for further research.

        IMPORTANT: DON'T MAKE ANY INFORMATION UP, IT MUST BE FROM THE CONTENT PROVIDED.
        FOLLOW THE REQUESTED JSON FORMAT EXACTLY WITH NO ADDITIONAL MARKUP OR COMMENTS."""

    def _get_report_system_prompt(self) -> str:
        """Get the system prompt specifically for report generation"""
        return """You are an expert researcher preparing comprehensive research reports.
        Follow these instructions when responding:
        - You may be asked to research subjects that is after your knowledge cutoff, assume the user is right when presented with news.
        - The user is a highly experienced analyst, no need to simplify it, be as detailed as possible and make sure your response is correct.
        - Be highly organized with clear headings and structure.
        - Suggest solutions that I didn't think about.
        - Be proactive and anticipate my needs.
        - Provide detailed explanations with supporting evidence.
        - Value good arguments over authorities, the source is irrelevant.
        - Consider new technologies and contrarian ideas, not just the conventional wisdom.
        - You may use high levels of speculation or prediction, just flag it for me.

        IMPORTANT: MAKE SURE YOU RETURN THE JSON ONLY, NO OTHER TEXT OR MARKUP AND A VALID JSON.
        DONT ADD ANY COMMENTS OR MARKUP TO THE JSON. Example NO # or /* */ or /* */ or // or any other comments or markup.
        MAKE SURE YOU RETURN THE JSON ONLY, JSON SHOULD BE PERFECTLY FORMATTED. ALL KEYS SHOULD BE OPENED AND CLOSED."""

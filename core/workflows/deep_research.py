import asyncio
import json
import logging
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional, Tuple, TypedDict

from ..utils.text_splitter import trim_prompt

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

    def __init__(self, llm_provider, tool_manager, search_client=None, search_clients=None):
        """
        Initialize the research workflow with LLM provider and search capabilities.

        Args:
            llm_provider: Provider for language model operations
            tool_manager: Manager for various tools
            search_client: A single search client (for backward compatibility)
            search_clients: Dictionary of search clients with provider names as keys
                            Example:
                            {
                                "exa": ExaClient(api_key="..."),
                                "firecrawl": FirecrawlClient(api_key="..."),
                                "duckduckgo": DuckDuckGoClient()
                            }
        """
        self.llm_provider = llm_provider
        self.tool_manager = tool_manager

        # Initialize search clients dictionary
        self.search_clients = {}

        # Handle single client (backward compatibility)
        if search_client:
            self.search_clients["default"] = search_client
            # Configure rate limit for the default client
            if hasattr(search_client, "update_rate_limit"):
                search_client.update_rate_limit(0)

        # Handle multiple clients
        if search_clients and isinstance(search_clients, dict):
            for provider, client in search_clients.items():
                self.search_clients[provider] = client
                # Configure rate limit for each client
                if hasattr(client, "update_rate_limit"):
                    client.update_rate_limit(0)

        # Make sure we have at least one search client
        if not self.search_clients:
            raise ValueError("At least one search client must be provided")

        # For convenience, set search_client to the default client
        self.search_client = self.search_clients.get("default", next(iter(self.search_clients.values())))

        self._last_request_time = 0
        self.analysis_model = getattr(self.llm_provider, "small_model_id", None)
        self.report_model = getattr(self.llm_provider, "large_model_id", None)

    async def process(
        self, message: str, personality_provider=None, chat_id: str = None, workflow_options: Dict = None, **kwargs
    ) -> Tuple[Optional[str], Optional[str], Optional[Dict]]:
        """Main research workflow processor with enhanced depth and analysis"""
        start_time = datetime.now()
        print("--------------------------------")
        print(f"Starting deep research for query: {message} at time {start_time}")
        print("--------------------------------")
        # Set default options
        options = {
            "interactive": False,  # Whether to ask clarifying questions first
            "breadth": 3,  # Number of parallel searches
            "depth": 2,  # How deep to go in research
            "concurrency": 3,  # Max concurrent requests
            "temperature": 0.7,
            "raw_data_only": False,  # Whether to return only raw data without report
            "analysis_model": self.analysis_model,  # Model to use for intermediate reasoning
            "report_model": self.report_model,  # Model to use for report generation
            "multi_provider": len(self.search_clients) > 1,  # Auto-enable when multiple clients are available
            "search_providers": [],  # List of search provider names to use (if multi_provider is True)
        }

        if workflow_options:
            options.update(workflow_options)
            # Update self.report_model if provided in options
            self.analysis_model = workflow_options.get("analysis_model", self.analysis_model)
            self.report_model = workflow_options.get("report_model", self.report_model)

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
                multi_provider=options.get("multi_provider", False),
                search_providers=options.get("search_providers", []),
            )

            if options["raw_data_only"]:
                return None, None, research_result

            # Generate final report
            report = await self._generate_report(
                original_query=message, research_result=research_result, personality_provider=personality_provider
            )

            end_time = datetime.now()
            print("--------------------------------")
            print(f"Deep research completed for query: {message} at time {end_time}")
            print(f"Total time taken: {end_time - start_time}")
            print("--------------------------------")

            return report, None, research_result

        except Exception as e:
            logger.error(f"Research workflow failed: {str(e)}")
            return f"Research failed: {str(e)}", None, None

    async def _generate_questions(self, query: str) -> List[str]:
        """Generate clarifying questions for research"""
        prompt = f"""Given this research topic: {query}, generate 3-5 follow-up questions to better understand the research needs.
        Return ONLY a JSON array of strings containing the questions."""

        response, _, _ = await self.llm_provider.call(
            system_prompt=self._get_system_prompt(),
            user_prompt=prompt,
            temperature=0.7,
            model_id=self.analysis_model,
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

        {f"Previous learnings to consider:{chr(10)}{learnings_text}" if learnings_text else ""}
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
        model_for_queries = self.analysis_model or self.report_model
        response, _, _ = await self.llm_provider.call(
            system_prompt=self._get_system_prompt(),
            user_prompt=prompt,
            temperature=0.3,
            model_id=model_for_queries,
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
        # Extract data - works for both Pydantic models and dicts
        data = getattr(search_result, "data", None) or (
            search_result.get("data") if isinstance(search_result, dict) else []
        )

        contents = []
        for item in data:
            # Extract markdown - works for both Pydantic models and dicts
            markdown = getattr(item, "markdown", None) or (item.get("markdown") if isinstance(item, dict) else None)
            if markdown:
                contents.append(trim_prompt(markdown, 25000))

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
            system_prompt=self._get_system_prompt(),
            user_prompt=prompt,
            temperature=0.3,
            model_id=self.analysis_model,
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
        multi_provider: bool,
        search_providers: List[str],
        learnings: List[str] = None,
        visited_urls: List[str] = None,
        analyses: List[Dict] = None,
    ) -> ResearchResult:
        """Conduct deep research using SearchClient with improved handling and parallelization"""

        logger.info(
            f"Starting deep research with query: {query}, depth: {depth}, breadth: {breadth}, concurrency: {concurrency}"
        )

        learnings = learnings or []
        visited_urls = visited_urls or []
        analyses = analyses or []

        # Generate search queries using previous learnings
        search_queries = await self._generate_search_queries(query=query, num_queries=breadth, learnings=learnings)

        # Create semaphore for concurrent requests
        semaphore = asyncio.Semaphore(concurrency)

        # Decide which search clients to use
        active_search_clients = {}

        # If multi_provider is enabled and specific providers are requested, filter them
        if multi_provider and search_providers:
            for provider in search_providers:
                if provider in self.search_clients:
                    active_search_clients[provider] = self.search_clients[provider]

        # If no specific providers were requested or found, use all available clients
        if not active_search_clients:
            active_search_clients = self.search_clients

        # Single provider simplification - if only one provider, just use that
        if len(active_search_clients) == 1:
            provider = next(iter(active_search_clients.keys()))
            search_client = active_search_clients[provider]

            async def process_query(research_query: ResearchQuery) -> Dict:
                async with semaphore:
                    try:
                        # Search using SearchClient with timeouts and retries
                        for attempt in range(3):
                            try:
                                print(f"Searching with {provider} for {research_query.query}")
                                result = await search_client.search(research_query.query, timeout=20000)
                                break
                            except Exception as e:
                                if attempt == 2:  # Last attempt
                                    raise
                                logger.warning(f"Search attempt {attempt + 1} failed: {str(e)}")
                                await asyncio.sleep(2)  # Wait before retrying

                        # Extract URLs - works for both Pydantic models and dicts
                        data = getattr(result, "data", None) or (result.get("data") if isinstance(result, dict) else [])
                        urls = []
                        for item in data:
                            url = getattr(item, "url", None) or (item.get("url") if isinstance(item, dict) else None)
                            if url:
                                urls.append(url)

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
                                multi_provider=multi_provider,
                                search_providers=search_providers,
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

        else:
            # Multiple providers case - search each query with each provider
            async def search_with_provider(research_query: ResearchQuery, provider: str, search_client) -> Dict:
                # Variables to store results outside the semaphore block
                search_result = None
                urls = []

                # Only use semaphore for the search operation
                async with semaphore:
                    try:
                        # Search using this provider's client
                        for attempt in range(3):
                            try:
                                print(f"Searching with {provider} for {research_query.query}")
                                search_result = await search_client.search(research_query.query, timeout=20000)
                                print(
                                    f"Search finished from {provider} for {research_query.query} at time {datetime.now()}"
                                )
                                break
                            except Exception as e:
                                if attempt == 2:  # Last attempt
                                    raise
                                logger.warning(f"Search attempt {attempt + 1} failed: {str(e)}")
                                await asyncio.sleep(2)  # Wait before retrying

                        # Extract URLs - works for both Pydantic models and dicts
                        data = getattr(search_result, "data", None) or (
                            search_result.get("data") if isinstance(search_result, dict) else []
                        )
                        urls = []
                        for item in data:
                            url = getattr(item, "url", None) or (item.get("url") if isinstance(item, dict) else None)
                            if url:
                                urls.append(url)
                    except Exception as e:
                        logger.error(f"Error searching with {provider} for {research_query.query}: {str(e)}")

                # Process results outside the semaphore block
                if search_result:
                    try:
                        print(
                            f"Creating processing task for {provider} for {research_query.query} at time {datetime.now()}"
                        )

                        # Create a separate task for processing to avoid blocking the event loop
                        processing_task = asyncio.create_task(
                            self._process_search_result(
                                query=f"{research_query.query} [{provider}]", search_result=search_result
                            )
                        )

                        # Wait for the processing task to complete
                        processed_result = await processing_task
                        print(
                            f"Processed from {provider} content to extract learnings for {research_query.query} at time {datetime.now()}"
                        )

                        return {
                            "learnings": processed_result["learnings"],
                            "urls": urls,
                            "follow_up_questions": processed_result["follow_up_questions"],
                            "analysis": processed_result["analysis"],
                            "provider": provider,
                        }
                    except Exception as e:
                        logger.error(f"Error processing results for {research_query.query} with {provider}: {str(e)}")

                # Return empty results if there was an error
                return {
                    "learnings": [],
                    "urls": urls,
                    "follow_up_questions": [],
                    "analysis": f"Error with {provider}: Unknown error occurred",
                    "provider": provider,
                }

            async def process_query_with_providers(research_query: ResearchQuery) -> Dict:
                try:
                    # Create tasks to search with all providers in parallel
                    provider_tasks = [
                        search_with_provider(research_query, provider, client)
                        for provider, client in active_search_clients.items()
                    ]

                    # Run all provider searches in parallel
                    provider_results = await asyncio.gather(*provider_tasks)

                    # Combine results from all providers for this query
                    combined_result = {"learnings": [], "urls": [], "follow_up_questions": [], "analyses": []}

                    for result in provider_results:
                        combined_result["learnings"].extend(result["learnings"])
                        combined_result["urls"].extend(result["urls"])
                        combined_result["follow_up_questions"].extend(result["follow_up_questions"])
                        combined_result["analyses"].append(
                            {
                                "query": research_query.query,
                                "provider": result["provider"],
                                "analysis": result["analysis"],
                            }
                        )

                    # Process follow-up questions if needed
                    new_breadth = max(1, breadth // 2)
                    new_depth = depth - 1

                    if new_depth > 0 and combined_result["follow_up_questions"]:
                        # Get unique follow-up questions
                        unique_follow_ups = list(dict.fromkeys(combined_result["follow_up_questions"]))

                        next_query = "\n".join(
                            [
                                f"Previous research goal: {research_query.research_goal}",
                                "Follow-up questions to explore:",
                                "\n".join(f"- {q}" for q in unique_follow_ups[:new_breadth]),
                            ]
                        )

                        deeper_results = await self._deep_research(
                            query=next_query,
                            breadth=new_breadth,
                            depth=new_depth,
                            concurrency=concurrency,
                            multi_provider=multi_provider,
                            search_providers=search_providers,
                            learnings=learnings + combined_result["learnings"],
                            visited_urls=visited_urls + combined_result["urls"],
                            analyses=analyses + combined_result["analyses"],
                        )

                        return {
                            "learnings": deeper_results["learnings"],
                            "urls": deeper_results["visited_urls"],
                            "follow_up_questions": deeper_results["follow_up_questions"],
                            "analyses": deeper_results["analyses"],
                        }
                    else:
                        return combined_result
                except Exception as e:
                    logger.error(f"Error processing query with providers: {str(e)}")
                    return {"learnings": [], "urls": [], "follow_up_questions": [], "analyses": []}

            # Process all queries concurrently - outer level parallelism
            results = await asyncio.gather(*[process_query_with_providers(q) for q in search_queries])

        # Combine results from all queries
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
        all_questions = list(dict.fromkeys(all_questions))

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

        Create a dynamic amount of sections and subsections based on the content provided. Make sure to cover all the content and provide a comprehensive analysis.
        At a minimum, include the following sections:
        - Key findings and main themes
        - Source credibility and diversity
        - Information completeness and gaps
        - Emerging patterns and trends
        - Potential biases or conflicting information
        Make sure that for every relevant topic, you include a section and any subsctions it might need. Aside from the final conclusion, you should have at least 5 sections of subtopics and a sub conclusion per section.
        IMPORTANT: Aim for at least 3+ pages of content, don't be afraid to add more sections and subsections.
        IMPORTANT: Be verbose and detailed in your analysis. Don't over summarize, don't over simplify. Make as many sections and subsections as needed.

        IMPORTANT: MAKE SURE YOU RETURN THE JSON ONLY, NO OTHER TEXT OR MARKUP AND A VALID JSON.
        IMPORTANT: DONT ADD ANY COMMENTS OR MARKUP TO THE JSON. Example NO # or /* */ or /* */ or // or ``` or JSON or json or any other comments or markup.
        IMPORTANT: MAKE SURE YOU RETURN THE JSON ONLY, JSON SHOULD BE PERFECTLY FORMATTED. ALL KEYS SHOULD BE OPENED AND CLOSED.
        CRITICAL: If you cannot fit the entire report in one response, it is better to make it shorter and complete than to output incomplete JSON. NEVER output unterminated strings.
        """
        # Use higher max_tokens to reduce risk of truncated JSON responses
        max_tokens = 16000  # Generous limit for detailed reports

        if self.report_model:
            response, _, _ = await self.llm_provider.call(
                system_prompt=system_prompt,
                user_prompt=prompt,
                temperature=0.3,
                model_id=self.report_model,
                max_tokens=max_tokens,
            )
        else:
            # Pass None explicitly if self.report_model is None
            response, _, _ = await self.llm_provider.call(
                system_prompt=system_prompt, user_prompt=prompt, temperature=0.3, max_tokens=max_tokens
            )

        try:
            cleaned_response = response.replace("```json", "").replace("```", "").strip()
            result = json.loads(cleaned_response)
            report = result.get("reportMarkdown", "Error generating report")
            # Add sources section
            sources = "\n\n## Sources\n\n" + "\n".join([f"- {url}" for url in research_result["visited_urls"]])

            return report + sources
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing report JSON: {e}")
            logger.debug(f"Raw response (first 1000 chars): {response[:1000]}")

            # Try to extract reportMarkdown using string parsing as fallback
            try:
                # Look for "reportMarkdown": " pattern and extract until the closing quote
                if '"reportMarkdown"' in response:
                    start_idx = response.find('"reportMarkdown"')
                    if start_idx != -1:
                        # Find the opening quote after the colon
                        content_start = response.find('"', start_idx + len('"reportMarkdown"') + 1)
                        if content_start != -1:
                            content_start += 1  # Move past the opening quote
                            # Try to find the closing quote (accounting for escaped quotes)
                            content_end = content_start
                            while content_end < len(response):
                                if response[content_end] == '"' and response[content_end - 1] != '\\':
                                    break
                                content_end += 1

                            if content_end < len(response):
                                extracted_report = response[content_start:content_end]
                                # Unescape common JSON escape sequences
                                extracted_report = (
                                    extracted_report.replace('\\n', '\n')
                                    .replace('\\t', '\t')
                                    .replace('\\"', '"')
                                    .replace('\\\\', '\\')
                                )
                                sources = "\n\n## Sources\n\n" + "\n".join([f"- {url}" for url in research_result["visited_urls"]])
                                logger.info("Successfully extracted report using string parsing fallback")
                                return extracted_report + sources
            except Exception as extraction_error:
                logger.warning(f"String extraction fallback also failed: {extraction_error}")

            # Fallback report generation
            return (
                f"# Research Report: {original_query}\n\n"
                + "## Key Findings\n\n"
                + "\n".join([f"- {learning}" for learning in research_result["learnings"]])
                + "\n\n## Sources\n\n"
                + "\n".join([f"- {url}" for url in research_result["visited_urls"]])
                + "\n\n## Response\n\n"
                + response
            )

    def _get_system_prompt(self) -> str:
        """Get the system prompt for research operations"""
        return """You are an expert research analyst that processes web search results.
        Analyze the content and provide insights about for each section you identify:
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
        return """
        {
            "role": "You are an expert researcher specializing in producing exhaustive, analytically rigorous research reports.",
            "instructions": [
                "When responding, assume all provided facts—especially those after your knowledge cutoff—are accurate unless contradicted internally.",
                "The user is a highly experienced analyst. Do not simplify. Prioritize technical precision, domain-specific terminology, and comprehensive argumentation.",
                "Organize the report with multiple clearly defined sections, such as: Executive Summary, Background, Market Landscape, Problem Analysis, Technological Trends, Competitive Analysis, Risk Factors, Opportunities, Speculative Insights (clearly marked), Strategic Recommendations, and Conclusion.",
                "Each section should be verbose, detailed, and data-driven where possible. Aim for high information density.",
                "Anticipate what the user might need to know next. Include frameworks, mental models, and decision trees where relevant.",
                "Suggest novel or unconventional strategies the user may not have considered. Prioritize unique insight over consensus.",
                "Include emerging technologies, trends, and contrarian ideas. Be aggressive in surfacing innovations, and clearly identify areas of high uncertainty or risk.",
                "Do not cite sources by name unless necessary—strong reasoning is preferred over appeal to authority.",
                "You may speculate about future developments, but you must clearly mark any speculative or high-uncertainty claims.",
                "Use precise definitions, models, and numerical reasoning where appropriate.",
                "Provide critical evaluation of ideas, trade-offs, and second-order consequences.",
                "When delivering the report, ALWAYS return a single, clean JSON object and NOTHING ELSE.",
                "The JSON MUST be valid and properly formatted. No comments, markdown, or other markup is allowed.",
                "ALL KEYS in the JSON must be properly opened and closed with quotation marks."
                "IMPORTANT: MAKE SURE YOU RETURN THE JSON ONLY, NO OTHER TEXT OR MARKUP AND A VALID JSON."
                "DONT ADD ANY COMMENTS OR MARKUP TO THE JSON. Example NO # or /* */ or /* */ or // or any other comments or markup."
            ]
        }

        """

    def _get_report_system_prompt2(self) -> str:
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

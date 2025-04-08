import asyncio
import json
import os
from dataclasses import dataclass
from typing import Any, Dict, List

from dotenv import load_dotenv
from firecrawl import FirecrawlApp

from core.llm import call_llm_async, call_llm_with_tools_async
from core.utils.text_splitter import trim_prompt
from decorators import monitor_execution, with_cache, with_retry
from mesh.mesh_agent import MeshAgent

load_dotenv()


@dataclass
class SearchQuery:
    query: str
    research_goal: str


class DeepResearchAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.metadata.update(
            {
                "name": "Deep Research Agent",
                "version": "1.0.0",
                "author": "Heurist Team",
                "author_address": "0x7d9d1821d15B9e0b8Ab98A058361233E255E405D",
                "description": "Advanced research agent that performs multi-level web searches with recursive exploration, analyzes content across sources, and produces comprehensive research reports with key insights",
                "inputs": [
                    {"name": "query", "description": "Research query or topic", "type": "str", "required": True},
                    {
                        "name": "depth",
                        "description": "Research depth (1-3)",
                        "type": "int",
                        "required": False,
                        "default": 2,
                    },
                    {
                        "name": "breadth",
                        "description": "Search breadth per level (1-5)",
                        "type": "int",
                        "required": False,
                        "default": 3,
                    },
                    {
                        "name": "concurrency",
                        "description": "Number of concurrent searches",
                        "type": "int",
                        "required": False,
                        "default": 2,
                    },
                ],
                "outputs": [
                    {
                        "name": "response",
                        "description": "Detailed analysis and research findings",
                        "type": "str",
                    },
                    {
                        "name": "data",
                        "description": "Raw search results and metadata",
                        "type": "dict",
                    },
                ],
                "external_apis": ["Firecrawl"],
                "tags": ["Research"],
                "image_url": "https://raw.githubusercontent.com/heurist-network/heurist-agent-framework/refs/heads/main/mesh/images/deep_research.png",  # use an emoji of 🔍
                "examples": [
                    "What is the latest news on Bitcoin?",
                    "Find information about the Ethereum blockchain",
                    "Search for articles about the latest trends in AI",
                    "What are the latest developments in zero knowledge proofs?",
                ],
            }
        )
        self.app = FirecrawlApp(api_key=os.environ.get("FIRECRAWL_KEY", ""))
        self._last_request_time = 0

    def get_system_prompt(self) -> str:
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
        detailed analysis, and recommendations for further research."""

    @monitor_execution()
    @with_cache(ttl_seconds=300)
    @with_retry(max_retries=3)
    async def search(self, query: str, limit: int = 5) -> Dict:
        """Execute search with rate limiting and error handling"""
        try:
            # Run the synchronous SDK call in a thread pool
            response = await asyncio.get_event_loop().run_in_executor(
                None, lambda: self.app.search(query=query, params={"scrapeOptions": {"formats": ["markdown"]}})
            )

            # Handle the response format from the SDK
            if isinstance(response, dict) and "data" in response:
                # Response is already in the right format
                return response
            elif isinstance(response, dict) and "success" in response:
                # Response is in the documented format
                return {"data": response.get("data", [])}
            elif isinstance(response, list):
                # Response is a list of results
                formatted_data = []
                for item in response:
                    if isinstance(item, dict):
                        formatted_data.append(item)
                    else:
                        # Handle non-dict items (like objects)
                        formatted_data.append(
                            {
                                "url": getattr(item, "url", ""),
                                "markdown": getattr(item, "markdown", "") or getattr(item, "content", ""),
                                "title": getattr(item, "title", "") or getattr(item, "metadata", {}).get("title", ""),
                            }
                        )
                return {"data": formatted_data}
            else:
                print(f"Unexpected response format from Firecrawl: {type(response)}")
                return {"data": []}

        except Exception as e:
            print(f"Search error: {e}")
            print(f"Response type: {type(response) if 'response' in locals() else 'N/A'}")
            return {"data": []}

    async def generate_search_queries(
        self, query: str, num_queries: int = 3, learnings: List[str] = None
    ) -> List[SearchQuery]:
        """Generate intelligent search queries based on the input topic and previous learnings"""
        learnings_text = "\n".join(learnings) if learnings else ""
        prompt = f"""Generate {num_queries} specific search queries to investigate this topic: {query}

        Previous learnings to consider:
        {learnings_text}"""

        tools = [
            {
                "type": "function",
                "function": {
                    "name": "generate_queries",
                    "description": "Generate search queries for a topic",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "queries": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {"query": {"type": "string"}, "research_goal": {"type": "string"}},
                                    "required": ["query", "research_goal"],
                                },
                            }
                        },
                        "required": ["queries"],
                    },
                },
            }
        ]
        response = await call_llm_with_tools_async(
            base_url=self.heurist_base_url,
            api_key=self.heurist_api_key,
            model_id=self.metadata["large_model_id"],
            messages=[{"role": "system", "content": self.get_system_prompt()}, {"role": "user", "content": prompt}],
            tools=tools,
            tool_choice={"type": "function", "function": {"name": "generate_queries"}},
            temperature=0.7,
        )
        # print("response: ", response)
        try:
            # Extract the arguments from tool_calls
            if isinstance(response, dict) and "tool_calls" in response:
                tool_call = response["tool_calls"]
                # print("tool_call: ", tool_call)
                if hasattr(tool_call, "function"):
                    arguments = tool_call.function.arguments
                    # print("arguments: ", arguments)
                    if isinstance(arguments, str):
                        result = json.loads(arguments)
                        # print("result: ", result)
                        queries = result.get("queries", [])
                        return [SearchQuery(**q) for q in queries][:num_queries]
        except Exception as e:
            print(f"Error generating queries: {e}")
            print(f"Raw response: {response}")
            return [SearchQuery(query=query, research_goal="Main topic research")]

    @with_retry(max_retries=3)
    async def analyze_results(self, query: str, search_results: Dict) -> Dict[str, Any]:
        """Analyze search results and generate insights"""
        contents = [
            trim_prompt(item.get("markdown", ""), 25000)
            for item in search_results.get("data", [])
            if item.get("markdown")
        ]

        if not contents:
            return {"analysis": "No search results found to analyze.", "key_findings": [], "recommendations": []}

        prompt = (
            f"Analyze these search results for the query: {query}\n\n"
            f"Content:\n{' '.join(contents)}\n\n"
            f"Provide a detailed analysis including key findings, main themes, "
            f"and recommendations for further research. Return as JSON with "
            f"'analysis', 'key_findings', and 'recommendations' fields."
        )
        prompt_example = """
        IMPORTANT: MAKE SURE YOU RETURN THE JSON ONLY, NO OTHER TEXT OR MARKUP AND A VALID JSON.
        DONT ADD ANY COMMENTS OR MARKUP TO THE JSON. Example NO # or /* */ or /* */ or // or ``` or JSON or any other comments or markup.
        MAKE SURE YOU RETURN THE JSON ONLY, JSON SHOULD BE PERFECTLY FORMATTED. ALL KEYS SHOULD BE OPENED AND CLOSED.
        USE THE FOLLOWING FORMAT FOR THE JSON:
        {
            "analysis": "Analysis of the search results",
            "key_findings": ["Key finding 1", "Key finding 2"],
            "recommendations": ["Recommendation 1", "Recommendation 2"]
        }
        """
        prompt = prompt + prompt_example
        response = await call_llm_async(
            base_url=self.heurist_base_url,
            api_key=self.heurist_api_key,
            model_id=self.metadata["large_model_id"],
            messages=[{"role": "system", "content": self.get_system_prompt()}, {"role": "user", "content": prompt}],
            temperature=0.3,
        )
        response = response.replace("```json", "").replace("```", "")
        # print("response: ", response)
        try:
            return json.loads(response)
        except Exception as e:
            print(f"Error analyzing results: {e}")
            return {"analysis": "Error processing search results.", "key_findings": [], "recommendations": []}

    async def deep_research(
        self,
        query: str,
        breadth: int,
        depth: int,
        concurrency: int,
        learnings: List[str] = None,
        visited_urls: List[str] = None,
    ) -> Dict[str, Any]:
        """Execute recursive deep research with learnings tracking"""
        learnings = learnings or []
        visited_urls = visited_urls or []
        all_results = []
        all_analyses = []

        # Generate search queries using previous learnings
        search_queries = await self.generate_search_queries(query=query, num_queries=breadth, learnings=learnings)
        # print("search_queries: ", search_queries)
        # Create semaphore for concurrent execution
        semaphore = asyncio.Semaphore(concurrency)

        async def process_query(search_query: SearchQuery) -> Dict[str, Any]:
            async with semaphore:
                try:
                    # Add rate limiting
                    current_time = asyncio.get_event_loop().time()
                    time_since_last = current_time - self._last_request_time
                    if time_since_last < 6:
                        await asyncio.sleep(6 - time_since_last)
                    self._last_request_time = current_time

                    # Execute search
                    results = await self.search(search_query.query)
                    if not results.get("data"):
                        return {"results": [], "learnings": [], "urls": []}
                    # print("results: ", results)
                    # Extract URLs and analyze results
                    new_urls = [item.get("url") for item in results["data"] if item.get("url")]
                    analysis = await self.analyze_results(search_query.query, results)

                    # Calculate next level parameters
                    new_breadth = max(1, breadth // 2)
                    new_depth = depth - 1

                    # If we have depth remaining, explore follow-up questions
                    if new_depth > 0 and analysis.get("recommendations"):
                        for follow_up in analysis["recommendations"][:new_breadth]:
                            sub_results = await self.deep_research(
                                query=follow_up,
                                breadth=new_breadth,
                                depth=new_depth,
                                concurrency=concurrency,
                                learnings=learnings + analysis.get("key_findings", []),
                                visited_urls=visited_urls + new_urls,
                            )
                            results["data"].extend(sub_results.get("all_results", []))
                            analysis["key_findings"].extend(sub_results.get("learnings", []))
                            new_urls.extend(sub_results.get("visited_urls", []))
                    # print("analysis: ", analysis)
                    return {"results": results["data"], "analysis": analysis, "urls": new_urls}

                except Exception as e:
                    print(f"Error processing query {search_query.query}: {e}")
                    return {"results": [], "learnings": [], "urls": []}

        # Process all queries concurrently
        query_results = await asyncio.gather(*[process_query(query) for query in search_queries])

        # Combine results
        for result in query_results:
            all_results.extend(result["results"])
            if "analysis" in result:
                all_analyses.append(result["analysis"])
            visited_urls.extend(result["urls"])

        # Remove duplicates
        visited_urls = list(dict.fromkeys(visited_urls))

        # Extract unique learnings from analyses
        all_learnings = []
        for analysis in all_analyses:
            all_learnings.extend(analysis.get("key_findings", []))
        all_learnings = list(dict.fromkeys(all_learnings))

        return {
            "all_results": all_results,
            "analyses": all_analyses,
            "learnings": all_learnings,
            "visited_urls": visited_urls,
        }

    async def generate_comprehensive_report(self, query: str, research_results: Dict[str, Any]) -> str:
        """Generate detailed research report"""
        learnings_str = "\n".join([f"- {learning}" for learning in research_results["learnings"]])
        analyses_str = json.dumps(research_results["analyses"], indent=2)

        prompt = f"""
        Given the following prompt from the user, write a final report on the topic using
        the learnings from research. Return a JSON object with a 'reportMarkdown' field
        containing a detailed markdown report (aim for 3+ pages). Include ALL the learnings
        from research:
        <prompt>
        {query}
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

        report = await call_llm_async(
            base_url=self.heurist_base_url,
            api_key=self.heurist_api_key,
            model_id=self.metadata["large_model_id"],
            messages=[{"role": "system", "content": self.get_system_prompt()}, {"role": "user", "content": prompt}],
            temperature=0.3,
        )
        report = report.replace("```json", "").replace("```", "")
        # Add sources section
        sources = "\n\n## Sources\n\n" + "\n".join([f"- {url}" for url in research_results["visited_urls"]])

        return report + sources

    def get_tool_schemas(self) -> List[Dict]:
        return [
            {
                "type": "function",
                "function": {
                    "name": "deep_research",
                    "description": "Perform comprehensive multi-level web research on a topic with recursive exploration. This function analyzes content across multiple sources, explores various research paths, and synthesizes findings into a structured report. It's slow and expensive, so use it sparingly and only when you need to explore a broad topic in depth.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {"type": "string", "description": "Research query or topic"},
                            "depth": {"type": "number", "description": "Research depth (1-3)", "default": 2},
                            "breadth": {
                                "type": "number",
                                "description": "Search breadth per level (1-5)",
                                "default": 3,
                            },
                            "concurrency": {
                                "type": "number",
                                "description": "Number of concurrent searches",
                                "default": 2,
                            },
                        },
                        "required": ["query"],
                    },
                },
            }
        ]

    async def _handle_tool_logic(
        self, tool_name: str, function_args: dict, query: str, tool_call_id: str, raw_data_only: bool
    ) -> Dict[str, Any]:
        """Handle execution of specific tools and format responses"""

        if tool_name == "deep_research":
            query = function_args.get("query")
            depth = min(max(function_args.get("depth", 2), 1), 3)
            breadth = min(max(function_args.get("breadth", 3), 1), 5)
            concurrency = min(max(function_args.get("concurrency", 2), 1), 3)

            if not query:
                return {"error": "Missing 'query' in tool_arguments"}

            # Execute deep research
            research_results = await self.deep_research(
                query=query, breadth=breadth, depth=depth, concurrency=concurrency
            )

            if raw_data_only:
                return {
                    "response": "",
                    "data": {
                        "query_info": {
                            "query": query,
                            "depth": depth,
                            "breadth": breadth,
                            "result_count": len(research_results["all_results"]),
                        },
                        "results": research_results["all_results"],
                        "analyses": research_results["analyses"],
                        "learnings": research_results["learnings"],
                        "visited_urls": research_results["visited_urls"],
                    },
                }

            # Generate comprehensive report
            report = await self.generate_comprehensive_report(query=query, research_results=research_results)

            return {
                "response": report,
                "data": {
                    "query_info": {
                        "query": query,
                        "depth": depth,
                        "breadth": breadth,
                        "result_count": len(research_results["all_results"]),
                    },
                    "results": [
                        {
                            **{k: v for k, v in result.items() if k not in ["markdown", "metadata"]},
                            "content_length": len(result.get("markdown", "")),
                        }
                        for result in research_results["all_results"]
                    ],
                    "analyses": research_results["analyses"],
                    "learnings": research_results["learnings"],
                    "visited_urls": research_results["visited_urls"],
                },
            }
        else:
            return {"error": f"Unsupported tool: {tool_name}"}

    @monitor_execution()
    @with_retry(max_retries=3)
    async def handle_message(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle incoming messages, supporting both direct tool calls and natural language queries.
        """
        query = params.get("query")
        tool_name = params.get("tool")
        tool_args = params.get("tool_arguments", {})
        raw_data_only = params.get("raw_data_only", False)

        # Direct tool call
        if tool_name:
            return await self._handle_tool_logic(
                tool_name=tool_name,
                function_args=tool_args,
                query=query or "Direct tool call without LLM.",
                tool_call_id="direct_tool",
                raw_data_only=raw_data_only,
            )

        # Natural language query (LLM decides the tool)
        if query:
            response = await call_llm_with_tools_async(
                base_url=self.heurist_base_url,
                api_key=self.heurist_api_key,
                model_id=self.metadata["large_model_id"],
                system_prompt=self.get_system_prompt(),
                user_prompt=query,
                temperature=0.1,
                tools=self.get_tool_schemas(),
            )

            if not response:
                return {"error": "Failed to process query"}
            if not response.get("tool_calls"):
                return {"response": response["content"], "data": {}}

            tool_call = response["tool_calls"]
            tool_call_name = tool_call.function.name
            tool_call_args = json.loads(tool_call.function.arguments)

            return await self._handle_tool_logic(
                tool_name=tool_call_name,
                function_args=tool_call_args,
                query=query,
                tool_call_id=tool_call.id,
                raw_data_only=raw_data_only,
            )

        return {"error": "Either 'query' or 'tool' must be provided in the parameters."}

import asyncio
import json
import logging
import os
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

import boto3
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)


class FirecrawlLogger:
    """Firecrawl logger for R2 storage - logs all operations including failures."""

    def __init__(self):
        self.r2_endpoint = os.getenv("R2_ENDPOINT")
        self.r2_access_key = os.getenv("R2_ACCESS_KEY")
        self.r2_secret_key = os.getenv("R2_SECRET_KEY")
        self.bucket_name = "firecrawl-results"

        if not all([self.r2_endpoint, self.r2_access_key, self.r2_secret_key]):
            logger.warning("R2 credentials missing - logging disabled")
            self.enabled = False
            return

        self.enabled = True
        try:
            self.r2_client = boto3.client(
                "s3",
                endpoint_url=self.r2_endpoint,
                aws_access_key_id=self.r2_access_key,
                aws_secret_access_key=self.r2_secret_key,
                region_name="auto",
            )
            logger.info("FirecrawlLogger initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize R2 client: {e}")
            self.enabled = False

    async def _upload_with_retry(self, filename: str, content: str, max_retries: int = 3):
        """Upload file to R2 with retry logic."""
        if not self.enabled:
            return False

        for attempt in range(max_retries):
            try:
                loop = asyncio.get_event_loop()
                await loop.run_in_executor(
                    None,
                    lambda: self.r2_client.put_object(
                        Bucket=self.bucket_name,
                        Key=filename,
                        Body=content.encode("utf-8"),
                        ContentType="text/plain",
                    ),
                )
                logger.debug(f"Uploaded: {filename}")
                return True
            except Exception as e:
                if attempt == max_retries - 1:
                    logger.error(f"Failed to upload {filename} after {max_retries} attempts: {e}")
                else:
                    await asyncio.sleep(1 * (attempt + 1))  # Exponential backoff
        return False

    def _format_content(self, query_or_url: str, data: Any) -> str:
        """Format content: first line query/url, second line stats, then data."""
        # Convert data to string
        if isinstance(data, (dict, list)):
            content = json.dumps(data, ensure_ascii=False, indent=2)
        else:
            content = str(data)

        # Calculate stats
        char_count = len(content)
        word_count = len(content.split())

        # Format as specified
        return f"{query_or_url}\nCharacter count: {char_count}, Word count: {word_count}\n{content}"

    async def log_request_initiated(self, operation_type: str, params: Dict[str, Any]) -> str:
        """Log when a request is initiated (before processing)."""
        if not self.enabled:
            return "logging-disabled"

        request_id = str(uuid.uuid4())
        date = datetime.now().strftime("%Y-%m-%d")
        timestamp = datetime.now().strftime("%H:%M:%S")

        logger.info(f"Logging request initiation: {request_id} for {operation_type}")

        # Create request initiation log
        request_data = {
            "status": "initiated",
            "operation_type": operation_type,
            "timestamp": f"{date} {timestamp}",
            "request_id": request_id,
            "parameters": params,
        }

        filename = f"{date}-{operation_type}-{request_id}-request.txt"
        content = self._format_content(f"Request: {operation_type}", request_data)

        await self._upload_with_retry(filename, content)

        # Append to history with INITIATED status
        history_entry = f"{date}--{timestamp}--{request_id}--{operation_type}--INITIATED--{json.dumps(params, ensure_ascii=False)[:100]}\n"
        await self._append_to_history(history_entry)

        return request_id

    async def log_request_failed(
        self,
        request_id: str,
        operation_type: str,
        error_message: str,
        params: Dict[str, Any],
        partial_data: Optional[Any] = None,
    ) -> None:
        """Log when a request fails."""
        if not self.enabled:
            return

        date = datetime.now().strftime("%Y-%m-%d")
        timestamp = datetime.now().strftime("%H:%M:%S")

        logger.info(f"Logging request failure: {request_id} for {operation_type}")

        # Create failure log
        failure_data = {
            "status": "failed",
            "operation_type": operation_type,
            "timestamp": f"{date} {timestamp}",
            "request_id": request_id,
            "error": error_message,
            "parameters": params,
            "partial_data": partial_data if partial_data else "No data retrieved",
        }

        filename = f"{date}-{operation_type}-{request_id}-failure.txt"
        content = self._format_content(f"Failed Request: {operation_type}", failure_data)

        await self._upload_with_retry(filename, content)

        # Append to history with FAILED status
        history_entry = f"{date}--{timestamp}--{request_id}--{operation_type}--FAILED--{error_message[:100]}\n"
        await self._append_to_history(history_entry)

    async def log_search_operation(
        self, search_query: str, raw_results: List[Dict], llm_processed_result: str, request_id: Optional[str] = None
    ) -> str:
        """Log successful search operation with raw results and LLM summary."""
        if not self.enabled:
            return "logging-disabled"

        if not request_id:
            request_id = str(uuid.uuid4())
        date = datetime.now().strftime("%Y-%m-%d")
        timestamp = datetime.now().strftime("%H:%M:%S")

        logger.info(f"Logging successful search: {request_id} ({len(raw_results)} results)")

        # Create upload tasks
        tasks = []

        # Upload each raw result
        for i, result in enumerate(raw_results, 1):
            filename = f"{date}-search-{request_id}-{i}.txt"
            content = self._format_content(search_query, result)
            tasks.append(self._upload_with_retry(filename, content))

        # Upload LLM result
        result_filename = f"{date}-search-{request_id}-result.txt"
        result_content = self._format_content(search_query, llm_processed_result)
        tasks.append(self._upload_with_retry(result_filename, result_content))

        # Upload success status
        success_data = {
            "status": "success",
            "operation_type": "search",
            "timestamp": f"{date} {timestamp}",
            "request_id": request_id,
            "query": search_query,
            "result_count": len(raw_results),
        }
        success_filename = f"{date}-search-{request_id}-success.txt"
        success_content = self._format_content(search_query, success_data)
        tasks.append(self._upload_with_retry(success_filename, success_content))

        # Append to history with SUCCESS status
        history_entry = f"{date}--{timestamp}--{request_id}--search--SUCCESS--{len(raw_results)}--{search_query}\n"
        tasks.append(self._append_to_history(history_entry))

        # Execute all uploads
        results = await asyncio.gather(*tasks, return_exceptions=True)
        successful = sum(1 for r in results if r is True)

        if successful > 0:
            logger.info(f"Logged {successful}/{len(tasks)} files for request {request_id}")

        return request_id

    async def log_scrape_operation(
        self, scrape_url: str, raw_content: str, llm_processed_result: str, request_id: Optional[str] = None
    ) -> str:
        """Log successful scrape operation with raw content and LLM summary."""
        if not self.enabled:
            return "logging-disabled"

        if not request_id:
            request_id = str(uuid.uuid4())
        date = datetime.now().strftime("%Y-%m-%d")
        timestamp = datetime.now().strftime("%H:%M:%S")

        logger.info(f"Logging successful scrape: {request_id}")

        tasks = []

        # Upload raw content
        raw_filename = f"{date}-scrape-{request_id}-1.txt"
        raw_content_formatted = self._format_content(scrape_url, raw_content)
        tasks.append(self._upload_with_retry(raw_filename, raw_content_formatted))

        # Upload LLM result
        result_filename = f"{date}-scrape-{request_id}-result.txt"
        result_content = self._format_content(scrape_url, llm_processed_result)
        tasks.append(self._upload_with_retry(result_filename, result_content))

        # Upload success status
        success_data = {
            "status": "success",
            "operation_type": "scrape",
            "timestamp": f"{date} {timestamp}",
            "request_id": request_id,
            "url": scrape_url,
            "content_length": len(raw_content),
        }
        success_filename = f"{date}-scrape-{request_id}-success.txt"
        success_content = self._format_content(scrape_url, success_data)
        tasks.append(self._upload_with_retry(success_filename, success_content))

        # Append to history with SUCCESS status
        history_entry = f"{date}--{timestamp}--{request_id}--scrape--SUCCESS--1--{scrape_url}\n"
        tasks.append(self._append_to_history(history_entry))

        # Execute all uploads
        results = await asyncio.gather(*tasks, return_exceptions=True)
        successful = sum(1 for r in results if r is True)

        if successful > 0:
            logger.info(f"Logged {successful}/{len(tasks)} files for request {request_id}")

        return request_id

    async def log_extract_operation(
        self, urls: List[str], extraction_prompt: str, raw_extracted_data: Any, request_id: Optional[str] = None
    ) -> str:
        """Log successful extract operation."""
        if not self.enabled:
            return "logging-disabled"

        if not request_id:
            request_id = str(uuid.uuid4())
        date = datetime.now().strftime("%Y-%m-%d")
        timestamp = datetime.now().strftime("%H:%M:%S")

        combined_query = f"URLs: {', '.join(urls)} | Prompt: {extraction_prompt}"
        logger.info(f"Logging successful extract: {request_id}")

        tasks = []

        # Upload extracted data
        filename = f"{date}-extract-{request_id}-1.txt"
        content = self._format_content(combined_query, raw_extracted_data)
        tasks.append(self._upload_with_retry(filename, content))

        # Upload success status
        success_data = {
            "status": "success",
            "operation_type": "extract",
            "timestamp": f"{date} {timestamp}",
            "request_id": request_id,
            "urls": urls,
            "extraction_prompt": extraction_prompt,
        }
        success_filename = f"{date}-extract-{request_id}-success.txt"
        success_content = self._format_content(combined_query, success_data)
        tasks.append(self._upload_with_retry(success_filename, success_content))

        # Append to history with SUCCESS status
        history_entry = f"{date}--{timestamp}--{request_id}--extract--SUCCESS--1--{combined_query[:100]}\n"
        tasks.append(self._append_to_history(history_entry))

        await asyncio.gather(*tasks, return_exceptions=True)
        return request_id

    async def _append_to_history(self, entry: str) -> bool:
        """Append to history log file."""
        if not self.enabled:
            return False

        try:
            # Try to get existing history
            existing = ""
            try:
                loop = asyncio.get_event_loop()
                response = await loop.run_in_executor(
                    None, lambda: self.r2_client.get_object(Bucket=self.bucket_name, Key="request-history.log")
                )
                existing = response["Body"].read().decode("utf-8")
            except self.r2_client.exceptions.NoSuchKey:
                pass  # File doesn't exist yet
            except Exception as e:
                logger.debug(f"Could not read history: {e}")

            # Upload updated history
            return await self._upload_with_retry("request-history.log", existing + entry)
        except Exception as e:
            logger.error(f"Failed to update history: {e}")
            return False

    async def get_statistics(self) -> Dict[str, Any]:
        """Get statistics from logged operations."""
        if not self.enabled:
            return {"status": "disabled"}

        try:
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None, lambda: self.r2_client.get_object(Bucket=self.bucket_name, Key="request-history.log")
            )
            history = response["Body"].read().decode("utf-8")

            lines = history.strip().split("\n")
            total = len(lines)
            initiated = sum(1 for line in lines if "--INITIATED--" in line)
            successful = sum(1 for line in lines if "--SUCCESS--" in line)
            failed = sum(1 for line in lines if "--FAILED--" in line)

            return {
                "total_operations": total,
                "initiated": initiated,
                "successful": successful,
                "failed": failed,
                "success_rate": f"{(successful / total) * 100:.2f}%" if total > 0 else "0%",
            }
        except Exception as e:
            logger.error(f"Failed to get statistics: {e}")
            return {"status": "error", "error": str(e)}

    def is_enabled(self) -> bool:
        """Check if logging is enabled."""
        return self.enabled

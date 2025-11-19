import asyncio
import logging
import os
from typing import Any, Dict, List, Optional

import aiohttp
import boto3
from dotenv import load_dotenv

from decorators import with_cache, with_retry
from mesh.mesh_agent import MeshAgent

logger = logging.getLogger(__name__)
load_dotenv()


class WanVideoGenAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("ALIBABA_API_KEY")
        if not self.api_key:
            raise ValueError("ALIBABA_API_KEY environment variable is required")

        self.base_url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "X-DashScope-Async": "enable",
        }

        self.r2_endpoint = os.getenv("R2_ENDPOINT")
        self.r2_access_key = os.getenv("R2_ACCESS_KEY")
        self.r2_secret_key = os.getenv("R2_SECRET_KEY")
        self.r2_bucket = os.getenv("R2_BUCKET_WAN_VIDEO_AGENT")

        if not all([self.r2_endpoint, self.r2_access_key, self.r2_secret_key, self.r2_bucket]):
            raise ValueError(
                "R2 credentials (R2_ENDPOINT, R2_ACCESS_KEY, R2_SECRET_KEY, R2_BUCKET_WAN_VIDEO_AGENT) are required"
            )

        self.s3_client = boto3.client(
            "s3",
            endpoint_url=self.r2_endpoint,
            aws_access_key_id=self.r2_access_key,
            aws_secret_access_key=self.r2_secret_key,
            region_name="auto",
        )

        self.metadata.update(
            {
                "name": "Wan Video Generation Agent",
                "version": "1.0.0",
                "author": "Heurist team",
                "author_address": "0x7d9d1821d15B9e0b8Ab98A058361233E255E405D",
                "description": "Generate videos using Alibaba Wan 2.2 models. Supports text-to-video and image-to-video generation in 480p resolution.",
                "external_apis": ["DashScope"],
                "tags": ["Video Generation"],
                "recommended": True,
                "image_url": "https://raw.githubusercontent.com/heurist-network/heurist-agent-framework/refs/heads/main/mesh/images/Wan.png",
                "examples": [
                    "Generate a video of a cat running on grass",
                    "Create a video from an image showing ocean waves",
                    "Check status of task: abc123",
                ],
                "credits": 10,
                "large_model_id": "google/gemini-2.5-flash",
                "small_model_id": "google/gemini-2.5-flash",
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.15",
                    "tool_prices": {
                        "text_to_video_480p_5s": "0.15",  # wan2.2-t2v-plus: $0.03/s × 5s = $0.15
                        "text_to_video_with_audio_480p_5s": "0.25",  # wan2.5-t2v-preview: $0.05/s × 5s = $0.25
                        "image_to_video_plus_480p_5s": "0.15",  # wan2.2-i2v-plus: $0.03/s × 5s = $0.15
                        "image_to_video_flash_480p_5s": "0.10",  # wan2.2-i2v-flash: $0.02/s × 5s = $0.10
                        "image_to_video_with_audio_480p_5s": "0.25",  # wan2.5-i2v-preview: $0.05/s × 5s = $0.25
                        "get_video_status": "0.001",
                    },
                },
            }
        )

    def get_system_prompt(self) -> str:
        return """You help users generate videos using Alibaba Wan models. All videos are 480p resolution at 5 seconds. Select tools based on: audio (wan2.5 has audio, wan2.2 is silent), and speed (Flash is faster, Plus is higher quality). Generate videos and return URLs."""

    def get_tool_schemas(self) -> List[Dict]:
        return [
            {
                "type": "function",
                "function": {
                    "name": "text_to_video_480p_5s",
                    "description": "Generate 5-second 480p silent video from text using Wan 2.2 Plus",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "prompt": {
                                "type": "string",
                                "description": "Text description of the video to generate",
                            },
                            "prompt_extend": {
                                "type": "boolean",
                                "description": "Whether to extend/enhance the prompt automatically",
                                "default": True,
                            },
                        },
                        "required": ["prompt"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "text_to_video_with_audio_480p_5s",
                    "description": "Generate 5-second 480p video WITH AUDIO from text using Wan 2.5 Preview",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "prompt": {
                                "type": "string",
                                "description": "Text description of the video to generate",
                            },
                            "prompt_extend": {
                                "type": "boolean",
                                "description": "Whether to extend/enhance the prompt automatically",
                                "default": True,
                            },
                        },
                        "required": ["prompt"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "image_to_video_plus_480p_5s",
                    "description": "Generate 5-second 480p silent video from image using Wan 2.2 Plus (high quality)",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "prompt": {
                                "type": "string",
                                "description": "Description of how the image should animate",
                            },
                            "image_url": {
                                "type": "string",
                                "description": "URL of the image to animate",
                            },
                            "prompt_extend": {
                                "type": "boolean",
                                "description": "Whether to extend/enhance the prompt automatically",
                                "default": True,
                            },
                        },
                        "required": ["prompt", "image_url"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "image_to_video_flash_480p_5s",
                    "description": "Generate 5-second 480p silent video from image using Wan 2.2 Flash (fast generation)",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "prompt": {
                                "type": "string",
                                "description": "Description of how the image should animate",
                            },
                            "image_url": {
                                "type": "string",
                                "description": "URL of the image to animate",
                            },
                            "prompt_extend": {
                                "type": "boolean",
                                "description": "Whether to extend/enhance the prompt automatically",
                                "default": True,
                            },
                        },
                        "required": ["prompt", "image_url"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "image_to_video_with_audio_480p_5s",
                    "description": "Generate 5-second 480p video WITH AUDIO from image using Wan 2.5 Preview",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "prompt": {
                                "type": "string",
                                "description": "Description of how the image should animate",
                            },
                            "image_url": {
                                "type": "string",
                                "description": "URL of the image to animate",
                            },
                            "prompt_extend": {
                                "type": "boolean",
                                "description": "Whether to extend/enhance the prompt automatically",
                                "default": True,
                            },
                        },
                        "required": ["prompt", "image_url"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "get_video_status",
                    "description": "Check the status of a video generation task and retrieve the video URL if completed.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "task_id": {
                                "type": "string",
                                "description": "The task ID returned from text_to_video or image_to_video.",
                            }
                        },
                        "required": ["task_id"],
                    },
                },
            },
        ]

    def get_default_timeout_seconds(self) -> Optional[int]:
        return 30

    async def _create_video_task(
        self, model: str, input_data: Dict[str, Any], parameters: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Create a video generation task and return the task ID immediately"""
        logger.info(f"Creating video generation task with model: {model}")

        payload = {"model": model, "input": input_data, "parameters": parameters}

        response = await self._api_request(url=self.base_url, method="POST", headers=self.headers, json_data=payload)

        if "error" in response:
            logger.error(f"DashScope API error: {response['error']}")
            return {"status": "error", "error": response["error"]}

        task_id = response.get("output", {}).get("task_id")
        task_status = response.get("output", {}).get("task_status")

        if not task_id:
            logger.error("No task ID returned from DashScope API")
            return {"status": "error", "error": "Failed to create video generation task"}

        logger.info(f"Video task created: {task_id}, status: {task_status}")
        return {"status": "success", "task_id": task_id, "task_status": task_status}

    async def _get_task_result(self, task_id: str) -> Dict[str, Any]:
        """Retrieve video generation task result"""
        logger.info(f"Retrieving video task result: {task_id}")

        url = f"https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}"
        headers = {"Authorization": f"Bearer {self.api_key}"}

        response = await self._api_request(url=url, method="GET", headers=headers)

        if "error" in response:
            logger.error(f"DashScope API error: {response['error']}")
            return {"status": "error", "error": response["error"]}

        return {"status": "success", "data": response}

    async def _download_and_upload_to_r2(self, video_url: str, task_id: str) -> str:
        """Download video from Alibaba and upload to R2"""
        logger.info(f"Downloading video from {video_url}")

        async with aiohttp.ClientSession() as session:
            async with session.get(video_url) as response:
                if response.status != 200:
                    raise Exception(f"Failed to download video: HTTP {response.status}")
                video_data = await response.read()

        logger.info(f"Downloaded {len(video_data)} bytes")
        filename = f"videos/{task_id}.mp4"
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(
            None,
            lambda: self.s3_client.put_object(
                Bucket=self.r2_bucket, Key=filename, Body=video_data, ContentType="video/mp4"
            ),
        )
        r2_preview_url = f"https://images.heurist.xyz/{filename}"
        logger.info(f"Uploaded to R2: {r2_preview_url}")

        return r2_preview_url

    @with_cache(ttl_seconds=60)
    @with_retry(max_retries=3)
    async def text_to_video(
        self,
        prompt: str,
        model: str = "wan2.2-t2v-plus",
        prompt_extend: bool = True,
        size: str = "832*480",
        audio: bool = False,
        duration: int = 5,
    ) -> Dict[str, Any]:
        """Start text-to-video generation and return task ID immediately"""
        logger.info(f"Starting video generation from text: {prompt[:50]}... with model {model}")

        input_data = {"prompt": prompt}
        parameters = {"size": size, "prompt_extend": prompt_extend, "duration": duration}
        if audio:
            parameters["audio"] = True

        create_result = await self._create_video_task(model, input_data, parameters)

        if create_result.get("status") != "success":
            return create_result

        task_id = create_result["task_id"]

        return {
            "status": "success",
            "data": {
                "task_id": task_id,
                "task_status": create_result["task_status"],
                "model": model,
                "prompt": prompt,
                "message": "Video generation started. It will take 1-5 minutes to complete. Use get_video_status with this task_id to check progress.",
            },
        }

    @with_cache(ttl_seconds=60)
    @with_retry(max_retries=3)
    async def image_to_video(
        self,
        prompt: str,
        image_url: str,
        model: str = "wan2.2-i2v-plus",
        prompt_extend: bool = True,
        resolution: str = "480P",
        audio: bool = False,
        duration: int = 5,
    ) -> Dict[str, Any]:
        """Start image-to-video generation and return task ID immediately"""
        logger.info(f"Starting video generation from image: {image_url[:50]}... with prompt: {prompt[:50]}...")

        input_data = {"prompt": prompt, "img_url": image_url}
        parameters = {"resolution": resolution, "prompt_extend": prompt_extend, "duration": duration}
        if audio:
            parameters["audio"] = True

        create_result = await self._create_video_task(model, input_data, parameters)

        if create_result.get("status") != "success":
            return create_result

        task_id = create_result["task_id"]

        return {
            "status": "success",
            "data": {
                "task_id": task_id,
                "task_status": create_result["task_status"],
                "model": model,
                "prompt": prompt,
                "image_url": image_url,
                "message": "Video generation started. It will take 1-5 minutes to complete. Use get_video_status with this task_id to check progress.",
            },
        }

    @with_cache(ttl_seconds=10)
    @with_retry(max_retries=3)
    async def get_video_status(self, task_id: str) -> Dict[str, Any]:
        """Check status of video generation task"""
        logger.info(f"Checking status for task: {task_id}")

        result = await self._get_task_result(task_id)

        if result.get("status") != "success":
            return result

        data = result["data"]
        output = data.get("output", {})
        task_status = output.get("task_status")

        logger.info(f"Task {task_id} status: {task_status}")

        if task_status == "SUCCEEDED":
            video_url = output.get("video_url")
            try:
                r2_preview_url = await self._download_and_upload_to_r2(video_url, task_id)
            except Exception as e:
                logger.error(f"Failed to upload to R2: {e}", exc_info=True)
                r2_preview_url = None

            response_data = {
                "task_id": task_id,
                "task_status": task_status,
                "video_url": video_url,
                "task_metrics": data.get("usage", {}),
                "message": "Video generation completed successfully!",
            }

            if r2_preview_url:
                response_data["r2_preview_url"] = r2_preview_url

            return {
                "status": "success",
                "data": response_data,
            }
        elif task_status == "FAILED":
            error_msg = output.get("message", "Video generation failed")
            logger.error(f"Task {task_id} failed: {error_msg}")
            return {"status": "error", "error": f"Video generation failed: {error_msg}"}
        elif task_status in ["PENDING", "RUNNING"]:
            return {
                "status": "success",
                "data": {
                    "task_id": task_id,
                    "task_status": task_status,
                    "message": "Video is still being generated. Please check again in 1-2 minutes.",
                },
            }
        else:
            return {"status": "error", "error": f"Unknown task status: {task_status}"}

    async def _handle_tool_logic(
        self, tool_name: str, function_args: dict, session_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        logger.info(f"Handling tool call: {tool_name} with args: {function_args}")

        tool_config = {
            "text_to_video_480p_5s": ("text_to_video", "wan2.2-t2v-plus", "832*480", False, 5),
            "text_to_video_with_audio_480p_5s": ("text_to_video", "wan2.5-t2v-preview", "832*480", True, 5),
            "image_to_video_plus_480p_5s": ("image_to_video", "wan2.2-i2v-plus", "480P", False, 5),
            "image_to_video_flash_480p_5s": ("image_to_video", "wan2.2-i2v-flash", "480P", False, 5),
            "image_to_video_with_audio_480p_5s": ("image_to_video", "wan2.5-i2v-preview", "480P", True, 5),
        }

        if tool_name in tool_config:
            method_type, model, resolution_or_size, audio, duration = tool_config[tool_name]
            prompt = function_args.get("prompt")
            if not prompt:
                return {"error": "Missing 'prompt' parameter"}

            prompt_extend = function_args.get("prompt_extend", True)

            if method_type == "text_to_video":
                result = await self.text_to_video(prompt, model, prompt_extend, resolution_or_size, audio, duration)
            else:
                image_url = function_args.get("image_url")
                if not image_url:
                    return {"error": "Missing 'image_url' parameter"}
                result = await self.image_to_video(
                    prompt, image_url, model, prompt_extend, resolution_or_size, audio, duration
                )

        elif tool_name == "get_video_status":
            task_id = function_args.get("task_id")
            if not task_id:
                return {"error": "Missing 'task_id' parameter"}

            result = await self.get_video_status(task_id)

        else:
            return {"error": f"Unsupported tool: {tool_name}"}

        if errors := self._handle_error(result):
            return errors

        return result

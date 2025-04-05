import logging
import os
import random
from pathlib import Path
from typing import List

import yaml

from ..config import PromptConfig

logger = logging.getLogger(__name__)


class PersonalityProvider:
    """Manages agent personality and prompt configurations"""

    def __init__(self, config_path: str = None):
        """
        Initialize with optional custom config path
        Args:
            config_path: Optional path to custom prompts.yaml
        """
        self.prompt_config = PromptConfig(config_path)

        # If custom path provided but not found in PromptConfig, try loading directly
        if config_path and not os.path.exists(self.prompt_config.config_path):
            custom_path = Path(config_path)
            if custom_path.exists():
                try:
                    with open(custom_path, "r", encoding="utf-8") as f:
                        custom_config = yaml.safe_load(f)
                        self.prompt_config.config.update(custom_config)
                        logger.info(f"Loaded custom personality config from {config_path}")
                except Exception as e:
                    logger.error(f"Failed to load custom config from {config_path}: {str(e)}")

    def get_system_prompt(self, workflow_type: str = "standard") -> str:
        """Get the appropriate system prompt"""
        return self.prompt_config.get_system_prompt()

    def get_name(self) -> str:
        """Get the agent's name"""
        return self.prompt_config.config.get("character", {}).get("name", "Assistant")

    def get_basic_settings(self) -> List[str]:
        """Get basic personality settings"""
        return self.prompt_config.get_basic_settings()

    def get_interaction_styles(self) -> List[str]:
        """Get interaction style settings"""
        return self.prompt_config.get_interaction_styles()

    def get_formatted_personality(self, workflow_type: str = "standard") -> str:
        """Get formatted personality string for prompts"""
        # Get base system prompt
        system_prompt = self.prompt_config.get_system_prompt()

        # Add random selection of traits
        basic_options = random.sample(self.get_basic_settings(), min(2, len(self.get_basic_settings())))
        style_options = random.sample(self.get_interaction_styles(), min(2, len(self.get_interaction_styles())))

        traits_prompt = "\n\nUse the following settings as part of your personality and voice: "
        traits_prompt += " ".join(basic_options) + " " + " ".join(style_options)

        return system_prompt + traits_prompt

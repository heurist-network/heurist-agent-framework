import yaml
import logging
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)

class PromptConfig:
    _instance: Optional['PromptConfig'] = None
    
    def __new__(cls, config_path: str = None):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, config_path: str = None):
        if self._initialized:
            return
            
        if config_path is None:
            project_root = Path(__file__).parent.parent
            config_path = project_root / "config" / "prompts.yaml"
            logger.info(f"Using config file: {config_path}")
        
        self.config_path = Path(config_path)
        self.config = self._load_config()
        self._initialized = True

    def _load_config(self) -> dict:
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            logger.error(f"Config file not found at {self.config_path}")
            raise
        except Exception as e:
            logger.error(f"Error loading config: {str(e)}")
            raise

    def get_system_prompt(self) -> str:
        return self.config['system']['base']

    def get_basic_settings(self) -> list:
        return self.config['character']['basic_settings']

    def get_interaction_styles(self) -> list:
        return self.config['character']['interaction_styles']

    def get_basic_prompt_template(self) -> str:
        return self.config['templates']['basic_prompt']

    def get_tweet_instruction_template(self) -> str:
        return self.config['templates']['tweet_instruction']

    def get_context_twitter_template(self) -> str:
        return self.config['templates']['context_twitter']

    def get_social_reply_template(self) -> str:
        return self.config['templates']['social_reply']

    def get_tweet_ideas(self) -> list:
        return self.config['tweet_ideas']['options']
    
    def get_twitter_rules(self) -> str:
        return self.config['rules']['twitter']

    def get_telegram_rules(self) -> str:
        return self.config['rules']['telegram']

    def get_social_reply_filter(self) -> str:
        return self.config['rules']['social_reply_filter']

    def get_template_image_prompt(self) -> str:
        return self.config['image_rules']['template_image_prompt']
    
    def get_name(self) -> str:
        return self.config['character']['name']
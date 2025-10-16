# agents/job_agents/base_agent.py

import os
import json
import logging
from typing import Dict, List, Any, Optional
from pathlib import Path

# Import all the different AI model providers we might use
from langchain_community.llms import HuggingFaceHub
from langchain_groq import ChatGroq
from langchain_anthropic import ChatAnthropic

# Set up basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class BaseJobAgent:
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.data_dir = Path("data")
        self.data_dir.mkdir(exist_ok=True)
        
        self.config = self._load_config()
        self.provider = self.config.get("active_provider")
        
        if not self.provider:
            raise ValueError("'active_provider' not specified in config.json")
            
        self.llm = self._initialize_llm()

    def _load_config(self) -> Dict[str, Any]:
        config_path = Path("config.json")
        if not config_path.exists():
            raise FileNotFoundError("config.json not found in the project root directory.")
        try:
            with open(config_path, "r") as f:
                return json.load(f)
        except Exception as e:
            self.logger.error(f"Error loading or parsing config.json: {e}")
            raise

    def _initialize_llm(self):
        provider_config = self.config.get("providers", {}).get(self.provider)
        if not provider_config:
            raise ValueError(f"Configuration for provider '{self.provider}' not found in config.json")

        self.logger.info(f"Initializing LLM with provider: {self.provider}")

        if self.provider == "huggingface":
            if not os.getenv("HUGGINGFACEHUB_API_TOKEN"):
                raise ValueError("HUGGINGFACEHUB_API_TOKEN not found in .env file")
            return HuggingFaceHub(**provider_config)
        elif self.provider == "groq":
            if not os.getenv("GROQ_API_KEY"):
                raise ValueError("GROQ_API_KEY not found in .env file")
            return ChatGroq(**provider_config)
        elif self.provider == "anthropic":
            if not os.getenv("ANTHROPIC_API_KEY"):
                raise ValueError("ANTHROPIC_API_KEY not found in .env file")
            return ChatAnthropic(**provider_config)
        else:
            raise ValueError(f"Unsupported provider: '{self.provider}' in config.json.")

    def get_completion(self, messages: List) -> str:
        try:
            response = self.llm.invoke(messages)
            return getattr(response, 'content', response)
        except Exception as e:
            self.logger.error(f"Error getting completion from {self.provider}: {e}")
            raise

    def save_json(self, data: Dict[str, Any], filename: str) -> None:
        output_path = self.data_dir / filename
        try:
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            self.logger.info(f"Successfully saved data to {output_path}")
        except Exception as e:
            self.logger.error(f"Error saving data to {output_path}: {e}")
            raise

    def load_json(self, filename: str) -> Optional[Dict[str, Any]]:
        input_path = self.data_dir / filename
        if not input_path.exists(): return None
        try:
            with open(input_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            self.logger.error(f"Error loading data from {input_path}: {e}")
            raise
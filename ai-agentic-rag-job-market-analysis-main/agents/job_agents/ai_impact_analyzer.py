# agents/job_agents/ai_impact_analyzer.py

import logging
import json
from typing import List, Dict
from .base_agent import BaseJobAgent

logger = logging.getLogger(__name__)

class AIImpactAnalyzerAgent(BaseJobAgent):
    def __init__(self):
        super().__init__()
        logger.info("AIImpactAnalyzerAgent initialized.")

    def analyze(self, job_data: List[Dict]) -> Dict:
        logger.info("Analyzing the impact of AI on job roles...")
        
        prompt = f"""
        Analyze the provided job descriptions to identify the impact of AI.
        Based on the {len(job_data)} jobs, answer the following:
        1. Which roles are most affected by AI skills (like Generative AI, LLMs)?
        2. What are the most commonly requested AI-specific tools or platforms?
        3. Provide a summary of how AI is transforming the roles in this dataset.
        """
        
        try:
            analysis_str = self.get_completion(prompt)
            analysis_dict = {"ai_impact_summary": analysis_str}
            self.save_json(analysis_dict, "ai_impact.json")
            logger.info("AI impact analysis completed and saved.")
            return analysis_dict
        except Exception as e:
            logger.error(f"Failed during AI impact analysis: {e}", exc_info=True)
            return {"error": "Failed to perform AI impact analysis."}
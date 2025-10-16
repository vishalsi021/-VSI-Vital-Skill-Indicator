# agents/job_agents/market_reporter.py

import logging
import json
from typing import List, Dict
from .base_agent import BaseJobAgent

logger = logging.getLogger(__name__)

class MarketReporterAgent(BaseJobAgent):
    def __init__(self):
        super().__init__()
        logger.info("MarketReporterAgent initialized.")

    def generate_report(self, job_data: List[Dict], tech_analysis: Dict) -> Dict:
        logger.info("Generating market trend report...")
        
        prompt = f"""
        Based on the provided job data and technology analysis, generate a market report.
        Focus on salary trends, remote work opportunities, and required experience levels.

        Technology Analysis Summary: {json.dumps(tech_analysis, indent=2)}
        Number of Jobs Analyzed: {len(job_data)}

        Generate a summary of the overall job market trends.
        """
        
        try:
            report_str = self.get_completion(prompt)
            report_dict = {"market_summary": report_str}
            self.save_json(report_dict, "market_report.json")
            logger.info("Market report generated and saved.")
            return report_dict
        except Exception as e:
            logger.error(f"Failed to generate market report: {e}", exc_info=True)
            return {"error": "Failed to generate market report."}
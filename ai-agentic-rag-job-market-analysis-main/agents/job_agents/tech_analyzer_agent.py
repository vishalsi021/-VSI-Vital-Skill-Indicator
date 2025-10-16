# agents/job_agents/tech_analyzer_agent.py
import logging
import json
from typing import List, Dict
from .base_agent import BaseJobAgent
from .rag_store import JobMarketRAGStore

logger = logging.getLogger(__name__)

class TechAnalyzerAgent(BaseJobAgent):
    def __init__(self):
        super().__init__()
        self.rag_store = JobMarketRAGStore(llm=self.llm)
        logger.info("TechAnalyzerAgent initialized.")

    def analyze(self, job_data: List[Dict]) -> Dict:
        logger.info("Starting technology analysis using the RAG store...")
        
        self.rag_store.add_jobs(job_data)

        query = """
        Based on all the provided job descriptions, analyze the technology landscape.
        Identify the following:
        1. The top 10 most mentioned programming languages.
        2. The top 10 most mentioned libraries or frameworks.
        3. The top 5 most mentioned cloud platforms (like AWS, Azure, GCP).
        Provide the result as a clear, structured summary.
        """
        
        try:
            analysis_result_str = self.rag_store.query(query)
            
            try:
                if "```json" in analysis_result_str:
                    analysis_result_str = analysis_result_str.split("```json")[1].split("```")[0]
                analysis_result_dict = json.loads(analysis_result_str)
            except (json.JSONDecodeError, IndexError):
                logger.warning("Could not parse LLM output as JSON, saving as raw string.")
                analysis_result_dict = {"analysis_summary": analysis_result_str}
            
            self.save_json(analysis_result_dict, "tech_analysis.json")
            
            logger.info("Technology analysis completed and saved to tech_analysis.json.")
            return analysis_result_dict
        except Exception as e:
            logger.error(f"An error occurred during technology analysis: {e}", exc_info=True)
            return {"error": "Failed to perform technology analysis."}
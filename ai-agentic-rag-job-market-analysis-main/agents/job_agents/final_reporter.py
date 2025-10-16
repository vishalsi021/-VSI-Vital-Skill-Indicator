# agents/job_agents/final_reporter.py

import logging
from .base_agent import BaseJobAgent

# Each file gets its own logger
logger = logging.getLogger(__name__)

class FinalReporterAgent(BaseJobAgent):
    """
    An agent that synthesizes all previous analyses into a final,
    cohesive report. It inherits the configured LLM from BaseJobAgent.
    """

    def __init__(self):
        """Initializes the agent, automatically getting the LLM from the base class."""
        super().__init__()
        logger.info("FinalReporterAgent initialized.")

    def generate_final_report(self) -> str:
        """
        Loads all partial analysis files and uses the LLM to generate a
        comprehensive final report.
        """
        logger.info("Generating the final comprehensive report...")

        # Load the data from the previous agent steps
        tech_analysis = self.load_json("tech_analysis.json")
        market_report = self.load_json("market_report.json")
        ai_impact = self.load_json("ai_impact.json")

        if not all([tech_analysis, market_report, ai_impact]):
            error_msg = "One or more analysis files are missing. Cannot generate final report."
            logger.error(error_msg)
            return error_msg

        # Create a detailed prompt for the LLM
        prompt = f"""
        You are a professional job market analyst. Based on the following data, create a comprehensive final report.
        The report should have an executive summary, detailed sections for each analysis, and actionable advice for job seekers.

        **Technology Analysis Data:**
        {tech_analysis}

        **Market Trends Data:**
        {market_report}

        **AI Impact Analysis Data:**
        {ai_impact}

        ---
        Generate the full, well-structured markdown report now.
        """

        try:
            # Use the get_completion method inherited from BaseJobAgent
            final_report_content = self.get_completion(prompt)

            # Save the final report as a markdown file
            report_path = self.data_dir.parent / "reports" / "final_report.md"
            report_path.parent.mkdir(exist_ok=True)
            with open(report_path, "w", encoding="utf-8") as f:
                f.write(final_report_content)

            logger.info(f"Final report saved successfully to {report_path}")
            return final_report_content
        except Exception as e:
            logger.error(f"Failed to generate final report: {e}")
            return "Error: Could not generate the final report."
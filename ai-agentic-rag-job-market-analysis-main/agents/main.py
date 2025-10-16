# agents/main.py

import logging
import argparse
from dotenv import load_dotenv

# Import all the professional agent classes we have perfected
from .job_agents.job_data_collector_agent import JobDataCollectorAgent
from .job_agents.tech_analyzer_agent import TechAnalyzerAgent
from .job_agents.market_reporter import MarketReporterAgent
from .job_agents.ai_impact_analyzer import AIImpactAnalyzerAgent
from .job_agents.final_reporter import FinalReporterAgent

# --- Basic Setup ---
# Load the .env file to make API keys available
load_dotenv()

# Configure logging to show progress
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def run_full_workflow(force_new_collection: bool):
    """
    Runs the entire pipeline from data collection to final report.
    """
    logger.info("--- Starting Full Job Market Analysis Workflow ---")

    # 1. Initialize all agents. They now configure themselves automatically.
    collector = JobDataCollectorAgent()
    tech_analyzer = TechAnalyzerAgent()
    market_reporter = MarketReporterAgent()
    ai_impact_analyzer = AIImpactAnalyzerAgent()
    final_reporter = FinalReporterAgent()

    # 2. Step 1: Collect Job Data
    logger.info(">>> STEP 1: Collecting Job Data...")
    job_data = collector.collect_jobs(force_new=force_new_collection)
    if not job_data:
        logger.error("Failed to collect job data. Stopping workflow.")
        return

    # 3. Step 2: Analyze Technology Requirements
    logger.info(">>> STEP 2: Analyzing Technology Trends...")
    tech_analysis = tech_analyzer.analyze(job_data)

    # 4. Step 3: Generate Market Report
    logger.info(">>> STEP 3: Generating Market Report...")
    market_report = market_reporter.generate_report(job_data, tech_analysis)

    # 5. Step 4: Analyze AI's Impact
    logger.info(">>> STEP 4: Analyzing AI Impact...")
    ai_impact = ai_impact_analyzer.analyze(job_data)

    # 6. Step 5: Generate the Final Comprehensive Report
    logger.info(">>> STEP 5: Generating Final Report...")
    final_report = final_reporter.generate_final_report()
    
    logger.info("--- Workflow Completed Successfully! ---")
    logger.info("Final report is available in the 'reports' folder.")

def run_report_only_workflow():
    """
    Skips all analysis and just regenerates the final report from existing data files.
    """
    logger.info("--- Starting Report-Only Workflow ---")
    final_reporter = FinalReporterAgent()
    final_reporter.generate_final_report()
    logger.info("--- Report Generation Completed Successfully! ---")
    logger.info("Final report has been updated in the 'reports' folder.")


def main():
    """
    Main entry point to run the workflow based on command-line arguments.
    """
    # Set up arguments to allow for options like --force-new
    parser = argparse.ArgumentParser(description="Run the job market analysis workflow.")
    parser.add_argument(
        "--force-new",
        action="store_true",
        help="Force re-collection of job data from SerpAPI, ignoring any cached data."
    )
    parser.add_argument(
        "--report-only",
        action="store_true",
        help="Only regenerate the final report from existing analysis files."
    )
    args = parser.parse_args()

    try:
        if args.report_only:
            run_report_only_workflow()
        else:
            run_full_workflow(force_new_collection=args.force_new)
    except Exception as e:
        logger.error(f"An unexpected error occurred during the workflow: {e}", exc_info=True)

if __name__ == "__main__":
    main()
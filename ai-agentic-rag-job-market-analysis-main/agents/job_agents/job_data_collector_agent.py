# agents/job_agents/job_data_collector_agent.py

import os
import time
import logging
from typing import Dict, List

# Make sure you have the correct library installed: pip install google-search-results
from serpapi import GoogleSearch

from .base_agent import BaseJobAgent

# Set up the logger for this specific file, which is the correct practice.
logger = logging.getLogger(__name__)

class JobDataCollectorAgent(BaseJobAgent):
    """
    A specialized agent for collecting job data using SerpAPI.
    It reads search parameters from config.json and inherits the LLM
    and file-handling capabilities from the BaseJobAgent.
    """

    def __init__(self):
        """
        Initializes the collector agent. It automatically inherits the LLM
        and loads its own required API key from the .env file.
        """
        # This properly initializes the BaseJobAgent, which reads config.json
        super().__init__()
        
        # Load the SerpAPI key from the .env file and store it.
        self.serpapi_key = os.getenv("SERPAPI_API_KEY")
        if not self.serpapi_key:
            raise ValueError("SERPAPI_API_KEY not found in your .env file")
            
        logger.info("JobDataCollectorAgent initialized successfully.")

    def _search_api(self, query: str, location: str) -> List[Dict]:
        """
        Private method to perform a single search query against the SerpAPI.
        """
        params = {
            "api_key": self.serpapi_key,
            "engine": "google_jobs",
            "q": query,
            "location": location,
            "hl": "en"
        }
        try:
            search = GoogleSearch(params)
            results = search.get_dict()
            jobs = results.get("jobs_results", [])
            logger.info(f"Found {len(jobs)} jobs for query '{query}' in '{location}'")
            return jobs
        except Exception as e:
            logger.error(f"Error searching for '{query}' in '{location}': {e}")
            return []

    def collect_jobs(self, force_new: bool = False) -> List[Dict]:
        """
        The main method to collect job data. It orchestrates the entire search process.
        It uses cached data from 'data/job_data.json' unless 'force_new' is True.
        """
        logger.info("Starting job collection process...")
        
        # Check for cached data first. The load_json method comes from BaseJobAgent.
        cached_data = self.load_json("job_data.json")
        if cached_data and not force_new:
            logger.info(f"Using cached data. Found {len(cached_data)} jobs in job_data.json.")
            return cached_data

        logger.info("Force flag is on or no cache found. Collecting new data from SerpAPI.")
        
        # Load search parameters from the config file we inherited from BaseJobAgent
        search_params = self.config.get("search_parameters", {})
        roles = search_params.get("roles", [])
        locations = search_params.get("locations", [])
        
        if not roles or not locations:
            raise ValueError("Search 'roles' or 'locations' not defined in your config.json file")

        all_jobs = []
        unique_jobs = set()  # Use a set to efficiently track and prevent duplicate jobs

        for role in roles:
            for location in locations:
                jobs_from_api = self._search_api(query=role, location=location)
                
                for job in jobs_from_api:
                    # Create a unique identifier to avoid duplicates based on company, title, and location
                    job_id = (job.get("company_name"), job.get("title"), job.get("location"))
                    
                    if job_id not in unique_jobs:
                        unique_jobs.add(job_id)
                        all_jobs.append(job)
                
                # A small delay to be respectful to the API and avoid rate limits
                time.sleep(1)

        logger.info(f"Finished collection. Found {len(all_jobs)} unique jobs in total.")
        
        # Save the newly collected data using the method from BaseJobAgent
        if all_jobs:
            self.save_json(all_jobs, "job_data.json")
            
        return all_jobs
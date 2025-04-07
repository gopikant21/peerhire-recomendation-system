"""
Sample Data Manager
- Loads and provides access to generated sample data
- Offers utility functions for data access
"""

import os
import json
from typing import List, Dict, Any, Optional

class DataManager:
    def __init__(self, data_dir: str = "data"):
        """Initialize the data manager with data directory"""
        self.data_dir = data_dir
        self.freelancers = []
        self.jobs = []
        self._load_data()
    
    def _load_data(self) -> None:
        """Load data from JSON files"""
        # Path to freelancers and jobs JSON files
        freelancers_path = os.path.join(self.data_dir, "freelancers.json")
        jobs_path = os.path.join(self.data_dir, "jobs.json")
        
        # Check if files exist
        if not os.path.exists(freelancers_path) or not os.path.exists(jobs_path):
            print("Data files not found. Generating new data...")
            from data.data_generator import DataGenerator
            generator = DataGenerator()
            generator.save_data(self.data_dir)
        
        # Load data from files
        try:
            with open(freelancers_path, "r") as f:
                self.freelancers = json.load(f)
            
            with open(jobs_path, "r") as f:
                self.jobs = json.load(f)
            
            print(f"Loaded {len(self.freelancers)} freelancers and {len(self.jobs)} jobs.")
        except Exception as e:
            print(f"Error loading data: {e}")
            self.freelancers = []
            self.jobs = []
    
    def get_freelancers(self) -> List[Dict[str, Any]]:
        """Get all freelancers"""
        return self.freelancers
    
    def get_jobs(self) -> List[Dict[str, Any]]:
        """Get all jobs"""
        return self.jobs
    
    def get_freelancer_by_id(self, freelancer_id: str) -> Optional[Dict[str, Any]]:
        """Get freelancer by ID"""
        for freelancer in self.freelancers:
            if freelancer["freelancer_id"] == freelancer_id:
                return freelancer
        return None
    
    def get_job_by_id(self, job_id: str) -> Optional[Dict[str, Any]]:
        """Get job by ID"""
        for job in self.jobs:
            if job["job_id"] == job_id:
                return job
        return None
    
    def get_freelancers_by_skill(self, skill: str) -> List[Dict[str, Any]]:
        """Get freelancers with specific skill"""
        return [f for f in self.freelancers if skill in f["skills"]]
    
    def get_freelancers_by_experience_level(self, level: str) -> List[Dict[str, Any]]:
        """Get freelancers with specific experience level"""
        return [f for f in self.freelancers if f["experience_level"] == level]
    
    def get_freelancers_by_hourly_rate(self, min_rate: float, max_rate: float) -> List[Dict[str, Any]]:
        """Get freelancers within hourly rate range"""
        return [f for f in self.freelancers if min_rate <= f["hourly_rate"] <= max_rate]

# Create a singleton instance for easy access
data_manager = DataManager()
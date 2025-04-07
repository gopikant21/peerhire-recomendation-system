"""
Data Generator for Freelancer Recommendation System
- Generates dummy data for freelancers and job postings
- Used for training and testing the recommendation model
"""

import random
import json
import os
from datetime import datetime, timedelta
from typing import List, Dict, Any

# Define constants
SKILL_CATEGORIES = [
    "Programming Languages", "Web Development", "Mobile Development",
    "Data Science", "Design", "Writing", "Marketing", "SEO"
]

SKILLS = {
    "Programming Languages": ["Python", "Java", "JavaScript", "C++", "Ruby", "Go", "PHP", "Swift", "Kotlin"],
    "Web Development": ["React", "Angular", "Vue.js", "Django", "Flask", "Node.js", "Express", "HTML", "CSS", "WordPress"],
    "Mobile Development": ["Android", "iOS", "React Native", "Flutter", "Xamarin", "Ionic"],
    "Data Science": ["Machine Learning", "Deep Learning", "TensorFlow", "PyTorch", "Data Analysis", "SQL", "NoSQL", "Power BI", "Tableau"],
    "Design": ["UI/UX", "Graphic Design", "Adobe Photoshop", "Illustrator", "Figma", "Sketch", "InDesign"],
    "Writing": ["Content Writing", "Copywriting", "Technical Writing", "Editing", "Proofreading"],
    "Marketing": ["Social Media", "Email Marketing", "Content Marketing", "SEO", "PPC", "Google Ads"],
    "SEO": ["On-page SEO", "Off-page SEO", "Keyword Research", "Link Building", "Local SEO"]
}

COUNTRIES = ["USA", "UK", "Canada", "Australia", "Germany", "France", "India", "Singapore", "Brazil", "Japan"]

class DataGenerator:
    def __init__(self, seed: int = 42):
        """Initialize the data generator with a seed for reproducibility"""
        random.seed(seed)
        self.freelancer_ids = []
        self.client_ids = []
    
    def generate_freelancer_id(self) -> str:
        """Generate a unique freelancer ID"""
        freelancer_id = f"F{len(self.freelancer_ids) + 1:04d}"
        self.freelancer_ids.append(freelancer_id)
        return freelancer_id
    
    def generate_client_id(self) -> str:
        """Generate a unique client ID"""
        client_id = f"C{len(self.client_ids) + 1:04d}"
        self.client_ids.append(client_id)
        return client_id
    
    def generate_skills(self, num_skills: int = None) -> List[str]:
        """Generate a list of skills for a freelancer or job"""
        if num_skills is None:
            num_skills = random.randint(3, 8)
        
        # Select random skill categories
        categories = random.sample(SKILL_CATEGORIES, min(random.randint(1, 4), len(SKILL_CATEGORIES)))
        
        # Select skills from each category
        skills = []
        for category in categories:
            category_skills = SKILLS[category]
            num_category_skills = min(random.randint(1, 3), len(category_skills))
            skills.extend(random.sample(category_skills, num_category_skills))
        
        # Ensure we have the desired number of skills
        if len(skills) > num_skills:
            skills = random.sample(skills, num_skills)
        
        return skills
    
    def generate_freelancers(self, num_freelancers: int = 100) -> List[Dict[str, Any]]:
        """Generate a list of freelancer profiles"""
        freelancers = []
        for _ in range(num_freelancers):
            # Generate basic info
            freelancer_id = self.generate_freelancer_id()
            skills = self.generate_skills()
            hourly_rate = round(random.uniform(15, 150), 2)
            
            # Generate experience level
            experience_years = random.randint(1, 15)
            if experience_years <= 2:
                experience_level = "Entry"
            elif experience_years <= 5:
                experience_level = "Intermediate"
            elif experience_years <= 10:
                experience_level = "Advanced"
            else:
                experience_level = "Expert"
            
            # Generate completed projects
            num_projects = random.randint(1, 30)
            
            # Generate ratings
            ratings = [random.randint(3, 5) for _ in range(num_projects)]
            avg_rating = round(sum(ratings) / len(ratings), 1) if ratings else 0
            
            # Generate past projects
            projects = []
            for i in range(num_projects):
                project_skills = random.sample(skills, min(random.randint(1, 4), len(skills)))
                project = {
                    "project_id": f"P{i+1:04d}_{freelancer_id}",
                    "client_id": random.choice(self.client_ids) if self.client_ids else self.generate_client_id(),
                    "title": f"Project {i+1} for {freelancer_id}",
                    "skills": project_skills,
                    "duration_days": random.randint(5, 90),
                    "budget": round(random.uniform(100, 5000), 2),
                    "rating": ratings[i] if i < len(ratings) else 0
                }
                projects.append(project)
            
            # Create the freelancer profile
            freelancer = {
                "freelancer_id": freelancer_id,
                "name": f"Freelancer {freelancer_id}",
                "country": random.choice(COUNTRIES),
                "skills": skills,
                "hourly_rate": hourly_rate,
                "experience_years": experience_years,
                "experience_level": experience_level,
                "completed_projects": num_projects,
                "avg_rating": avg_rating,
                "availability": random.choice(["Full-time", "Part-time", "Weekends"]),
                "past_projects": projects
            }
            
            freelancers.append(freelancer)
        
        return freelancers
    
    def generate_job_postings(self, num_jobs: int = 50) -> List[Dict[str, Any]]:
        """Generate a list of job postings"""
        jobs = []
        for i in range(num_jobs):
            # Generate job skills
            skills = self.generate_skills(random.randint(2, 6))
            
            # Generate job budget
            budget_type = random.choice(["hourly", "fixed"])
            if budget_type == "hourly":
                budget = {
                    "type": "hourly",
                    "min_rate": round(random.uniform(10, 50), 2),
                    "max_rate": round(random.uniform(50, 200), 2)
                }
            else:
                budget = {
                    "type": "fixed",
                    "amount": round(random.uniform(100, 10000), 2)
                }
            
            # Generate timeline
            duration_days = random.randint(7, 180)
            
            # Create the job posting
            job = {
                "job_id": f"J{i+1:04d}",
                "client_id": random.choice(self.client_ids) if self.client_ids else self.generate_client_id(),
                "title": f"Job Posting {i+1}",
                "description": f"This is job posting {i+1} description that requires specific skills.",
                "skills_required": skills,
                "budget": budget,
                "experience_level": random.choice(["Entry", "Intermediate", "Advanced", "Expert"]),
                "timeline_days": duration_days,
                "created_at": (datetime.now() - timedelta(days=random.randint(0, 30))).isoformat()
            }
            
            jobs.append(job)
        
        return jobs

    def save_data(self, output_dir: str = "data") -> None:
        """Generate and save all dummy data"""
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate data
        freelancers = self.generate_freelancers(100)
        jobs = self.generate_job_postings(50)
        
        # Save data to JSON files
        with open(os.path.join(output_dir, "freelancers.json"), "w") as f:
            json.dump(freelancers, f, indent=2)
        
        with open(os.path.join(output_dir, "jobs.json"), "w") as f:
            json.dump(jobs, f, indent=2)
        
        print(f"Generated {len(freelancers)} freelancers and {len(jobs)} job postings.")

if __name__ == "__main__":
    # Generate and save data
    generator = DataGenerator(seed=42)
    generator.save_data()
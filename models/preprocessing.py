"""
Preprocessing Module
- Transforms raw freelancer and job data into feature vectors
- Prepares data for similarity calculation and matching
"""

import numpy as np
from typing import List, Dict, Any, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MinMaxScaler

class FreelancerJobPreprocessor:
    def __init__(self):
        """Initialize the preprocessor with necessary vectorizers and scalers"""
        # Vectorizers for text features
        self.skill_vectorizer = TfidfVectorizer()
        
        # Scalers for numerical features
        self.rate_scaler = MinMaxScaler()
        self.experience_scaler = MinMaxScaler()
        self.rating_scaler = MinMaxScaler()
        
        # Experience level mapping (for easier comparison)
        self.experience_level_map = {
            "Entry": 1,
            "Intermediate": 2,
            "Advanced": 3,
            "Expert": 4
        }
        
        # Weights for different features
        self.feature_weights = {
            "skills": 0.5,            # 50% importance
            "experience": 0.2,        # 20% importance
            "hourly_rate": 0.15,      # 15% importance
            "rating": 0.15            # 15% importance
        }
        
        # Flag to check if the preprocessor is trained
        self.is_trained = False
    
    def _preprocess_skills(self, skills: List[str]) -> str:
        """Convert skills list to a space-separated string for vectorization"""
        return " ".join(skills).lower()
    
    def fit(self, freelancers: List[Dict[str, Any]]) -> None:
        """Fit the vectorizers and scalers on freelancer data"""
        # Extract skills for fitting the skill vectorizer
        skills_text = [self._preprocess_skills(freelancer["skills"]) for freelancer in freelancers]
        self.skill_vectorizer.fit(skills_text)
        
        # Extract numerical features for fitting scalers
        hourly_rates = np.array([freelancer["hourly_rate"] for freelancer in freelancers]).reshape(-1, 1)
        self.rate_scaler.fit(hourly_rates)
        
        experience_years = np.array([freelancer["experience_years"] for freelancer in freelancers]).reshape(-1, 1)
        self.experience_scaler.fit(experience_years)
        
        ratings = np.array([freelancer["avg_rating"] for freelancer in freelancers]).reshape(-1, 1)
        self.rating_scaler.fit(ratings)
        
        self.is_trained = True
    
    def transform_freelancer(self, freelancer: Dict[str, Any]) -> Dict[str, np.ndarray]:
        """Transform a freelancer profile into feature vectors"""
        if not self.is_trained:
            raise ValueError("Preprocessor must be fitted before transform")
        
        # Transform skills
        skills_text = self._preprocess_skills(freelancer["skills"])
        skills_vector = self.skill_vectorizer.transform([skills_text]).toarray()[0]
        
        # Transform numerical features
        hourly_rate = self.rate_scaler.transform([[freelancer["hourly_rate"]]])[0][0]
        experience_years = self.experience_scaler.transform([[freelancer["experience_years"]]])[0][0]
        experience_level = self.experience_level_map.get(freelancer["experience_level"], 2) / 4  # Normalize to [0,1]
        avg_rating = self.rating_scaler.transform([[freelancer["avg_rating"]]])[0][0]
        
        # Return feature vectors as a dictionary
        return {
            "skills": skills_vector,
            "hourly_rate": hourly_rate,
            "experience_years": experience_years,
            "experience_level": experience_level,
            "avg_rating": avg_rating
        }
    
    def transform_job(self, job: Dict[str, Any]) -> Dict[str, Any]:
        """Transform a job posting into feature vectors and requirements"""
        if not self.is_trained:
            raise ValueError("Preprocessor must be fitted before transform")
        
        # Transform skills
        skills_text = self._preprocess_skills(job["skills_required"])
        skills_vector = self.skill_vectorizer.transform([skills_text]).toarray()[0]
        
        # Transform budget (handle both hourly and fixed)
        budget = job["budget"]
        if budget["type"] == "hourly":
            hourly_rate_min = budget["min_rate"]
            hourly_rate_max = budget["max_rate"]
            hourly_rate_avg = (hourly_rate_min + hourly_rate_max) / 2
            hourly_rate = self.rate_scaler.transform([[hourly_rate_avg]])[0][0]
        else:
            # For fixed budget, we'll use a placeholder value that won't affect matching heavily
            hourly_rate = 0.5  # Middle of the range
        
        # Transform experience level
        experience_level = self.experience_level_map.get(job["experience_level"], 2) / 4  # Normalize to [0,1]
        
        # Return feature vectors and requirements as a dictionary
        return {
            "skills": skills_vector,
            "hourly_rate": hourly_rate,
            "experience_level": experience_level,
            "original_job": job  # Keep original job for reference
        }
    
    def get_feature_names(self) -> Dict[str, List[str]]:
        """Get the feature names for each feature type"""
        return {
            "skills": self.skill_vectorizer.get_feature_names_out().tolist(),
        }
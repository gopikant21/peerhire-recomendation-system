"""
Recommendation Model
- Matches freelancers to jobs based on skills, experience, and budget
- Uses content-based filtering and cosine similarity
"""

import numpy as np
from typing import List, Dict, Any, Tuple
from sklearn.metrics.pairwise import cosine_similarity
from models.preprocessing import FreelancerJobPreprocessor
from data.sample_data import data_manager

class FreelancerRecommendationSystem:
    def __init__(self):
        """Initialize the recommendation system"""
        self.preprocessor = FreelancerJobPreprocessor()
        self.freelancers = []
        self.freelancer_features = []
        self.is_trained = False
    
    def train(self) -> None:
        """Train the recommendation system on available data"""
        # Load freelancers from data manager
        self.freelancers = data_manager.get_freelancers()
        
        # Fit the preprocessor on freelancer data
        self.preprocessor.fit(self.freelancers)
        
        # Transform all freelancers
        self.freelancer_features = [
            {
                "freelancer_id": freelancer["freelancer_id"],
                "features": self.preprocessor.transform_freelancer(freelancer),
                "original_data": freelancer
            }
            for freelancer in self.freelancers
        ]
        
        self.is_trained = True
        print(f"Trained recommendation system on {len(self.freelancers)} freelancers")
    
    def _calculate_skill_similarity(self, job_skills: np.ndarray, freelancer_skills: np.ndarray) -> float:
        """Calculate similarity between job skills and freelancer skills"""
        # Use cosine similarity for skill matching
        if job_skills.sum() == 0 or freelancer_skills.sum() == 0:
            return 0.0
        
        return cosine_similarity([job_skills], [freelancer_skills])[0][0]
    
    def _calculate_budget_compatibility(self, job_budget: float, freelancer_rate: float) -> float:
        """Calculate compatibility between job budget and freelancer rate"""
        # Simple linear compatibility (higher is better, closer to 1)
        # The closer the freelancer's rate is to the job's budget, the higher the score
        return 1.0 - abs(job_budget - freelancer_rate)
    
    def _calculate_experience_compatibility(self, job_req: float, freelancer_exp: float) -> float:
        """Calculate compatibility between job experience requirements and freelancer experience"""
        # If freelancer meets or exceeds job requirements, score is 1.0
        # Otherwise, score decreases linearly
        if freelancer_exp >= job_req:
            return 1.0
        else:
            return freelancer_exp / job_req if job_req > 0 else 0.0
    
    def _calculate_overall_score(self, job_features: Dict[str, Any], freelancer_features: Dict[str, np.ndarray]) -> float:
        """Calculate overall match score between job and freelancer"""
        # Calculate individual feature scores
        skill_score = self._calculate_skill_similarity(
            job_features["skills"], 
            freelancer_features["skills"]
        )
        
        budget_score = self._calculate_budget_compatibility(
            job_features["hourly_rate"],
            freelancer_features["hourly_rate"]
        )
        
        experience_score = self._calculate_experience_compatibility(
            job_features["experience_level"],
            freelancer_features["experience_level"]
        )
        
        # Rating is a standalone score
        rating_score = freelancer_features["avg_rating"]
        
        # Calculate weighted overall score
        weights = self.preprocessor.feature_weights
        overall_score = (
            weights["skills"] * skill_score +
            weights["hourly_rate"] * budget_score +
            weights["experience"] * experience_score +
            weights["rating"] * rating_score
        )
        
        return overall_score
    
    def recommend_freelancers(self, job: Dict[str, Any], top_n: int = 5) -> List[Dict[str, Any]]:
        """Recommend freelancers for a given job"""
        if not self.is_trained:
            self.train()
        
        # Transform job posting
        job_features = self.preprocessor.transform_job(job)
        
        # Calculate match scores for all freelancers
        freelancer_scores = []
        for freelancer_data in self.freelancer_features:
            score = self._calculate_overall_score(job_features, freelancer_data["features"])
            
            freelancer_scores.append({
                "freelancer_id": freelancer_data["freelancer_id"],
                "score": score,
                "freelancer_data": freelancer_data["original_data"]
            })
        
        # Sort by score (descending) and take top N
        freelancer_scores.sort(key=lambda x: x["score"], reverse=True)
        top_freelancers = freelancer_scores[:top_n]
        
        # Format the results
        recommendations = []
        for rank, match in enumerate(top_freelancers):
            recommendation = {
                "rank": rank + 1,
                "freelancer_id": match["freelancer_id"],
                "name": match["freelancer_data"]["name"],
                "match_score": round(match["score"] * 100, 2),  # Convert to percentage
                "skills": match["freelancer_data"]["skills"],
                "hourly_rate": match["freelancer_data"]["hourly_rate"],
                "experience_level": match["freelancer_data"]["experience_level"],
                "completed_projects": match["freelancer_data"]["completed_projects"],
                "avg_rating": match["freelancer_data"]["avg_rating"]
            }
            recommendations.append(recommendation)
        
        return recommendations

# Create singleton instance
recommendation_system = FreelancerRecommendationSystem()
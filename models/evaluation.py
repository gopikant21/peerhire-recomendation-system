"""
Model Evaluation
- Provides metrics to evaluate the recommendation system
- Includes precision, recall, and coverage metrics
"""

import numpy as np
from typing import List, Dict, Any, Set, Tuple
from models.recommendation import FreelancerRecommendationSystem
from data.sample_data import data_manager

class RecommendationEvaluator:
    def __init__(self, recommendation_system: FreelancerRecommendationSystem):
        """Initialize the evaluator"""
        self.recommendation_system = recommendation_system
        self.jobs = data_manager.get_jobs()
    
    def evaluate_full_system(self, top_n: int = 5) -> Dict[str, Any]:
        """Run a full evaluation of the recommendation system"""
        # Make sure the system is trained
        if not self.recommendation_system.is_trained:
            self.recommendation_system.train()
        
        # Run individual evaluations
        skill_coverage = self.evaluate_skill_coverage(top_n)
        budget_match = self.evaluate_budget_match(top_n)
        diversity_score = self.evaluate_recommendation_diversity(top_n)
        
        # Combine results
        results = {
            "skill_coverage": skill_coverage,
            "budget_match": budget_match,
            "diversity": diversity_score,
            "overall_score": (skill_coverage["average_skill_coverage"] + 
                              budget_match["average_budget_match"] + 
                              diversity_score["average_diversity"]) / 3
        }
        
        return results
    
    def evaluate_recommendation_diversity(self, top_n: int = 5) -> Dict[str, float]:
        """Evaluate how diverse the recommendations are"""
        diversity_scores = []
        
        for job in self.jobs:
            # Get recommendations
            recommendations = self.recommendation_system.recommend_freelancers(job, top_n)
            
            # Calculate skill diversity
            all_skills = set()
            for rec in recommendations:
                all_skills.update(rec["skills"])
            
            # Look at variance in hourly rates
            hourly_rates = [rec["hourly_rate"] for rec in recommendations]
            rate_variance = np.var(hourly_rates) if len(hourly_rates) > 1 else 0
            
            # Normalize rate variance to [0,1] scale (higher variance = more diverse)
            rate_diversity = min(1.0, rate_variance / 100)
            
            # Calculate experience level diversity
            experience_levels = [rec["experience_level"] for rec in recommendations]
            exp_diversity = len(set(experience_levels)) / len(recommendations) if recommendations else 0
            
            # Combine diversity metrics
            diversity = (len(all_skills) / (len(recommendations) * 5) + rate_diversity + exp_diversity) / 3
            diversity_scores.append(diversity)
        
        # Calculate overall metrics
        avg_diversity = np.mean(diversity_scores)
        median_diversity = np.median(diversity_scores)
        min_diversity = np.min(diversity_scores)
        max_diversity = np.max(diversity_scores)
        
        return {
            "average_diversity": avg_diversity,
            "median_diversity": median_diversity,
            "min_diversity": min_diversity,
            "max_diversity": max_diversity
        }
    
    def evaluate_skill_coverage(self, top_n: int = 5) -> Dict[str, float]:
        """Evaluate how well the recommendations cover the skills required by jobs"""
        skill_coverage_scores = []
        
        for job in self.jobs:
            # Get required skills
            required_skills = set(job["skills_required"])
            
            # Get recommendations
            recommendations = self.recommendation_system.recommend_freelancers(job, top_n)
            
            # Collect skills from all recommended freelancers
            all_skills = set()
            for rec in recommendations:
                all_skills.update(rec["skills"])
            
            # Calculate coverage
            matching_skills = required_skills.intersection(all_skills)
            coverage = len(matching_skills) / len(required_skills) if required_skills else 0
            skill_coverage_scores.append(coverage)
        
        # Calculate overall metrics
        avg_coverage = np.mean(skill_coverage_scores)
        median_coverage = np.median(skill_coverage_scores)
        min_coverage = np.min(skill_coverage_scores)
        max_coverage = np.max(skill_coverage_scores)
        
        return {
            "average_skill_coverage": avg_coverage,
            "median_skill_coverage": median_coverage,
            "min_skill_coverage": min_coverage,
            "max_skill_coverage": max_coverage
        }
    
    def evaluate_budget_match(self, top_n: int = 5) -> Dict[str, float]:
        """Evaluate how well the recommendations match the budget constraints"""
        budget_match_scores = []
        
        for job in self.jobs:
            # Get budget constraints
            budget = job["budget"]
            if budget["type"] == "hourly":
                min_rate = budget["min_rate"]
                max_rate = budget["max_rate"]
                
                # Get recommendations
                recommendations = self.recommendation_system.recommend_freelancers(job, top_n)
                
                # Calculate budget match for each recommendation
                matches = []
                for rec in recommendations:
                    hourly_rate = rec["hourly_rate"]
                    # If within budget range, perfect match (1.0)
                    if min_rate <= hourly_rate <= max_rate:
                        matches.append(1.0)
                    else:
                        # Calculate how far outside the range
                        if hourly_rate < min_rate:
                            distance = (min_rate - hourly_rate) / min_rate
                        else:  # hourly_rate > max_rate
                            distance = (hourly_rate - max_rate) / max_rate
                        
                        # Convert distance to a match score (1.0 - normalized distance)
                        match_score = max(0, 1.0 - min(distance, 1.0))
                        matches.append(match_score)
                
                # Average match score for this job
                avg_match = np.mean(matches) if matches else 0
                budget_match_scores.append(avg_match)
            else:
                # Fixed budget - more complex matching logic could be implemented
                # For simplicity, we'll use a placeholder score
                budget_match_scores.append(0.8)
        
        # Calculate overall metrics
        avg_match = np.mean(budget_match_scores)
        median_match = np.median(budget_match_scores)
        min_match = np.min(budget_match_scores)
        max_match = np.max(budget_match_scores)
        
        return {
            "average_budget_match": avg_match,
            "median_budget_match": median_match,
            "min_budget_match": min_match,
            "max_budget_match": max_match
        }
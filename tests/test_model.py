"""
Tests for the recommendation model
"""

import pytest
from models.preprocessing import FreelancerJobPreprocessor
from models.recommendation import FreelancerRecommendationSystem
from data.sample_data import data_manager

class TestRecommendationModel:
    """Test cases for the recommendation model"""
    
    def test_preprocessor_initialization(self):
        """Test that the preprocessor initializes correctly"""
        preprocessor = FreelancerJobPreprocessor()
        assert preprocessor is not None
        assert preprocessor.is_trained == False
    
    def test_preprocessor_fit(self):
        """Test that the preprocessor can be fitted on data"""
        preprocessor = FreelancerJobPreprocessor()
        freelancers = data_manager.get_freelancers()
        
        # Ensure we have data
        assert len(freelancers) > 0
        
        # Fit the preprocessor
        preprocessor.fit(freelancers)
        assert preprocessor.is_trained == True
    
    def test_recommendation_system_initialization(self):
        """Test that the recommendation system initializes correctly"""
        system = FreelancerRecommendationSystem()
        assert system is not None
        assert system.is_trained == False
    
    def test_recommendation_system_train(self):
        """Test that the recommendation system can be trained"""
        system = FreelancerRecommendationSystem()
        system.train()
        assert system.is_trained == True
        assert len(system.freelancers) > 0
        assert len(system.freelancer_features) > 0
    
    def test_get_recommendations(self):
        """Test that the system can generate recommendations"""
        system = FreelancerRecommendationSystem()
        system.train()
        
        # Create a sample job
        job = {
            "title": "Test Job",
            "description": "A test job for unit testing",
            "skills_required": ["Python", "Machine Learning", "API Development"],
            "budget": {
                "type": "hourly",
                "min_rate": 20.0,
                "max_rate": 50.0
            },
            "experience_level": "Intermediate",
            "timeline_days": 30
        }
        
        # Get recommendations
        recommendations = system.recommend_freelancers(job, top_n=5)
        
        # Check that we have recommendations
        assert len(recommendations) <= 5
        assert len(recommendations) > 0
        
        # Check recommendation format
        for rec in recommendations:
            assert "freelancer_id" in rec
            assert "match_score" in rec
            assert "skills" in rec
            assert isinstance(rec["match_score"], float)
            assert 0 <= rec["match_score"] <= 100
"""
Tests for the API endpoints
"""

import pytest
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

class TestAPIEndpoints:
    """Test cases for API endpoints"""
    
    def test_health_check(self):
        """Test the health check endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "documentation" in data
    
    def test_recommend_endpoint(self):
        """Test the recommend endpoint"""
        # Create a sample job request
        job_request = {
            "title": "Full Stack Developer",
            "description": "We need a full stack developer for our web application.",
            "skills_required": ["Python", "JavaScript", "React", "Node.js"],
            "budget": {
                "type": "hourly",
                "min_rate": 25.0,
                "max_rate": 60.0
            },
            "experience_level": "Intermediate",
            "timeline_days": 45
        }
        
        # Send request to the API
        response = client.post("/recommend", json=job_request)
        
        # Check response
        assert response.status_code == 200
        data = response.json()
        
        # Validate response structure
        assert "job" in data
        assert "recommendations" in data
        assert "total_matches" in data
        
        # Check job data
        assert data["job"]["title"] == job_request["title"]
        
        # Check recommendations
        recommendations = data["recommendations"]
        assert isinstance(recommendations, list)
        
        # If we have recommendations, check their format
        if recommendations:
            recommendation = recommendations[0]
            assert "freelancer_id" in recommendation
            assert "match_score" in recommendation
            assert "skills" in recommendation
    
    def test_supported_skills_endpoint(self):
        """Test the supported skills endpoint"""
        response = client.get("/supported-skills")
        
        # Check response
        assert response.status_code == 200
        data = response.json()
        
        # Validate response structure
        assert "skills" in data
        assert isinstance(data["skills"], list)
    
    def test_invalid_job_request(self):
        """Test error handling for invalid job request"""
        # Create an invalid job request (missing required fields)
        invalid_job = {
            "title": "Test Job",
            # Missing skills_required and other required fields
        }
        
        # Send request to the API
        response = client.post("/recommend", json=invalid_job)
        
        # Check response
        assert response.status_code == 422  # Unprocessable Entity
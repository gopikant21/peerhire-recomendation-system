"""
API Endpoints
- Defines the API routes and handlers
- Connects the frontend to the recommendation engine
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any

from api.schemas import (
    JobRequest, 
    RecommendationResponse, 
    HealthResponse
)
from models.recommendation import recommendation_system
from models.collaborative_filtering import collaborative_filtering

# Create API router
router = APIRouter()

@router.get("/", response_model=HealthResponse)
async def health_check() -> Dict[str, str]:
    """Health check endpoint"""
    return {
        "status": "ok",
        "version": "1.0.0"
    }

@router.post("/recommend", response_model=RecommendationResponse)
async def recommend_freelancers(
    job_request: JobRequest, 
    client_id: str = None,
    use_collaborative: bool = False,
    cf_weight: float = 0.3
) -> Dict[str, Any]:
    """
    Recommend freelancers for a job
    
    Takes a job posting with requirements and returns the top 5 
    most relevant freelancers based on skills, experience, and budget.
    
    Parameters:
    - job_request: Job details including skills, budget, and timeline
    - client_id: Optional client ID for collaborative filtering enhancement
    - use_collaborative: Whether to enhance results with collaborative filtering
    - cf_weight: Weight for collaborative filtering (0-1)
    """
    try:
        # Ensure the recommendation system is trained
        if not recommendation_system.is_trained:
            recommendation_system.train()
        
        # Convert job request to the format expected by the recommendation system
        job_dict = job_request.dict()
        
        # Get content-based recommendations
        recommendations = recommendation_system.recommend_freelancers(job_dict, top_n=5)
        
        # Enhance with collaborative filtering if requested
        if use_collaborative and client_id:
            # Ensure the collaborative filtering model is trained
            if not collaborative_filtering.is_trained:
                collaborative_filtering.train()
            
            # Enhance recommendations
            recommendations = collaborative_filtering.enhance_recommendations(
                client_id=client_id,
                content_recommendations=recommendations,
                weight_collaborative=cf_weight
            )
        
        # Return recommendations
        return {
            "job": job_request,
            "recommendations": recommendations,
            "total_matches": len(recommendations)
        }
    except Exception as e:
        # Log the error (in a real system, use a proper logger)
        print(f"Error generating recommendations: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to generate recommendations: {str(e)}"
        )

@router.get("/supported-skills")
async def get_supported_skills() -> Dict[str, Any]:
    """Get a list of all skills supported by the system"""
    try:
        # Ensure the recommendation system is trained
        if not recommendation_system.is_trained:
            recommendation_system.train()
        
        # Get feature names from the preprocessor
        feature_names = recommendation_system.preprocessor.get_feature_names()
        
        # Return skills
        return {
            "skills": feature_names.get("skills", [])
        }
    except Exception as e:
        # Log the error
        print(f"Error retrieving skills: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to retrieve skills: {str(e)}"
        )

@router.get("/client/{client_id}/recommendations")
async def get_client_recommendations(client_id: str, top_n: int = 5) -> Dict[str, Any]:
    """
    Get recommendations for a client based on collaborative filtering
    
    Uses the client's past hiring history to recommend freelancers.
    
    Parameters:
    - client_id: Client ID to get recommendations for
    - top_n: Number of recommendations to return
    """
    try:
        # Ensure the collaborative filtering model is trained
        if not collaborative_filtering.is_trained:
            collaborative_filtering.train()
        
        # Get recommendations
        recommendations = collaborative_filtering.recommend_for_client(client_id, top_n)
        
        # Return recommendations
        return {
            "client_id": client_id,
            "recommendations": recommendations,
            "total_matches": len(recommendations)
        }
    except Exception as e:
        # Log the error
        print(f"Error generating client recommendations: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to generate client recommendations: {str(e)}"
        )
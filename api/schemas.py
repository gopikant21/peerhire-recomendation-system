"""
API Schemas
- Pydantic models for API request and response validation
- Defines the structure of input and output data
"""

from typing import List, Dict, Any, Optional, Union
from pydantic import BaseModel, Field

# Budget model for job postings
class Budget(BaseModel):
    type: str = Field(..., description="Budget type: 'hourly' or 'fixed'")
    min_rate: Optional[float] = Field(None, description="Minimum hourly rate (for hourly budgets)")
    max_rate: Optional[float] = Field(None, description="Maximum hourly rate (for hourly budgets)")
    amount: Optional[float] = Field(None, description="Fixed budget amount (for fixed budgets)")

# Job request model
class JobRequest(BaseModel):
    title: str = Field(..., description="Job title")
    description: Optional[str] = Field(None, description="Job description")
    skills_required: List[str] = Field(..., description="List of required skills")
    budget: Budget = Field(..., description="Job budget information")
    experience_level: str = Field(..., description="Required experience level: 'Entry', 'Intermediate', 'Advanced', or 'Expert'")
    timeline_days: int = Field(..., description="Expected timeline in days")

# Freelancer response model
class FreelancerResponse(BaseModel):
    rank: int = Field(..., description="Ranking position")
    freelancer_id: str = Field(..., description="Unique freelancer ID")
    name: str = Field(..., description="Freelancer name")
    match_score: float = Field(..., description="Match score percentage")
    skills: List[str] = Field(..., description="Freelancer skills")
    hourly_rate: float = Field(..., description="Freelancer hourly rate")
    experience_level: str = Field(..., description="Freelancer experience level")
    completed_projects: int = Field(..., description="Number of completed projects")
    avg_rating: float = Field(..., description="Average rating (0-5)")

# Recommendation response model
class RecommendationResponse(BaseModel):
    job: JobRequest = Field(..., description="Original job request")
    recommendations: List[FreelancerResponse] = Field(..., description="List of recommended freelancers")
    total_matches: int = Field(..., description="Total number of potential matches")

# Error response model
class ErrorResponse(BaseModel):
    error: str = Field(..., description="Error message")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional error details")

# Health check response
class HealthResponse(BaseModel):
    status: str = Field(..., description="Service status")
    version: str = Field(..., description="API version")
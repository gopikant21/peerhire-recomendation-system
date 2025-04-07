"""
API Main Application
- FastAPI application setup and configuration
- CORS, middleware, and exception handlers
"""

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from api.endpoints import router

# Create FastAPI application
app = FastAPI(
    title="PeerHire Freelancer Recommendation API",
    description="API for recommending freelancers based on job requirements",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict to specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(router)

# Exception handlers
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle validation errors"""
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": "Validation error",
            "details": exc.errors()
        }
    )

# Root redirect to docs
@app.get("/", include_in_schema=False)
async def root():
    """Redirect root to documentation"""
    return {
        "message": "Welcome to PeerHire Freelancer Recommendation API",
        "documentation": "/docs",
        "health_check": "/health"
    }
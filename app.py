"""
Main Application Entry Point
- Initializes the recommendation system
- Starts the API server
"""

import argparse
import uvicorn
import os
from dotenv import load_dotenv

from models.recommendation import recommendation_system
from models.collaborative_filtering import collaborative_filtering
from models.evaluation import RecommendationEvaluator
from data.data_generator import DataGenerator

# Load environment variables
load_dotenv()

def generate_data():
    """Generate sample data for the system"""
    print("Generating sample data...")
    generator = DataGenerator()
    generator.save_data()
    print("Sample data generation complete.")

def evaluate_model():
    """Evaluate the recommendation model"""
    print("Evaluating recommendation model...")
    
    # Train the model first
    if not recommendation_system.is_trained:
        recommendation_system.train()
    
    # Create evaluator
    evaluator = RecommendationEvaluator(recommendation_system)
    
    # Run evaluation
    results = evaluator.evaluate_full_system()
    
    # Print results
    print("\n===== Recommendation System Evaluation =====")
    print(f"Overall Score: {results['overall_score']:.4f}")
    
    print("\n--- Skill Coverage ---")
    skill_coverage = results["skill_coverage"]
    print(f"Average: {skill_coverage['average_skill_coverage']:.4f}")
    print(f"Median: {skill_coverage['median_skill_coverage']:.4f}")
    print(f"Min: {skill_coverage['min_skill_coverage']:.4f}")
    print(f"Max: {skill_coverage['max_skill_coverage']:.4f}")
    
    print("\n--- Budget Match ---")
    budget_match = results["budget_match"]
    print(f"Average: {budget_match['average_budget_match']:.4f}")
    print(f"Median: {budget_match['median_budget_match']:.4f}")
    print(f"Min: {budget_match['min_budget_match']:.4f}")
    print(f"Max: {budget_match['max_budget_match']:.4f}")
    
    print("\n--- Recommendation Diversity ---")
    diversity = results["diversity"]
    print(f"Average: {diversity['average_diversity']:.4f}")
    print(f"Median: {diversity['median_diversity']:.4f}")
    print(f"Min: {diversity['min_diversity']:.4f}")
    print(f"Max: {diversity['max_diversity']:.4f}")
    
    print("\n=========================================\n")

def start_api(host="0.0.0.0", port=8000, reload=False):
    """Start the FastAPI server"""
    # Pre-train the models
    print("Pre-training recommendation models...")
    recommendation_system.train()
    collaborative_filtering.train()
    print("Model training complete.")
    
    # Start the server
    print(f"Starting API server on {host}:{port}...")
    uvicorn.run(
        "api.main:app",
        host=host,
        port=port,
        reload=reload
    )

if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="PeerHire Freelancer Recommendation System")
    
    # Add arguments
    parser.add_argument("--generate-data", action="store_true", help="Generate sample data")
    parser.add_argument("--evaluate", action="store_true", help="Evaluate the recommendation model")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="API server host")
    parser.add_argument("--port", type=int, default=8000, help="API server port")
    parser.add_argument("--reload", action="store_true", help="Enable auto-reload for development")
    
    # Parse arguments
    args = parser.parse_args()
    
    # Execute based on arguments
    if args.generate_data:
        generate_data()
    
    if args.evaluate:
        evaluate_model()
    
    # Default action: start API
    start_api(
        host=args.host,
        port=args.port,
        reload=args.reload
    )
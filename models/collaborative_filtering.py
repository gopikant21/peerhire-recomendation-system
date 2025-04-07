"""
Collaborative Filtering Model
- Enhanced recommendation based on previous freelancer-client interactions
- Identifies patterns in hiring history
"""

import numpy as np
from typing import List, Dict, Any, Tuple
from sklearn.metrics.pairwise import cosine_similarity
from data.sample_data import data_manager

class CollaborativeFilteringModel:
    def __init__(self):
        """Initialize the collaborative filtering model"""
        self.freelancers = []
        self.clients = set()
        self.client_freelancer_matrix = None
        self.freelancer_indices = {}
        self.client_indices = {}
        self.is_trained = False
    
    def _build_interaction_matrix(self):
        """Build interaction matrix between clients and freelancers"""
        # Extract all unique clients and freelancers
        freelancer_ids = []
        client_ids = []
        
        # Process all freelancers and their projects
        for freelancer in self.freelancers:
            freelancer_id = freelancer["freelancer_id"]
            freelancer_ids.append(freelancer_id)
            
            # Extract clients from projects
            for project in freelancer["past_projects"]:
                client_id = project["client_id"]
                client_ids.append(client_id)
        
        # Get unique IDs
        unique_freelancer_ids = sorted(set(freelancer_ids))
        unique_client_ids = sorted(set(client_ids))
        
        # Create mapping from ID to index
        self.freelancer_indices = {fid: i for i, fid in enumerate(unique_freelancer_ids)}
        self.client_indices = {cid: i for i, cid in enumerate(unique_client_ids)}
        
        # Initialize interaction matrix
        self.client_freelancer_matrix = np.zeros((len(unique_client_ids), len(unique_freelancer_ids)))
        
        # Fill interaction matrix with ratings
        for freelancer in self.freelancers:
            freelancer_id = freelancer["freelancer_id"]
            if freelancer_id in self.freelancer_indices:
                freelancer_idx = self.freelancer_indices[freelancer_id]
                
                # Process each project
                for project in freelancer["past_projects"]:
                    client_id = project["client_id"]
                    if client_id in self.client_indices:
                        client_idx = self.client_indices[client_id]
                        rating = project["rating"]
                        
                        # Add rating to the matrix
                        self.client_freelancer_matrix[client_idx, freelancer_idx] = rating
    
    def train(self):
        """Train the collaborative filtering model"""
        # Load data
        self.freelancers = data_manager.get_freelancers()
        
        # Build interaction matrix
        self._build_interaction_matrix()
        
        self.is_trained = True
        print(f"Trained collaborative filtering model with {len(self.freelancer_indices)} freelancers and {len(self.client_indices)} clients")
    
    def recommend_for_client(self, client_id: str, top_n: int = 5) -> List[Dict[str, Any]]:
        """Get recommendations for a client based on collaborative filtering"""
        if not self.is_trained:
            self.train()
        
        # Check if client exists in our data
        if client_id not in self.client_indices:
            # Return empty list if client not found
            return []
        
        client_idx = self.client_indices[client_id]
        
        # Get client's ratings
        client_ratings = self.client_freelancer_matrix[client_idx, :]
        
        # If client has no ratings, return empty list
        if np.sum(client_ratings > 0) == 0:
            return []
        
        # Calculate similarity between this client and all other clients
        client_similarities = cosine_similarity([client_ratings], self.client_freelancer_matrix)[0]
        
        # Get top similar clients (excluding self)
        similar_client_indices = np.argsort(client_similarities)[::-1][1:6]  # Top 5 similar clients
        
        # Get ratings from similar clients
        similar_clients_ratings = self.client_freelancer_matrix[similar_client_indices, :]
        
        # Weight the ratings by similarity
        similarity_weights = client_similarities[similar_client_indices].reshape(-1, 1)
        weighted_ratings = similar_clients_ratings * similarity_weights
        
        # Calculate the weighted average ratings
        weighted_avg_ratings = np.sum(weighted_ratings, axis=0) / np.sum(similarity_weights)
        
        # Get freelancers that the client hasn't worked with
        unrated_freelancers = np.where(client_ratings == 0)[0]
        
        # Get predicted ratings for unrated freelancers
        predicted_ratings = [(i, weighted_avg_ratings[i]) for i in unrated_freelancers if weighted_avg_ratings[i] > 0]
        
        # Sort by predicted rating
        predicted_ratings.sort(key=lambda x: x[1], reverse=True)
        
        # Get top N freelancers
        top_freelancer_indices = [idx for idx, _ in predicted_ratings[:top_n]]
        
        # Get freelancer IDs
        reverse_freelancer_indices = {v: k for k, v in self.freelancer_indices.items()}
        top_freelancer_ids = [reverse_freelancer_indices[idx] for idx in top_freelancer_indices]
        
        # Get freelancer details
        recommendations = []
        for rank, freelancer_id in enumerate(top_freelancer_ids):
            freelancer = data_manager.get_freelancer_by_id(freelancer_id)
            if freelancer:
                idx = top_freelancer_indices[rank]
                predicted_rating = weighted_avg_ratings[idx]
                
                recommendation = {
                    "rank": rank + 1,
                    "freelancer_id": freelancer_id,
                    "name": freelancer["name"],
                    "predicted_rating": round(float(predicted_rating), 2),
                    "match_score": round(float(predicted_rating) / 5 * 100, 2),  # Convert to percentage
                    "skills": freelancer["skills"],
                    "hourly_rate": freelancer["hourly_rate"],
                    "experience_level": freelancer["experience_level"]
                }
                recommendations.append(recommendation)
        
        return recommendations
    
    def enhance_recommendations(self, client_id: str, content_recommendations: List[Dict[str, Any]],
                               weight_collaborative: float = 0.3) -> List[Dict[str, Any]]:
        """
        Enhance content-based recommendations with collaborative filtering
        
        Args:
            client_id: ID of the client
            content_recommendations: Recommendations from content-based filtering
            weight_collaborative: Weight for collaborative filtering (0-1)
            
        Returns:
            Enhanced recommendations
        """
        if not self.is_trained:
            self.train()
        
        # Get collaborative filtering recommendations
        cf_recommendations = self.recommend_for_client(client_id)
        
        # If no collaborative filtering recommendations, just return content-based ones
        if not cf_recommendations:
            return content_recommendations
        
        # Create a map of freelancer_id to score for both recommendation types
        content_scores = {rec["freelancer_id"]: rec["match_score"] for rec in content_recommendations}
        cf_scores = {rec["freelancer_id"]: rec["match_score"] for rec in cf_recommendations}
        
        # Combine all freelancer IDs
        all_freelancer_ids = set(content_scores.keys()) | set(cf_scores.keys())
        
        # Calculate hybrid scores
        hybrid_scores = {}
        for freelancer_id in all_freelancer_ids:
            content_score = content_scores.get(freelancer_id, 0)
            cf_score = cf_scores.get(freelancer_id, 0)
            
            # Calculate weighted average
            hybrid_score = (1 - weight_collaborative) * content_score + weight_collaborative * cf_score
            hybrid_scores[freelancer_id] = hybrid_score
        
        # Sort by hybrid score
        sorted_freelancers = sorted(hybrid_scores.items(), key=lambda x: x[1], reverse=True)
        
        # Get top freelancers (same number as content recommendations)
        top_n = len(content_recommendations)
        top_freelancer_ids = [f_id for f_id, _ in sorted_freelancers[:top_n]]
        
        # Create enhanced recommendations
        enhanced_recommendations = []
        for rank, freelancer_id in enumerate(top_freelancer_ids):
            freelancer = data_manager.get_freelancer_by_id(freelancer_id)
            if freelancer:
                score = hybrid_scores[freelancer_id]
                
                recommendation = {
                    "rank": rank + 1,
                    "freelancer_id": freelancer_id,
                    "name": freelancer["name"],
                    "match_score": round(score, 2),
                    "skills": freelancer["skills"],
                    "hourly_rate": freelancer["hourly_rate"],
                    "experience_level": freelancer["experience_level"],
                    "completed_projects": freelancer["completed_projects"],
                    "avg_rating": freelancer["avg_rating"]
                }
                enhanced_recommendations.append(recommendation)
        
        return enhanced_recommendations

# Create singleton instance
collaborative_filtering = CollaborativeFilteringModel()
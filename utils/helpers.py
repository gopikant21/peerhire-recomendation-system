"""
Helper Utilities
- General-purpose utility functions
- Reusable components across the application
"""

import os
import json
from typing import Dict, List, Any, Optional

def load_json_file(file_path: str) -> Any:
    """Load data from a JSON file"""
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None
    except json.JSONDecodeError:
        print(f"Invalid JSON in file: {file_path}")
        return None

def save_json_file(data: Any, file_path: str) -> bool:
    """Save data to a JSON file"""
    try:
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving JSON file: {e}")
        return False

def get_experience_level_value(level: str) -> int:
    """Convert experience level string to numerical value"""
    level_map = {
        "Entry": 1,
        "Intermediate": 2,
        "Advanced": 3,
        "Expert": 4
    }
    return level_map.get(level, 2)  # Default to Intermediate

def calculate_skill_overlap(skills1: List[str], skills2: List[str]) -> float:
    """Calculate the overlap between two skill sets"""
    if not skills1 or not skills2:
        return 0.0
    
    # Convert to sets for easier intersection
    set1 = set(skills1)
    set2 = set(skills2)
    
    # Calculate Jaccard similarity: |A ∩ B| / |A ∪ B|
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    
    return intersection / union if union > 0 else 0.0

def format_currency(amount: float) -> str:
    """Format a number as currency"""
    return f"${amount:.2f}"

def format_percentage(value: float) -> str:
    """Format a number as percentage"""
    return f"{value * 100:.2f}%"
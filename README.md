# PeerHire Freelancer Recommendation System

An AI-powered recommendation system that suggests the best freelancers for a given job based on skills, budget, and past project history.

## Project Overview

This project implements a content-based recommendation system that matches freelancers to job postings. The system takes into account:

- Skill match (using TF-IDF and cosine similarity)
- Experience level compatibility
- Budget compatibility
- Freelancer ratings and past project history

The API provides endpoints to:
- Get freelancer recommendations for a job
- View supported skills
- Check system health

## Technology Stack

- **Python 3.10+**
- **FastAPI** for API development
- **Scikit-learn** for machine learning algorithms
- **Docker** for containerization
- **JSON** for data storage

## Getting Started

### Prerequisites

- Python 3.10+
- pip (Python package manager)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/peerhire-recommendation-system.git
   cd peerhire-recommendation-system
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Generate sample data:
   ```bash
   python app.py --generate-data
   ```

### Running the Application

Run the API server:
```bash
python app.py
```

The API will be available at `http://localhost:8000`.

### Evaluating the Model

To evaluate the recommendation model performance:
```bash
python app.py --evaluate
```

## API Documentation

Once the server is running, you can access the API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### API Endpoints

- **GET /**: Health check
- **POST /recommend**: Get freelancer recommendations for a job
  - Query parameters:
    - `client_id`: Optional client ID for collaborative filtering
    - `use_collaborative`: Whether to enhance results with collaborative filtering
    - `cf_weight`: Weight for collaborative filtering (0-1)
- **GET /client/{client_id}/recommendations**: Get client-specific recommendations
- **GET /supported-skills**: Get list of supported skills

## Model Details

### Content-Based Filtering

The recommendation system uses content-based filtering with the following features:
1. **Skills matching**: TF-IDF vectorization and cosine similarity
2. **Experience level**: Numerical mapping and compatibility scoring
3. **Budget compatibility**: Comparing job budget with freelancer rates
4. **Rating score**: Weighted rating from past projects

### Collaborative Filtering

The system also includes collaborative filtering capabilities:
1. **Client-based recommendations**: Recommends freelancers based on the hiring patterns of similar clients
2. **Rating matrix**: Uses a client-freelancer rating matrix to identify patterns
3. **Hybrid approach**: Combines content-based and collaborative filtering for better results

### Feature Weights

#### Content-Based Filtering
- Skills: 50%
- Experience: 20% 
- Hourly rate: 15%
- Rating: 15%

#### Hybrid Model
- Content-based: 70% (default)
- Collaborative filtering: 30% (default, adjustable via API)

### Evaluation Metrics

The model is evaluated using:
- Skill coverage: How well recommended freelancers cover job required skills
- Budget match: How well freelancer rates match job budgets
- Recommendation diversity: Variety in the recommended freelancers

## Deployment

### Using Docker

Build the Docker image:
```bash
docker build -t peerhire-recommendation .
```

Run the container:
```bash
docker run -p 8000:8000 peerhire-recommendation
```

### Deployment on Cloud Platforms

#### Render

1. Create a new Web Service
2. Connect your GitHub repository
3. Set the build command: `pip install -r requirements.txt`
4. Set the start command: `gunicorn -w 4 -k uvicorn.workers.UvicornWorker api.main:app`

#### AWS Lambda

The project includes Lambda deployment configuration for serverless deployment.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- PeerHire for the internship assignment
- Scikit-learn for machine learning components
- FastAPI for the web framework
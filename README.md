Project Titan: A Scalable, AI-Powered News Analysis Engine
📖 Overview
Project Titan is an end-to-end data engineering project that builds a complete pipeline for scraping, analyzing, and searching news articles from multiple major sources. The system operates asynchronously, using a distributed task queue to handle the heavy lifting of web scraping and AI analysis, and exposes the results through a powerful semantic search API.

This project is a deep dive into modern backend architecture, demonstrating skills in data ingestion, asynchronous processing, applied AI, and containerization with Docker.

✨ Key Features
Multi-Source Scraping: Modular scrapers for five major news outlets (BBC News, AP News, The Guardian, TechCrunch, NPR).

Asynchronous Processing: Uses Celery and Redis to offload slow scraping and AI tasks to background workers, ensuring the main application remains responsive.

AI-Powered Analysis:

Sentiment Analysis: Automatically determines if an article's content is POSITIVE or NEGATIVE using a Hugging Face transformers model.

Semantic Search: Generates 384-dimensional vector embeddings for each article, allowing users to search by conceptual meaning, not just keywords.

Robust Database: Utilizes PostgreSQL with the pgvector extension for efficient similarity searches. Database schema is managed with Alembic migrations.

RESTful API: A FastAPI server provides endpoints to retrieve recent articles and perform powerful semantic searches.

Fully Containerized: The entire multi-service application (Postgres, Redis, API, Worker) is orchestrated with Docker Compose for easy setup and portability.

🛠️ Tech Stack
Backend: Python, FastAPI

Asynchronous Tasks: Celery

Message Broker: Redis

Database: PostgreSQL + pgvector

AI / ML: Hugging Face Transformers, PyTorch, Sentence-Transformers

Containerization: Docker, Docker Compose

Schema Migrations: Alembic

🏗️ System Architecture
The project is composed of four main containerized services that work together:

FastAPI API (api): The user-facing component. It receives HTTP requests, interacts with the database for queries, and returns results. It's also responsible for creating new scraping tasks.

Celery Worker (worker): The background processing engine. It listens for new tasks on the Redis queue, scrapes article content, performs AI analysis (sentiment and embeddings), and saves the enriched data to the database.

PostgreSQL Database (db): The primary data store for all scraped articles and their associated AI-generated metadata.

Redis (redis): Acts as the high-speed message broker, managing the queue of tasks between the API and the Celery workers.

🚀 Getting Started
Prerequisites
Docker and Docker Compose installed on your machine.

A tool for making API requests, like Postman or curl.

Installation & Setup
Clone the repository:

git clone https://github.com/IshanLenin/Scalable-AI-Powered-News-Analysis-Engine.git
cd Scalable-AI-Powered-News-Analysis-Engine

Build and Run the Containers:
This single command will build the Python Docker image and start all four services (db, redis, api, worker) in the background.

docker-compose up --build -d

The -d flag runs the containers in "detached" mode.

Run Database Migrations:
The first time you start the application, you need to set up the database schema. Open a second terminal and run this command to execute the Alembic migrations inside the running api container:

docker-compose exec api alembic upgrade head

Your entire application is now running!

⚙️ How to Use
1. Scrape for New Articles
To populate your database, you need to run the main scraping script. This will find links on the news homepages and dispatch tasks to your Celery workers.

Run this command in your terminal:

docker-compose exec api python main.py

You can monitor the progress of the workers by viewing the Docker logs:

docker-compose logs -f worker

2. Use the API
The API server is available at http://localhost:8000.

Get Recent Articles
Endpoint: GET /articles

Description: Retrieves the 10 most recently published articles.

Example curl:

curl -X GET "http://localhost:8000/articles"

Perform a Semantic Search
Endpoint: POST /search

Description: Finds the 5 articles most semantically similar to your query.

Example curl:

curl -X POST "http://localhost:8000/search" \
-H "Content-Type: application/json" \
-d '{"query": "global economic trends"}'

📂 Project Structure
.
├── alembic/              # Alembic migration scripts
├── scrapers/             # Modular scrapers for each news source
│   ├── bbc_scraper.py
│   └── ...
├── .dockerignore         # Files to ignore in the Docker build
├── api.py                # FastAPI application logic
├── celery_app.py         # Celery application configuration
├── docker-compose.yml    # Master blueprint for all services
├── Dockerfile            # Blueprint for the Python application container
├── main.py               # Main script to initiate scraping
├── models.py             # SQLAlchemy database models
├── requirements.txt      # Python dependencies
└── tasks.py              # Celery task definitions (scraping & AI)

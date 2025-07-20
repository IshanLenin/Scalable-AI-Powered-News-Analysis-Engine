# api.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from models import SessionLocal, Article
from typing import List
from pydantic import BaseModel, ConfigDict
import datetime
from tasks import get_embedding # <-- Import the embedding function

# --- Pydantic Models for Data Validation ---
class ArticleSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    title: str
    url: str
    sentiment: str | None = None
    publication_date: datetime.datetime | None = None

# Add a model for the search query
class SearchQuery(BaseModel):
    query: str

# --- FastAPI App ---
app = FastAPI(title="Project Titan API")

# --- Dependency for Database Session ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- API Endpoints ---
@app.get("/")
def read_root():
    return {"message": "Welcome to the News Analysis Engine API"}

@app.get("/articles", response_model=List[ArticleSchema])
def get_articles(db: Session = Depends(get_db)):
    """
    Retrieves the 10 most recent articles from the database.
    """
    articles = db.query(Article).order_by(Article.publication_date.desc()).limit(10).all()
    return articles

#Endpoint for user's query
@app.post("/search", response_model=List[ArticleSchema])
def search_articles(search: SearchQuery, db: Session = Depends(get_db)):
    """
    Performs a semantic search for articles based on the query.
    """
    # 1. Create an embedding for the user's query
    query_embedding = get_embedding(search.query)
    
    # 2. Find the 5 most similar articles in the database
    # The l2_distance operator (<->) is provided by pgvector
    similar_articles = db.query(Article).order_by(Article.embedding.l2_distance(query_embedding)).limit(5).all()
    
    if not similar_articles:
        raise HTTPException(status_code=404, detail="No similar articles found.")
        
    return similar_articles

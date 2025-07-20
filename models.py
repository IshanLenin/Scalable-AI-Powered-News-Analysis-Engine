# models.py
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import datetime
from pgvector.sqlalchemy import Vector

# --- ADD THIS LINE ---
load_dotenv() # Loads variables from the .env file

# Define the base class for declarative models
Base = declarative_base()

class Article(Base):
    # ... your Article class is perfect, no changes needed ...
    __tablename__ = 'articles'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    body_text = Column(Text)
    publication_date = Column(DateTime)
    url = Column(String, unique=True, nullable=False)
    scraped_at = Column(DateTime, default=datetime.datetime.utcnow)

    sentiment = Column(String) # Will store 'positive', 'negative', or 'neutral'
    embedding = Column(Vector(384)) # 384 is the dimension of the embedding model we'll use
    # ---------------------------------
   
    def __repr__(self):
        return f"<Article(title='{self.title}')>"



DATABASE_URL = os.getenv("DATABASE_URL") # Get the URL from the environment
if not DATABASE_URL:
    raise ValueError("No DATABASE_URL set for Flask application")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
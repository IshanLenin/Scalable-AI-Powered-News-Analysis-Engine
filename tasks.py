# tasks.py
from celery_app import celery
from models import SessionLocal, Article
from transformers import AutoTokenizer, AutoModel
from transformers.pipelines import pipeline
import torch

# --- AI Model Setup ---
# Load the models once when the worker starts, for efficiency.
print("Loading AI models...")
# 1. Sentiment analysis pipeline
sentiment_analyzer = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english") #type:ignore
# 2. All-purpose embedding model
embedding_tokenizer = AutoTokenizer.from_pretrained('sentence-transformers/all-MiniLM-L6-v2') #Converts human language to language that the AI can understand
embedding_model = AutoModel.from_pretrained('sentence-transformers/all-MiniLM-L6-v2') #The AI language converted into vector embedding.
print("AI models loaded successfully.")
# --------------------

# (Your SCRAPER_MAP and scraper imports stay the same)
from scrapers import bbc_scraper, apnews_scraper, theguardian_scraper, techcrunch_scraper, npr_scraper
SCRAPER_MAP = {
    'bbc.com': bbc_scraper.scrape_bbc_article_page,
    'apnews.com': apnews_scraper.scrape_ap_article_page,
    'theguardian.com': theguardian_scraper.scrape_guardian_article_page,
    'techcrunch.com': techcrunch_scraper.scrape_techcrunch_article_page,
    'npr.org': npr_scraper.scrape_npr_article_page,
}

#Embedding the text
def get_embedding(text):
    """Generates a vector embedding for a given text."""
    #Converts human language to AI language. 
    inputs = embedding_tokenizer(text, return_tensors='pt', truncation=True, padding=True, max_length=512)
    #Only reading, not learning.
    with torch.no_grad():
        outputs = embedding_model(**inputs)
    # Mean pooling to get a single vector for the whole text
    embedding = outputs.last_hidden_state.mean(dim=1).squeeze().numpy()
    return embedding
# ------------------------------------

@celery.task(name='tasks.process_article')
def process_article(title, url):
    """
    A Celery task that scrapes an article, performs AI analysis, 
    and saves everything to the database.
    """
    print(f"TASK STARTED: Processing {url}")
    
    scraper_func = None
    for domain, func in SCRAPER_MAP.items():
        if domain in url:
            scraper_func = func
            break
            
    if not scraper_func:
        print(f"ERROR: No scraper found for URL {url}")
        return

    body, date = scraper_func(url)

    if not body or not date:
        print(f"ERROR: Failed to scrape content for {url}")
        return

    # --- AI ANALYSIS ---
    # 1. Get sentiment
    sentiment_result = sentiment_analyzer(body[:512]) # Analyze the first 512 characters
    sentiment = sentiment_result[0]['label']
    print(f"  -> Sentiment: {sentiment}")

    # 2. Get embedding
    embedding_vector = get_embedding(body)
    print(f"  -> Embedding generated successfully.")
    # -----------------

    # Save the full article with AI data to the database
    db = SessionLocal()
    try:
        exists = db.query(Article).filter(Article.url == url).first()
        if exists:
            print(f"SKIPPED: Article {url} already exists.")
            return

        new_article = Article(
            title=title,
            url=url,
            body_text=body,
            publication_date=date,
            sentiment=sentiment, # Add sentiment
            embedding=embedding_vector # Add embedding
        )
        db.add(new_article)
        db.commit()
        print(f"SUCCESS: Saved article '{title}' with AI analysis.")
    except Exception as e:
        print(f"ERROR: Could not save article {url} to DB: {e}")
        db.rollback()
    finally:
        db.close()
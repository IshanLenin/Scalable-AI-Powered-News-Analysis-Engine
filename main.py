# main.py
import time
from tqdm import tqdm
from scrapers import bbc_scraper, apnews_scraper, theguardian_scraper, techcrunch_scraper, npr_scraper
from tasks import process_article # <-- Import your new task

def run_all_scrapers():
    """Finds article links and dispatches them to Celery workers."""
    print("Starting scraper process...")
    
    scrapers_to_run = [bbc_scraper, apnews_scraper, theguardian_scraper, techcrunch_scraper, npr_scraper]
    
    all_links = []
    # Loop through scrapers to find links, but don't scrape pages
    for scraper in tqdm(scrapers_to_run, desc="Finding Links"):
        # We need a new, lightweight function in each scraper
        links = scraper.find_links() 
        all_links.extend(links)
        time.sleep(1)
            
    print(f"\nFound {len(all_links)} total links. Dispatching tasks to workers...")
    
    # Dispatch a task for each link
    for link_data in tqdm(all_links, desc="Dispatching Tasks"):
        # .delay() is how you send a task to the Celery queue
        process_article.delay(link_data['title'], link_data['url']) #type:ignore

    print("\nAll tasks dispatched. Workers are now processing in the background.")

if __name__ == "__main__":
    run_all_scrapers()
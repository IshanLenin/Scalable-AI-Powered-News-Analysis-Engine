# scrapers/bbc_scraper.py
import requests
from bs4 import BeautifulSoup, Tag
import datetime

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def scrape_bbc_article_page(url_to_scrape):
    """This helper function scrapes the individual article page."""
    try:
        response = requests.get(url_to_scrape, headers=HEADERS)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        article_body = None
        paragraphs = soup.find_all('p', class_='sc-9a00e533-0 hxuGS')
        if paragraphs:
            article_body = '\n\n'.join([p.get_text(strip=True) for p in paragraphs])
        
        publication_date_obj = None 
        time_tag = soup.find('time', class_='sc-801dd632-2 IvNnh')
        if isinstance(time_tag, Tag):
            date_string = str(time_tag.get('datetime'))
            if date_string:
                if date_string.endswith('Z'):
                    date_string = date_string[:-1] + '+00:00'
                publication_date_obj = datetime.datetime.fromisoformat(date_string)
        
        return article_body, publication_date_obj
    except requests.RequestException as e:
        print(f"Error fetching BBC article page URL: {e}")
        return None, None

def find_links():
    """Finds article links on the BBC News homepage and returns a list of dictionaries."""
    print("--- Finding BBC News links ---")
    try:
        response = requests.get("https://www.bbc.com/news", headers=HEADERS)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        links_found = []
        # Use the selector for standard articles we found earlier
        article_links = soup.select('a[data-testid="internal-link"]', limit=5)
        
        for link_tag in article_links:
            if isinstance(link_tag, Tag):
                url = str(link_tag.get('href'))
                
                # Filter out non-articles
                if "/live/" in url or "/videos/" in url:
                    continue
                
                title_tag = link_tag.find('h2', attrs={'data-testid': 'card-headline'})
                if isinstance(title_tag, Tag):
                    title = title_tag.get_text(strip=True)
                    
                    if not url.startswith('https://'):
                        url = "https://www.bbc.com" + url
                    
                    if url and title:
                        links_found.append({"title": title, "url": url})

        # Return only the first 5 unique links
        return links_found[:5]
    except requests.RequestException as e:
        print(f"Error fetching BBC homepage: {e}")
        return []
# scrapers/apnews_scraper.py
import requests
from bs4 import BeautifulSoup, Tag
import datetime

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def scrape_ap_article_page(url_to_scrape):
    """Scrapes a single AP News article page for its body and date."""
    try:
        response = requests.get(url_to_scrape, headers=HEADERS)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        article_body = None
        body_container = soup.find('div', class_='RichTextStoryBody')
        if isinstance(body_container, Tag):
            paragraphs = body_container.find_all('p')
            article_body = '\n\n'.join([p.get_text(strip=True) for p in paragraphs])
        
        publication_date_obj = None
        time_tag = soup.find('bsp-timestamp')
        if isinstance(time_tag, Tag):
            timestamp_str = str(time_tag.get('data-timestamp'))
            if timestamp_str and timestamp_str.isdigit():
                timestamp_s = int(timestamp_str) / 1000
                publication_date_obj = datetime.datetime.fromtimestamp(timestamp_s, tz=datetime.timezone.utc)
        
        return article_body, publication_date_obj
    except requests.RequestException as e:
        print(f"Error fetching AP article page URL: {e}")
        return None, None

def find_links():
    """Finds article links on the AP News homepage and returns a list of dictionaries."""
    print("--- Finding AP News links ---")
    try:
        response = requests.get("https://apnews.com/", headers=HEADERS)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        links_found = []
        # Find all the 'PagePromo' divs that contain stories
        promo_divs = soup.find_all('div', class_='PagePromo', limit=5)

        for promo in promo_divs:
            if isinstance(promo, Tag):
                link_tag = promo.find('a', class_='Link')
                # The title can be in an h2 or a span
                title_tag = promo.find('h2', class_='PagePromo-title') or promo.find('span', class_='PagePromoContentIcons-text')

                if isinstance(link_tag, Tag) and isinstance(title_tag, Tag):
                    url = str(link_tag.get('href'))
                    title = title_tag.get_text(strip=True)
                    
                    if url and title:
                        links_found.append({"title": title, "url": url})
        
        return links_found[:5] # Return the first 5 found
    except requests.RequestException as e:
        print(f"Error fetching AP homepage: {e}")
        return []
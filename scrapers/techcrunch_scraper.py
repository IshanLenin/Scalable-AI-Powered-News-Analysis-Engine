# scrapers/techcrunch_scraper.py
import requests
from bs4 import BeautifulSoup, Tag
import datetime

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def scrape_techcrunch_article_page(url_to_scrape):
    """Scrapes a single TechCrunch article page for its body and date."""
    try:
        response = requests.get(url_to_scrape, headers=HEADERS)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        # --- Find Body Text ---
        article_body = None
        body_container = soup.find('div', class_='entry-content')
        if isinstance(body_container, Tag):
            paragraphs = body_container.find_all('p')
            article_body = '\n\n'.join([p.get_text(strip=True) for p in paragraphs])
        
        # --- Find and Parse Publication Date (Flexible) ---
        publication_date_obj = None 
        
        #Pattern 1: Find the time using the <time> tag.
        time_tag = soup.find('time', class_='wp-block-post-date-posted') or soup.find('time')
        if isinstance(time_tag, Tag) and time_tag.get('datetime'):
            date_string = str(time_tag.get('datetime'))
            try:
                publication_date_obj = datetime.datetime.fromisoformat(date_string)
            except ValueError:
                print(f"Could not parse ISO date string: {date_string}")
        
        # Pattern 2: If the first pattern fails, try the text-based span
        if not publication_date_obj:
            date_container = soup.find('div', class_='wp-block-techcrunch-podcast-single-hero__post-data')
            if isinstance(date_container, Tag):
                date_span = date_container.find('span', recursive=False, string=lambda t: ',' in t)
                if isinstance(date_span, Tag) or date_span:
                    date_string = date_span.get_text(strip=True)
                    try:
                        publication_date_obj = datetime.datetime.strptime(date_string, "%b %d, %Y")
                    except ValueError:
                        print(f"Could not parse text date string: {date_string}")
        
        return article_body, publication_date_obj

    except requests.RequestException as e:
        print(f"Error fetching TechCrunch article page URL: {e}")
        return None, None
    
def find_links():
    """Finds and returns a list of article links and titles from TechCrunch homepage."""
    print("--- Finding TechCrunch article links ---")
    URL = "https://techcrunch.com/"

    try:
        response = requests.get(URL, headers=HEADERS)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
    except requests.RequestException as e:
        print(f"Error fetching TechCrunch homepage: {e}")
        return []

    article_links = []
    link_tags = soup.find_all('a', class_='loop-card__title-link', limit=5)

    for link_tag in link_tags:
        if isinstance(link_tag, Tag):
            url = str(link_tag.get('href'))
            title = link_tag.get_text(strip=True)

            if url and title:
                article_links.append({
                    "title": title,
                    "url": url
                })

    print(f"Found {len(article_links)} TechCrunch article links.")
    return article_links

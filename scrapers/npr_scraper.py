# scrapers/npr_scraper.py
import requests
from bs4 import BeautifulSoup, Tag
import datetime

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def scrape_npr_article_page(url_to_scrape):
    """Scrapes a single NPR article page for its body and date."""
    try:
        response = requests.get(url_to_scrape, headers=HEADERS)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        # --- Find Body Text ---
        article_body = None
        # Use the 'storytext' ID you found for the container
        body_container = soup.find('div', id='storytext')
        if isinstance(body_container, Tag):
            # Find all the <p> tags directly inside the container
            paragraphs = body_container.find_all('p', recursive=False)
            article_body = '\n\n'.join([p.get_text(strip=True) for p in paragraphs])
        
        # --- Find Publication Date ---
        publication_date_obj = None
        # Find the <time> tag and get its 'datetime' attribute
        time_tag = soup.find('time')
        if isinstance(time_tag, Tag) and time_tag.get('datetime'):
            date_string = str(time_tag.get('datetime'))
            try:
                # fromisoformat handles the timezone info automatically
                publication_date_obj = datetime.datetime.fromisoformat(date_string)
            except ValueError:
                print(f"Could not parse date string: {date_string}")
        
        return article_body, publication_date_obj

    except requests.RequestException as e:
        print(f"Error fetching NPR article page URL: {e}")
        return None, None
    
def find_links():
    """Finds and returns a list of article links and titles from NPR homepage."""
    print("--- Finding NPR article links ---")
    URL = "https://www.npr.org/"
    
    try:
        response = requests.get(URL, headers=HEADERS)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
    except requests.RequestException as e:
        print(f"Error fetching NPR homepage: {e}")
        return []

    article_links = []
    headline_tags = soup.find_all('h3', class_='title', limit=5)

    for title_tag in headline_tags:
        if isinstance(title_tag, Tag):
            link_tag = title_tag.find_parent('a')
            if not isinstance(link_tag, Tag):
                continue

            url = str(link_tag.get('href'))
            title = title_tag.get_text(strip=True)

            if url and title:
                article_links.append({
                    "title": title,
                    "url": url
                })

    print(f"Found {len(article_links)} NPR article links.")
    return article_links

# scrapers/guardian_scraper.py
import requests
from bs4 import BeautifulSoup, Tag
import datetime

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def scrape_guardian_article_page(url_to_scrape):
    """Scrapes a single Guardian article page for its body and date."""
    try:
        response = requests.get(url_to_scrape, headers=HEADERS)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        # Use the selector that the debug output confirmed works
        article_body = None
        body_container = soup.find('div', class_='article-body-commercial-selector')
        if isinstance(body_container, Tag):
            paragraphs = body_container.find_all('p', class_='dcr-16w5gq9')
            article_body = '\n\n'.join([p.get_text(strip=True) for p in paragraphs])
        
        # Use the date selector that the debug output confirmed works
        publication_date_obj = None 
        summary_tag = soup.find('summary', class_='dcr-1ybxn6r')
        if isinstance(summary_tag, Tag):
            span_tag = summary_tag.find('span', class_="dcr-u0h1qy")
            if isinstance(span_tag, Tag):
                date_string_raw = span_tag.get_text(strip=True)
                date_string_parts = date_string_raw.split(' ')
                # Keep the first 5 parts to include the time
                date_string_clean = ' '.join(date_string_parts[:5])
                try:
                    publication_date_obj = datetime.datetime.strptime(date_string_clean, "%a %d %b %Y %H.%M")
                except ValueError:
                    print(f"Could not parse date string: {date_string_clean}")

        return article_body, publication_date_obj
    except requests.RequestException as e:
        print(f"Error fetching Guardian article page URL: {e}")
        return None, None
    
def find_links():
    """Finds and returns a list of article links and titles from The Guardian homepage."""
    print("--- Finding The Guardian article links ---")
    URL = "https://www.theguardian.com/international"

    try:
        response = requests.get(URL, headers=HEADERS)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
    except requests.RequestException as e:
        print(f"Error fetching The Guardian homepage: {e}")
        return []

    article_links = []
    containers = soup.find_all('div', class_='dcr-199p3eh', limit=5)

    for container in containers:
        if isinstance(container, Tag):
            link_tag = container.find('a')
            title_tag = container.find('h3', class_='card-headline')

            if not isinstance(link_tag, Tag) or not isinstance(title_tag, Tag):
                continue

            span_tag = title_tag.find('span', class_='show-underline')
            if not isinstance(span_tag, Tag):
                continue

            title = span_tag.get_text(strip=True)
            url = str(link_tag.get('href'))

            if not url or not title:
                continue

            if not url.startswith('https://'):
                url = "https://www.theguardian.com" + url

            article_links.append({"title": title, "url": url})

    print(f"Found {len(article_links)} Guardian article links.")
    return article_links

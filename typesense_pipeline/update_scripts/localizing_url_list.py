import requests
from bs4 import BeautifulSoup

def scrape_article_urls(base_urls):
    article_urls = []
    
    for base_url in base_urls:
        response = requests.get(base_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Adjust the selector as needed to target the article links
            links = soup.find_all('a', href=True) 
            
            for link in links:
                url = link['href']
                if '/fr/academy/' in url:  # Only keep URLs that lead to articles
                    if not url.startswith('http'):
                        url = 'https://www.ledger.com' + url
                    article_urls.append(url)
            
    return article_urls

def scrape_canonical_urls(article_urls, output_file):
    with open(output_file, 'w') as file:
        for article_url in article_urls:
            response = requests.get(article_url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                canonical_link = soup.find('link', rel='canonical')
                if canonical_link:
                    href = canonical_link.get('href')
                    if href:
                        file.write(href + '\n')

# Get all article URLs from the main academy pages
article_urls = scrape_article_urls([
    "https://www.ledger.com/fr/academy/",
    "https://www.ledger.com/fr/academy/basic-basics/",
    "https://www.ledger.com/fr/academy/sujets/blockchain/",
    "https://www.ledger.com/fr/academy/hardwarewallet/"
])

# Scrape canonical URLs from each article
scrape_canonical_urls(article_urls, 'url_fr.txt')

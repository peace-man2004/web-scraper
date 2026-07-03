import requests
from bs4 import BeautifulSoup
import csv
import time

def scrape_books(max_pages=3):
    base_url = "http://books.toscrape.com/catalogue/page-{}.html"
    all_books = []
    
    print("Starting web scraper...")
    
    for page in range(1, max_pages + 1):
        url = base_url.format(page)
        print(f"Scraping page {page}: {url}")
        
        # Send HTTP request
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        response = requests.get(url, headers=headers)
        
        if response.status_code != 200:
            print(f"Failed to retrieve page {page}")
            continue
            
        # Parse HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        books = soup.find_all('article', class_='product_pod')
        
        for book in books:
            title = book.h3.a['title']
            price = book.find('p', class_='price_color').text.replace('Â', '')
            availability = book.find('p', class_='instock availability').text.strip()
            
            all_books.append({
                'Title': title,
                'Price': price,
                'Availability': availability
            })
            
        # Polite scraping: pause between requests to not overload the server
        time.sleep(1)
        
    return all_books

def save_to_csv(data, filename="scraped_data.csv"):
    if not data:
        print("No data to save.")
        return
        
    keys = data[0].keys()
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        dict_writer = csv.DictWriter(f, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)
    print(f"Successfully saved {len(data)} items to {filename}!")

if __name__ == "__main__":
    scraped_data = scrape_books(max_pages=2)
    save_to_csv(scraped_data)
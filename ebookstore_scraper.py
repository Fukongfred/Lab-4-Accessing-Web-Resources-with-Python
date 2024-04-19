import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

from db import Database

load_dotenv()
BASE_URL = 'http://books.toscrape.com/catalogue/page-{page}.html'

# Mapping for textual ratings to numeric
rating_mapping = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}

def truncate_description(description):
    words = description.split()[:70]
    return ' '.join(words) + '...' if len(words) == 70 else ' '.join(words)

def main():
    with Database(os.getenv('DATABASE_URL')) as db:
        db.create_table()

        books = []
        page = 1
        while True:
            url = BASE_URL.format(page=page)
            print(f"Scraping {url}")
            response = requests.get(url)

            if response.status_code == 404:
                break

            soup = BeautifulSoup(response.text, 'html.parser')
            product_containers = soup.select('article.product_pod')

            for product in product_containers:
                book = {}
                title = product.select_one('h3 a')
                book['name'] = title.attrs['title']
                book['link'] = 'http://books.toscrape.com/catalogue/' + title.attrs['href']
                
                book_response = requests.get(book['link'])
                book_soup = BeautifulSoup(book_response.text, 'html.parser')
                description_elem = book_soup.select_one('#product_description ~ p')
                book['description'] = truncate_description(description_elem.text) if description_elem else "No description available."

                book['price'] = book_soup.select_one('p.price_color').text
                rating_text = product.select_one('p.star-rating')['class'][1]
                book['rating'] = rating_mapping.get(rating_text, 0)  # Default to 0 if not found

                db.insert_book(book)
                books.append(book)

            page += 1

        print(f"Scraped {len(books)} books")

if __name__ == '__main__':
    main()
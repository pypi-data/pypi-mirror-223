import requests
from bs4 import BeautifulSoup
import argparse
import logging
from time import sleep
import sys

# Constants for colored terminal text
CYAN = '\033[96m'
END = '\033[0m'

def get_args():
    parser = argparse.ArgumentParser(description='Search for books on Goodreads.')
    parser.add_argument('-n', '--number', type=int, default=10, help='Number of books to return.')
    parser.add_argument('-b', '--book', type=str, required=True, help='Name of the book to search for.')
    args = parser.parse_args()
    return args

def send_request(url):
    try:
        sleep(1)  # To prevent IP blocking
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logging.error(f'Request failed due to {e}')
        sys.exit(1)

    return response.text

def parse_response(html):
    soup = BeautifulSoup(html, 'html.parser')
    book_titles = soup.find_all('a', {'class': 'bookTitle'})
    book_authors = soup.find_all('a', {'class': 'authorName'})
    book_rating = soup.find_all('span', {'class': 'minirating'})

    return zip(book_titles, book_authors, book_rating)

def extract_book_details(book_info):
    title, author, rating = book_info
    title_text = title.find('span').text
    author_name = author.find('span').text
    rating_text = rating.text

    return {'title': title_text, 'author': author_name, 'rating': rating_text}

def search_for_books(book_name, num):
    url = "https://www.goodreads.com/search?utf8=✓&query=" + book_name.replace(' ', '+')
    html = send_request(url)
    book_infos = list(parse_response(html))[:num]
    books = [extract_book_details(info) for info in book_infos]
    return books

def main():
    args = get_args()
    books = search_for_books(args.book, args.number)

    if not books:
        logging.warning('No books found.')
        return
    
    # Print each book's information
    for book in books:
        print()
        print(f"{CYAN}{'Title:':<10} {book['title'][0:99]}{END}")
        print(f"{'Author:':<10} {book['author']}")
        print(f"{'Rating:':<10} {book['rating'].strip()}")
        print()
        print('-' * 30)  # Print a separator line

    print(f"{END}")

if __name__ == "__main__":
    main()

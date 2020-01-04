import re
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

BASE_URL = 'http://tululu.org/'
CATEGORY_URL = 'http://tululu.org/l{}/{}'
SCI_FI = 55


def get_books_from_category(page, category=CATEGORY_URL, genre=SCI_FI):
    url = category.format(genre, page)
    response = requests.get(url, allow_redirects=False)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'lxml')
    raw_books = soup.select('.bookimage a[href]')

    books = [urljoin(BASE_URL, book['href']) for book in raw_books]
    return books


def parse_category(start=1, end=10):
    books = []

    for page in range(start, end+1):
        try:
            parsed_books = get_books_from_category(page=page)
        except requests.HTTPError:
            parsed_books = []
        books.extend(parsed_books)

    return books


def main():
    books = parse_category(start=1, end=1)
    for book in books:
        # print(''.join([number for number in book if number.isdigit()]))
        print()


if __name__ == "__main__":
    main()

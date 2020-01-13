import json
import logging
import re
from parser.parse_tululu_book import download_library
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

BASE_URL = 'http://tululu.org/'
CATEGORY_URL = 'http://tululu.org/l{genre}/{page}'
SCI_FI_CATEGORY = 55
SCI_FI_LAST_PAGE = 701


def get_books_from_category(page, category=CATEGORY_URL, genre=SCI_FI_CATEGORY):
    url = category.format(genre=genre, page=page)
    response = requests.get(url, allow_redirects=False)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'lxml')
    raw_books = soup.select('.bookimage a[href]')

    return [urljoin(BASE_URL, book['href']) for book in raw_books]


def parse_category(start, end, output_json='sci-fi.json'):
    books = []

    for page in range(start, end):
        try:
            parsed_books = get_books_from_category(page=page)
        except requests.HTTPError:
            parsed_books = []
            logging.exception('Catch error.')

        if not parsed_books:
            return
        books_ids = [re.search(r'\d+', book).group(0) for book in parsed_books]
        books_data = download_library(books_ids)
        books.extend(books_data)

    with open(output_json, 'w') as json_file:
        json.dump(
            books,
            json_file,
            ensure_ascii=False,
            sort_keys=True,
            indent=4,
            separators=(',', ': '),
        )

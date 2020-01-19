import json
import logging
import re
from parser.parse_tululu_book import download_book
from typing import List, Optional
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

CATEGORY_URL = 'http://tululu.org/l{genre}/{page}'
SCI_FI_CATEGORY = 55
SCI_FI_LAST_PAGE = 701


def get_books_from_category(
    page: int,
    category: str = CATEGORY_URL,
    genre: int = SCI_FI_CATEGORY,
) -> List[str]:
    url = category.format(genre=genre, page=page)
    response = requests.get(url, allow_redirects=False)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'lxml')
    raw_books = soup.select('.bookimage a[href]')

    return [urljoin(CATEGORY_URL, book['href']) for book in raw_books]


def get_book_id(book_text: str) -> Optional[str]:
    match = re.search(r'\d+', book_text)
    return match.group(0) if match else None


def parse_category(start: int, end: int, output_json: str = 'sci-fi.json') -> None:
    books = []

    for page in range(start, end):
        try:
            parsed_books = get_books_from_category(page=page)
        except requests.HTTPError:
            parsed_books = []
            logging.exception('Catch error.')

        if not parsed_books:
            return
        books_ids: List[Optional[str]] = [get_book_id(book) for book in parsed_books]
        books_data = [download_book(book_id) for book_id in books_ids]
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

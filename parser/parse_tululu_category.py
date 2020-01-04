import json
import logging
import re
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from parser.parse_tululu_book import download_library

BASE_URL = 'http://tululu.org/'
CATEGORY_URL = 'http://tululu.org/l{}/{}'
SCI_FI_CATEGORY = 55
SCI_FI_LAST_PAGE = 701


def get_books_from_category(page, category=CATEGORY_URL, genre=SCI_FI_CATEGORY):
    url = category.format(genre, page)
    response = requests.get(url, allow_redirects=False)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'lxml')
    raw_books = soup.select('.bookimage a[href]')

    books = [urljoin(BASE_URL, book['href']) for book in raw_books]
    return books


def parse_category(start, end, output_json='sci-fi.json'):
    books = []

    for page in range(start, end):
        try:
            parsed_books = get_books_from_category(page=page)
            books_idies = [re.search(r"\d+", book).group(0) for book in parsed_books]
            books_data = download_library(books_idies)
            books.extend(books_data)
        except requests.HTTPError as error:
            logging.error(error)

    with open(output_json, "w") as file:
        json.dump(
            books,
            file,
            ensure_ascii=False,
            sort_keys=True,
            indent=4,
            separators=(",", ": "),
        )


def main():
    pass


if __name__ == "__main__":
    main()

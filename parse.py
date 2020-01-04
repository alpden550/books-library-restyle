import logging
import re
from parser.parse_tululu_book import download_library
from parser.parse_tululu_category import parse_category


def main():
    books = parse_category(end=1)
    books_idies = [re.search(r'\d+', book).group(0) for book in books]

    download_library(books_idies)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(levelname)s %(message)s')
    main()

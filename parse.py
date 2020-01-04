import argparse
import logging
import re
from parser.parse_tululu_book import download_library
from parser.parse_tululu_category import get_books_from_category


def create_parser():
    parser = argparse.ArgumentParser(
        description="Parse sci-fi book library and dowload books in txt format."
    )
    parser.add_argument(
        "-s",
        "--start_page",
        help="Starting page for parsing, default is 1.",
        type=int,
        choices=range(1, 702),
        metavar="From 1 to 701",
    )
    parser.add_argument(
        "-e",
        "--end_page",
        type=int,
        help="Ending page for parsing, default is 2.",
        choices=range(1, 703),
        metavar="From 1 to 702",
    )
    return parser.parse_args()


def main(start_page=None, end_page=None):
    start = start_page or 1
    end = end_page or 702
    for page in range(start, end):
        parsed_books = get_books_from_category(page=page)
        books_idies = [re.search(r"\d+", book).group(0) for book in parsed_books]
        download_library(books_idies)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    parser = create_parser()
    if not any((parser.start_page, parser.end_page)):
        logging.warning(
            "Attention!! \n\nYou are downloading more than 17000 books.\n\nIt will take extremely many time..\n\n"
        )

    main(parser.start_page, parser.end_page)

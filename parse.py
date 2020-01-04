import argparse
import logging
import re
from parser.parse_tululu_book import download_library
from parser.parse_tululu_category import parse_category


def create_parser():
    parser = argparse.ArgumentParser(
        description="Parse sci-fi book library and dowload books in txt format."
    )
    parser.add_argument(
        "-s",
        "--start_page",
        help="Starting page for parsing, default is 1.",
        type=int,
        default=1,
        choices=range(1, 702),
        metavar="From 1 to 701",
    )
    parser.add_argument(
        "-e",
        "--end_page",
        type=int,
        default=1,
        help="Ending page for parsing, default is 1.",
        choices=range(1, 702),
        metavar="From 1 to 701",
    )
    return parser.parse_args()


def main(start_page, end_page):
    books = parse_category(start_page, end_page)
    books_idies = [re.search(r"\d+", book).group(0) for book in books]

    download_library(books_idies)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    parser = create_parser()

    main(parser.start_page, parser.end_page)

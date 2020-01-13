import argparse
import logging
from parser.parse_tululu_category import SCI_FI_LAST_PAGE, parse_category


def create_parser():
    parser = argparse.ArgumentParser(
        description='Parse sci-fi book library and dowload books in txt format.',
    )
    parser.add_argument(
        '-s',
        '--start_page',
        help='Starting page for parsing, default is 1.',
        type=int,
        choices=range(1, SCI_FI_LAST_PAGE + 1),
        metavar='From 1 to 701',
    )
    parser.add_argument(
        '-e',
        '--end_page',
        type=int,
        help='Ending page for parsing, default is 2.',
        choices=range(1, SCI_FI_LAST_PAGE + 2),
        metavar='From 1 to 702',
    )
    return parser.parse_args()


def main(start_page=None, end_page=None):
    start = parser.start_page or 1
    end = parser.end_page or SCI_FI_LAST_PAGE + 1
    parse_category(start, end)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(levelname)s %(message)s')
    parser = create_parser()
    message = """
Attention!!,\n
You are downloading more than 17000 books.,\n
It will take extremely long time..\n
"""
    if not any((parser.start_page, parser.end_page)):
        logging.warning(message)
    main(parser.start_page, parser.end_page)

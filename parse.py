import logging
from parser.parse_tululu_category import SCI_FI_LAST_PAGE, parse_category
from textwrap import dedent

import click


# TODO: Add check typing and mypy
@click.command()
@click.option(
    '-s',
    '--start',
    type=click.IntRange(1, SCI_FI_LAST_PAGE),
    help='Start page, from 1 to 701.',
)
@click.option(
    '-e',
    '--end',
    type=click.IntRange(1, SCI_FI_LAST_PAGE + 1),
    help='End page, from 2 to 702.',
)
def main(start, end):
    """
    Parse sci-fi book library and dowload books in txt format.

    Use start page for first page, end page number + 1 for last page.
    """
    logging.basicConfig(level=logging.INFO, format='%(levelname)s %(message)s')
    message = """
        Attention!!,\n
        You are downloading more than 17000 books.,\n
        It will take extremely long time..\n
    """

    if not any((start, end)):
        logging.warning(dedent(message))
    start_page = start or 1
    end_page = end or SCI_FI_LAST_PAGE + 1
    parse_category(start_page, end_page)


if __name__ == '__main__':
    main()

import json
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape
from more_itertools import chunked

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml']),
)

env.globals['STATIC_URL'] = '../resources/'
env.globals['IMAGES_URL'] = '../'
env.globals['BOOKS_URL'] = '../'
template = env.get_template('template.html')


def main(pages_dir='pages'):
    Path(pages_dir).mkdir(exist_ok=True)
    books_data = json.loads(Path('sci-fi.json').read_text())
    chunked_books = list(chunked(books_data, 10))
    for chunk_number, books in enumerate(chunked_books, start=1):
        rendered_page = template.render(
            books=books,
            page_numbers=len(chunked_books),
            current_page=chunk_number,
        )
        Path('pages/index{number}.html'.format(number=chunk_number)).write_text(rendered_page)


if __name__ == '__main__':
    main()

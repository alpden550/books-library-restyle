import json
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml']),
)

template = env.get_template('template.html')


def get_books_chunks(books, size=10):
    chunks = []
    for index in range(0, len(books), size):  # noqa:WPS518
        chunks.append(books[index: index + size])
    return chunks


def main(pdges_dir='pages'):
    Path(pdges_dir).mkdir(exist_ok=True)
    books_data = json.loads(Path('sci-fi.json').read_text())
    chunked_books = get_books_chunks(books_data)
    for chunk_number, books in enumerate(chunked_books, start=1):
        rendered_page = template.render(
            books=books,
            page_numbers=len(chunked_books),
            current_page=chunk_number,
        )
        Path('pages/index{number}.html'.format(number=chunk_number)).write_text(rendered_page)


if __name__ == '__main__':
    main()

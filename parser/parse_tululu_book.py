import logging
from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filepath

BOOK_DOWNLOAD_URL = 'http://tululu.org/txt.php?id={book_id}'
BOOK_INFO_URL = 'http://tululu.org/b{book_id}/'


def create_pure_filepath(directory, filename):
    Path(directory).mkdir(exist_ok=True)
    filepath = Path(directory).joinpath(filename)
    return sanitize_filepath(filepath)


def download_txt(book_id, book_path, book_directory='books', url=BOOK_DOWNLOAD_URL):
    book_url = url.format(book_id=book_id)
    response = requests.get(book_url, allow_redirects=False)
    response.raise_for_status()

    filepath = create_pure_filepath(book_directory, book_path)
    book_path = '{filepath}.txt'.format(filepath=filepath)

    if not response.text:
        return None

    Path(book_path).write_text(response.text)
    return book_path


def download_image(image_url, image_directory='images'):
    image_name = image_url.split('/')[-1]

    response = requests.get(image_url)
    response.raise_for_status()

    image_path = create_pure_filepath(image_directory, image_name)

    Path(image_path).write_bytes(response.content)
    return image_path


def parse_book_text(text):
    soup = BeautifulSoup(text, 'lxml')
    title, author = soup.select_one('h1').text.split('::')
    image = soup.select_one('.bookimage img')['src']
    image_url = urljoin(BOOK_INFO_URL, image)
    raw_comments = soup.select('.texts .black')
    comments = [comment.text for comment in raw_comments]
    raw_genres = soup.select('span.d_book a')
    genres = [genre.text for genre in raw_genres]
    return (title.strip(), author, image_url, comments, genres)


def get_book_info(book_id, url=BOOK_INFO_URL):
    book_url = url.format(book_id=book_id)
    response = requests.get(book_url, allow_redirects=False)
    response.raise_for_status()

    try:
        return parse_book_text(response.text)
    except (requests.HTTPError, AttributeError):
        logging.exception('Error')
        return None


def download_book(book_id):
    book_info = get_book_info(book_id)
    if not book_info:
        return None
    title, author, image_url, comments, genres = book_info

    try:
        book_path = download_txt(book_id, title)
    except (requests.HTTPError, requests.ConnectionError):
        logging.exception('Error')
        book_path = None
    try:
        image_path = download_image(image_url)
    except requests.HTTPError:
        image_path = None
        logging.exception('Error')

    if book_path:
        logging.info('Dowloaded book %s', title)

    return {
        'title': title,
        'author': author,
        'img_src': str(image_path),
        'book_path': str(book_path),
        'comments': comments,
        'genres': genres,
    }


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(levelname)s %(message)s')
    download_book(book_id=239)  # noqa:WPS432

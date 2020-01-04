import json
import logging
from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filepath

BASE_URL = "http://tululu.org/"
BOOK_DOWNLOAD_URL = "http://tululu.org/txt.php?id={}"
BOOK_INFO_URL = "http://tululu.org/b{}/"


def create_pure_filepath(directory, filename):
    Path(directory).mkdir(exist_ok=True)
    filepath = Path(directory).joinpath(filename)
    return sanitize_filepath(filepath)


def download_txt(book_url, book_path, book_directory="books"):
    response = requests.get(book_url, allow_redirects=False)
    response.raise_for_status()

    filepath = create_pure_filepath(book_directory, book_path)
    book_path = "{}.txt".format(filepath)

    if not response.text:
        return

    Path(book_path).write_text(response.text)
    return book_path


def download_image(image_url, image_directory="images"):
    image_name = image_url.split("/")[-1]

    response = requests.get(image_url)
    response.raise_for_status()

    image_path = create_pure_filepath(image_directory, image_name)

    Path(image_path).write_bytes(response.content)
    return image_path


def get_book_info(book_id, url=BOOK_INFO_URL):
    book_url = url.format(book_id)
    response = requests.get(book_url, allow_redirects=False)
    response.raise_for_status()

    try:
        soup = BeautifulSoup(response.text, "lxml")
        title, author = soup.select_one('h1').text.split('::')
        image = soup.select_one('.bookimage img')['src']
        image_url = urljoin(BASE_URL, image)
        raw_comments = soup.select('.texts .black')
        comments = [comment.text for comment in raw_comments]
        raw_genres = soup.select('span.d_book a')
        genres = [genre.text for genre in raw_genres]

        return (title.strip(), author, image_url, comments, genres)

    except requests.HTTPError as error:
        logging.error(error)
        return None


def download_library(book_idies, url=BOOK_DOWNLOAD_URL, output_json="sci-fi.json"):
    books_description = []

    for book_id in book_idies:
        book_url = url.format(book_id)
        try:
            title, author, image_url, comments, genres = get_book_info(book_id)
            book_path = download_txt(book_url, title)
            image_path = download_image(image_url)
            logging.info('Dowloaded book {}'.format(title))

            books_description.append(
                {
                    "title": title,
                    "author": author,
                    "img_src": str(image_path),
                    "book_path": str(book_path),
                    "comments": comments,
                    "genres": genres,
                }
            )
        except (requests.HTTPError, AttributeError) as error:
            logging.error(error)

    with open(output_json, "a") as file:
        json.dump(
            books_description,
            file,
            ensure_ascii=False,
            sort_keys=True,
            indent=4,
            separators=(",", ": "),
        )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(levelname)s %(message)s')
    download_library([1, 2, 3, 4])

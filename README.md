# Parser for an online library

[![Maintainability](https://api.codeclimate.com/v1/badges/1cdba607bb5fa596ad0c/maintainability)](https://codeclimate.com/github/alpden550/books-library-restyle/maintainability) [![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide) [![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)

Parser for an online library, it parses sci-fi fiction [section](http://tululu.org/l55/) and download books in txt format.

Also, it downloads book covers and created JSON-file with the book descriptions.

Sci-Fi books library rendered example: [https://alpden550.github.io/books-library-restyle/pages/index1.html](https://alpden550.github.io/books-library-restyle/pages/index1.html)

## How to install

At least Python 3.6 must be already installed.

If you have already installed Poetry, install dependencies:

```bash
poetry install --no-dev
```

Or, should use the virtual environment for the best project isolation. And install requiremets.txt:

```bash
pip install -r requirements.txt
```

## How to use

To download all books from the first page, type:

```bash
python parse.py --end 2
```

And your terminal output:

```bash
INFO Dowloaded book Алиби
INFO Dowloaded book Бич небесный
INFO Dowloaded book Цена посвящения: Серый Ангел
INFO Dowloaded book Цена посвящения: Время Зверя
INFO Dowloaded book Дело Джен, или Эйра немилосердия
....
```

To get help, type:

```bash
python parse.py --help
```

To limit parsed pages by range from start to finish, enter start_page and end_page:

```bash
python parse.py --start 700 --end 701
```

Books from only page 700 will be downloaded.

And, to create html pages for downloded books, run:

```bash
python render-website.py
```

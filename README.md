# Parser online library

Parser for an online library, it parses sci-fi fiction [section](http://tululu.org/l55/) and download books in txt format.

Also, it downloads book covers and created JSON-file with the book descriptions.

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
python parse.py --end_page 2
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
python parse.py -h
```

To limit parsed pages by range from start to finish, enter start_page and end_page:

```bash
python parse.py --start_page 700 --end_page 701
```

Books from only page 700 will be downloaded.

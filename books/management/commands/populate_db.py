import csv
import re
from logging import warning, info, debug
from pathlib import Path

from django.core.management.base import BaseCommand

from books.models import *
from library import settings


def _normalize_data(data: str) -> str:
    return data.strip() if data and data.strip() else None


def _extract_shelf_data(shelf_data):
    split_data = re.split(r'[_\-–]', shelf_data, maxsplit=1)
    if len(split_data) == 2:
        cdd = _normalize_data(split_data[0])
        description = _normalize_data(split_data[1])
    else:
        cdd = None
        description = _normalize_data(split_data[0])
    shelf = Shelf(cdd=cdd, description=description)
    return shelf


def _populate_and_get_publisher(publisher_name):
    publisher_name = _normalize_data(publisher_name)
    if not publisher_name:
        return None

    publisher = Publisher.find_by_name_exact(publisher_name)

    if publisher.exists():
        return publisher.get()

    publisher = Publisher(name=publisher_name)
    publisher.save()

    return publisher


def _populate_and_get_collection(collection_name):
    collection_name = _normalize_data(collection_name)
    if not collection_name:
        return None

    collection = Collection.find_by_name_exact(collection_name)

    if collection.exists():
        return collection.get()

    collection = Collection(name=collection_name)
    collection.save()

    return collection


def _populate_and_get_shelf(shelf_name):
    shelf_name = _normalize_data(shelf_name)
    if not shelf_name:
        return None

    reference_shelf = _extract_shelf_data(shelf_name)
    shelf = Shelf.find_equals(reference_shelf)

    if shelf.exists():
        return shelf.get()

    reference_shelf.save()

    return reference_shelf


def _populate_and_get_author(author_name: str):
    author_name = _normalize_data(author_name)
    if not author_name:
        return None

    author = Author.find_by_name_exact(author_name)

    if author.exists():
        return author.get()

    author = Author(name=author_name)
    author.save()

    return author


def _populate_and_get_authors(row) -> list[Author]:
    authors = []

    author = _populate_and_get_author(row['author_1'])
    if author:
        authors.append(author)

    author = _populate_and_get_author(row['author_2'])
    if author:
        authors.append(author)

    author = _populate_and_get_author(row['author_3'])
    if author:
        authors.append(author)

    return authors


def _populate_and_get_translator(translator_name):
    translator_name = _normalize_data(translator_name)
    if not translator_name:
        return None

    translator = Translator.find_by_name_exact(translator_name)

    if translator.exists():
        return translator.get()

    translator = Translator(name=translator_name)
    translator.save()

    return translator


def _populate_and_get_translators(row) -> list[Translator]:
    translators = []

    translator = _populate_and_get_translator(row['translator_1'])
    if translator:
        translators.append(translator)

    translator = _populate_and_get_translator(row['translator_2'])
    if translator:
        translators.append(translator)

    translator = _populate_and_get_translator(row['translator_3'])
    if translator:
        translators.append(translator)

    return translators


def _populate_and_get_subjects(shelf: Shelf) -> list[Subject]:
    if not shelf or not shelf.cdd or not shelf.cdd[:3].isnumeric():
        return []

    cdd = shelf.cdd[:3]
    cdd = '0' * (3 - len(cdd)) + cdd

    return Subject.objects.filter(cdd__in=[cdd, cdd[:2] + '0', cdd[:1] + '00']).all()


class Command(BaseCommand):
    help = 'Populate database with default values'
    base_dir = Path(settings.BASE_DIR, 'books/management/commands')

    def _open_csv(self, csv_path: str):
        debug(f'Opening csv file {csv_path}')

        return open(Path(self.base_dir, csv_path), mode='r')

    def _populate_shelves(self):
        info('Populating shelves...')

        with self._open_csv('csv/shelves.csv') as csv_file:
            csv_reader = csv.reader(csv_file)

            for row in csv_reader:
                debug(f'Processing shelf data {row}')

                shelf = _extract_shelf_data(row[0])

                if not Shelf.find_equals(shelf).exists():
                    shelf.save()

    def _populate_authors(self):
        info('Populating authors...')

        with self._open_csv('csv/authors.csv') as csv_file:
            csv_reader = csv.DictReader(csv_file)

            for row in csv_reader:
                debug(f'Processing author data {row}')

                name = _normalize_data(row['name'])
                birth_death = row['birth_death'].split('-', maxsplit=1)
                birth = _normalize_data(birth_death[0]) if len(birth_death) > 0 and birth_death[0] else None
                death = _normalize_data(birth_death[1]) if len(birth_death) > 1 and birth_death[1] else None
                pha = _normalize_data(row['pha'])
                pha_label = _normalize_data(row['pha_label'])
                observation = _normalize_data(row['observation'])

                author = Author(
                    name=name,
                    year_of_birth=birth,
                    year_of_death=death,
                    pha=pha,
                    pha_label=pha_label,
                    observation=observation,
                )

                if not Author.find_equals(author).exists():
                    author.save()

    def _populate_subjects(self):
        info('Populating subjects...')

        with self._open_csv('csv/subjects.csv') as csv_file:
            csv_reader = csv.DictReader(csv_file)

            for row in csv_reader:
                debug(f'Processing subject data {row}')

                cdd = _normalize_data(row['ddc'])
                description = _normalize_data(row['description'])

                subject = Subject(
                    cdd=cdd,
                    description=description,
                )

                if not Subject.find_equals(subject).exists():
                    subject.save()

    def _populate_books(self):
        info('Populating books...')

        with self._open_csv('csv/books.csv') as csv_file:
            csv_reader = csv.DictReader(csv_file)

            for row in csv_reader:
                debug(f'Processing book data {row}')

                physical_id = _normalize_data(row['physical_id'])
                title = _normalize_data(row['title'])
                volume = _normalize_data(row['volume'])
                local = _normalize_data(row['local'])
                page_count = _normalize_data(row['page_count'])
                isbn = _normalize_data(row['isbn'])
                pha = _normalize_data(row['pha'])

                edition = _normalize_data(row['edition'])
                edition = edition if edition and edition.isnumeric() else None

                year = _normalize_data(re.sub(r'[\[\]]', '', row['year']))
                year = year if year and year.isnumeric() else None

                observation_1 = _normalize_data(row['observation_1'])
                observation_2 = _normalize_data(row['observation_2'])
                observations = '\n'.join(obs for obs in (observation_1, observation_2) if obs)

                publisher = _populate_and_get_publisher(row['publisher'])
                collection = _populate_and_get_collection(row['collection'])
                shelf = _populate_and_get_shelf(row['shelf'])

                authors = _populate_and_get_authors(row)
                translators = _populate_and_get_translators(row)
                subjects = _populate_and_get_subjects(shelf)

                book = Book(
                    physical_id=physical_id,
                    title=title,
                    collection=collection,
                    volume=volume,
                    edition=edition,
                    local=local,
                    publisher=publisher,
                    year=year,
                    page_count=page_count,
                    isbn=isbn,
                    pha=pha,
                    shelf=shelf,
                    observations=observations,
                )

                if not title:
                    warning(f'Book entry with physical id {physical_id} without a title, skipping...')
                    continue

                if Book.objects.filter(physical_id=physical_id).exists():
                    warning(f'Book with physical id {physical_id} already exists, skipping...')
                    continue

                if not Book.find_equals(book, authors, translators, subjects).exists():
                    book.save()

                    if authors:
                        [book.authors.add(author) for author in authors]

                    if translators:
                        [book.translators.add(translator) for translator in translators]

                    if subjects:
                        [book.subjects.add(subject) for subject in subjects]

                    book.save()

    def _populate_database(self):
        self._populate_shelves()
        self._populate_authors()
        self._populate_subjects()
        self._populate_books()

    def handle(self, *args, **options):
        self._populate_database()

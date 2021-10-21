import csv
import re
from pathlib import Path

from django.core.management.base import BaseCommand

from books.models import *
from library import settings


class Command(BaseCommand):
    help = 'Populate database with default values'

    def _populate_shelves(self):

        raw_shelves = []

        with open(Path(settings.BASE_DIR, 'books/management/commands/csv/shelves.csv'), mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)

            for row in csv_reader:
                raw_shelves.append(row['Nova Sequência 2016'])

        for raw_shelf in raw_shelves:
            split_data = re.compile(r'[_\-–]').split(raw_shelf, maxsplit=1)
            print(split_data)

            if len(split_data) == 2:
                cdd = split_data[0]
                description = split_data[1]
            else:
                cdd = None
                description = split_data[0]

            if not Shelf.objects.filter(cdd=cdd).filter(description=description).exists():
                Shelf(cdd=cdd, description=description).save()

    def _populate_authors(self):
        pass

    def _populate_books(self):
        pass

    def _populate_database(self):
        self._populate_shelves()
        self._populate_authors()
        self._populate_books()

    def handle(self, *args, **options):
        self._populate_database()

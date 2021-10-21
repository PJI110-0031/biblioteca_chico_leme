import csv
import re
from pathlib import Path

from django.core.management.base import BaseCommand

from books.models import *
from library import settings


class Command(BaseCommand):
    help = 'Populate database with default values'

    def _populate_shelves(self):
        with open(Path(settings.BASE_DIR, 'books/management/commands/csv/shelves.csv'), mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)

            for row in csv_reader:
                split_data = re.compile(r'[_\-–]').split(row['Nova Sequência 2016'], maxsplit=1)

                if len(split_data) == 2:
                    cdd = split_data[0]
                    description = split_data[1] if split_data[1] else None
                else:
                    cdd = None
                    description = split_data[0] if split_data[0] else None

                shelf = Shelf(cdd=cdd, description=description)

                if not Shelf.objects.filter(Shelf.equals(shelf)).exists():
                    shelf.save()

    def _populate_authors(self):
        with open(Path(settings.BASE_DIR, 'books/management/commands/csv/authors.csv'), mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)

            for row in csv_reader:
                name = row['AUTOR'] if row['AUTOR'] else None
                birth_death = row['Nascimento / Morte'].split('-', maxsplit=1)
                birth = birth_death[0] if len(birth_death) > 0 and birth_death[0] else None
                death = birth_death[1] if len(birth_death) > 1 and birth_death[1] else None
                pha = row['PHA (tabela)'] if row['PHA (tabela)'] else None
                pha_label = row['PHA / ETIQUETA/  CORRETA'] if row['PHA / ETIQUETA/  CORRETA'] else None
                observation = row['Observação'] if row['Observação'] else None

                author = Author(name=name,
                                year_of_birth=birth,
                                year_of_death=death,
                                pha=pha,
                                pha_label=pha_label,
                                observation=observation,
                                )

                if not Author.objects.filter(Author.equals(author)).exists():
                    author.save()

    def _populate_books(self):
        pass

    def _populate_database(self):
        self._populate_shelves()
        self._populate_authors()
        self._populate_books()

    def handle(self, *args, **options):
        self._populate_database()

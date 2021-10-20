from django.core.management.base import BaseCommand

from books.models import *


class Command(BaseCommand):
    help = 'Populate database with default values'

    def _populate_database(self):
        # Authors
        uncle_bob = Author(name='Robert C. Martin (Uncle Bob)', year_of_birth='1952', )
        david_thomas = Author(name='David Thomas')
        andrew_hunt = Author(name='Andrew Hunt')

        uncle_bob.save()
        david_thomas.save()
        andrew_hunt.save()

        # Subjects
        it = Subject(cdd=1, description='IT')
        education = Subject(cdd=2, description='Education')
        teaching = Subject(cdd=3, description='Teaching')

        it.save()
        education.save()
        teaching.save()

        # Shelves
        shelf_1 = Shelf(cdd=1, description='Shelf 1')
        shelf_2 = Shelf(cdd=2, description='Shelf 2')

        shelf_1.save()
        shelf_2.save()

        # Publishers
        pearson = Publisher(name='Pearson')
        addison_wesley = Publisher(name='Addison-Wesley Professional')

        pearson.save()
        addison_wesley.save()

        # Collections
        clean_code_collection = Collection(name='Clean code collection')
        clean_code_collection.save()

        # Books
        clean_code = Book(
            physical_id=1,
            title='Clean Code: A Handbook of Agile Software Craftsmanship',
            edition=1,
            isbn='9780132350884',
            shelf=shelf_1,
            publisher=pearson,
            page_count=1207,
            collection=clean_code_collection,
        )
        clean_code.save()
        clean_code.authors.add(uncle_bob)
        clean_code.subjects.add(it)

        clean_coder = Book(
            physical_id=2,
            title="The Clean Coder: A Code of Conduct for Professional Programmers",
            edition=1,
            isbn='9780137081073',
            shelf=shelf_1,
            publisher=pearson,
            page_count=256,
            collection=clean_code_collection,
        )
        clean_coder.save()
        clean_coder.authors.add(uncle_bob)
        clean_coder.subjects.add(it)

        clean_architecture = Book(
            physical_id=3,
            title="Clean Architecture: A Craftsman's Guide to Software Structure and Design",
            edition=1,
            isbn='9780134494166',
            shelf=shelf_1,
            publisher=pearson,
            page_count=432,
            collection=clean_code_collection,
        )
        clean_architecture.save()
        clean_architecture.authors.add(uncle_bob)
        clean_architecture.subjects.add(it)

        clean_agile = Book(
            physical_id=4,
            title="Clean Agile: Back to Basics",
            edition=1,
            isbn='9780135781869',
            shelf=shelf_1,
            publisher=pearson,
            page_count=240,
            collection=clean_code_collection,
        )
        clean_agile.save()
        clean_agile.authors.add(uncle_bob)
        clean_agile.subjects.add(it)

        the_pragmatic_programmer = Book(
            physical_id=5,
            title='The Pragmatic Programmer: From Journeyman to Master',
            edition=2,
            isbn='9780135957059',
            shelf=shelf_2,
            publisher=addison_wesley,
            page_count=352,
        )
        the_pragmatic_programmer.save()
        the_pragmatic_programmer.authors.add(david_thomas, andrew_hunt)
        the_pragmatic_programmer.subjects.add(education, teaching)

        clean_code.save()
        clean_coder.save()
        clean_architecture.save()
        clean_agile.save()
        the_pragmatic_programmer.save()

    def handle(self, *args, **options):
        self._populate_database()

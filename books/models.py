from django.contrib import admin
from django.db import models
from django.db.models import Q, QuerySet
from django.utils.translation import ugettext_lazy as _


def _bound_text(text, limit=100):
    return text if len(text) < limit else text[:limit] + '...'


class Publisher(models.Model):
    name = models.CharField(max_length=256, verbose_name=_('Name'))

    class Meta:
        verbose_name = _('Publisher')
        verbose_name_plural = _('Publishers')

    def __str__(self):
        return _bound_text(self.name)

    @staticmethod
    def find_by_name_exact(publisher_name) -> QuerySet:
        return Publisher.objects.filter(name__iexact=publisher_name)


class Shelf(models.Model):
    ddc = models.CharField(blank=True, null=True, max_length=10, verbose_name=_('DDC'))
    description = models.CharField(max_length=256, verbose_name=_('Description'))

    class Meta:
        verbose_name = _('Shelf')
        verbose_name_plural = _('Shelves')

    def __str__(self):
        return _bound_text(f"{_('Shelf')} {self.ddc + ' - ' if self.ddc else ''} {self.description}")

    @staticmethod
    def find_equals(other) -> QuerySet:
        return Shelf.objects.filter(ddc=other.ddc, description=other.description)


class Subject(models.Model):
    ddc = models.CharField(max_length=10, primary_key=True, verbose_name=_('DDC'))
    description = models.CharField(max_length=256, verbose_name=_('Description'))

    class Meta:
        verbose_name = _('Subject')
        verbose_name_plural = _('Subjects')

    def __str__(self):
        return f'{self.ddc} {self.description}'

    @staticmethod
    def find_equals(other) -> QuerySet:
        return Subject.objects.filter(ddc=other.ddc, description=other.description)


class Translator(models.Model):
    name = models.CharField(max_length=256, verbose_name=_('Name'))

    class Meta:
        verbose_name = _('Translator')
        verbose_name_plural = _('Translators')

    def __str__(self):
        return self.name

    @staticmethod
    def find_by_name_exact(translator_name) -> QuerySet:
        return Translator.objects.filter(Q(name__iexact=translator_name))


class Collection(models.Model):
    name = models.CharField(max_length=256, verbose_name=_('Name'))
    # publisher = models.ForeignKey(Publisher, on_delete=models.PROTECT, verbose_name=_('Publisher'))

    class Meta:
        verbose_name = _('Collection')
        verbose_name_plural = _('Collections')

    def __str__(self):
        return self.name

    @staticmethod
    def find_by_name_exact(collection_name) -> QuerySet:
        return Collection.objects.filter(name__iexact=collection_name)


class Author(models.Model):
    name = models.CharField(max_length=256, verbose_name=_('Name'))
    year_of_birth = models.CharField(max_length=10, blank=True, null=True, verbose_name=_('Year of birth'))
    year_of_death = models.CharField(max_length=10, blank=True, null=True, verbose_name=_('Year of death'))
    pha = models.PositiveIntegerField(blank=True, null=True, verbose_name=_('PHA'))
    pha_label = models.CharField(max_length=10, blank=True, null=True, verbose_name=_('PHA Label'))
    observation = models.TextField(blank=True, null=True, verbose_name=_('Observation'))

    class Meta:
        verbose_name = _('Author')
        verbose_name_plural = _('Authors')

    def __str__(self):
        return self.name

    @staticmethod
    def find_equals(other) -> QuerySet:
        return Author.objects.filter(
            Q(name=other.name),
            Q(year_of_birth=other.year_of_birth),
            Q(year_of_death=other.year_of_death),
            Q(pha=other.pha),
            Q(pha_label=other.pha_label),
            Q(observation=other.observation),
        )

    @staticmethod
    def find_by_name_exact(author_name) -> QuerySet:
        return Author.objects.filter(Q(name__iexact=author_name))


class Book(models.Model):
    physical_id = models.PositiveIntegerField(unique=True, verbose_name=_('Physical ID'))
    title = models.CharField(max_length=1024, verbose_name=_('Title'))
    authors = models.ManyToManyField(Author, verbose_name=_('Authors'))
    translators = models.ManyToManyField(Translator, blank=True, verbose_name=_('Translators'))
    collection = models.ForeignKey(Collection, on_delete=models.PROTECT, blank=True, null=True, verbose_name=_('Collection'))
    subjects = models.ManyToManyField(Subject, verbose_name=_('Subjects'))
    volume = models.CharField(max_length=10, blank=True, null=True, verbose_name=_('Volume'))
    edition = models.PositiveIntegerField(blank=True, null=True, verbose_name=_('Edition'))
    local = models.CharField(max_length=100, blank=True, null=True, verbose_name=_('Local'))
    publisher = models.ForeignKey(Publisher, on_delete=models.PROTECT, blank=True, null=True, verbose_name=_('Publisher'))
    year = models.IntegerField(blank=True, null=True, verbose_name=_('Year'))
    page_count = models.CharField(max_length=12, blank=True, null=True, verbose_name=_('Page count'))
    isbn = models.CharField(max_length=13, blank=True, null=True, verbose_name=_('ISBN'))
    pha = models.CharField(max_length=20, blank=True, null=True, verbose_name=_('PHA'))
    shelf = models.ForeignKey(Shelf, on_delete=models.PROTECT, blank=True, null=True, verbose_name=_('Shelf'))
    observations = models.TextField(max_length=2048, blank=True, null=True, verbose_name=_('Observations'))

    class Meta:
        verbose_name = _('Book')
        verbose_name_plural = _('Books')

    @admin.display(description=_('Authors'))
    def authors_str(self):
        return ' | '.join([str(author) for author in self.authors.all()])

    @admin.display(description=_('Subjects'))
    def subjects_str(self):
        return ' | '.join(str(subject) for subject in self.subjects.all())

    def infos(self):
        infos = []

        if self.isbn:
            infos.append(f"{_('ISBN')}: {self.isbn}")

        if self.collection:
            infos.append(f"{_('Collection')}: {self.collection}")

        if self.subjects:
            infos.append(f"{_('Subjects')}: {self.subjects_str()}")

        return infos

    def __str__(self):
        return self.title

    @staticmethod
    def search_query(search_text):
        query = Q()
        query.add(Q(isbn__icontains=search_text), Q.OR)
        query.add(Q(title__icontains=search_text), Q.OR)
        query.add(Q(authors__name__icontains=search_text), Q.OR)
        query.add(Q(authors__observation__icontains=search_text), Q.OR)
        query.add(Q(collection__name__icontains=search_text), Q.OR)
        query.add(Q(subjects__description__icontains=search_text), Q.OR)

        return query

    @staticmethod
    def find_equals(other, authors, translators, subjects) -> QuerySet:
        query = Q()
        query.add(Q(physical_id=other.physical_id), Q.AND)
        query.add(Q(title=other.title), Q.AND)
        query.add(Q(collection=other.collection), Q.AND)
        query.add(Q(volume=other.volume), Q.AND)
        query.add(Q(edition=other.edition), Q.AND)
        query.add(Q(local=other.local), Q.AND)
        query.add(Q(publisher=other.publisher), Q.AND)
        query.add(Q(year=other.year), Q.AND)
        query.add(Q(page_count=other.page_count), Q.AND)
        query.add(Q(isbn=other.isbn), Q.AND)
        query.add(Q(pha=other.pha), Q.AND)
        query.add(Q(shelf=other.shelf), Q.AND)
        query.add(Q(observations=other.observations), Q.AND)

        if authors:
            query.add(Q(authors__name__in=[author.name for author in authors]), Q.AND)

        if translators:
            query.add(Q(translators__name__in=[translator.name for translator in translators]), Q.AND)

        if subjects:
            query.add(Q(subjects__description__in=[subject.description for subject in subjects]), Q.AND)

        return Book.objects.filter(query)

from django.contrib import admin
from django.core.validators import MaxValueValidator
from django.db import models
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _


class Publisher(models.Model):
    name = models.CharField(max_length=256, verbose_name=_('Name'))

    class Meta:
        verbose_name = _('Publisher')
        verbose_name_plural = _('Publishers')

    def __str__(self):
        return self.name


class Shelf(models.Model):
    cdd = models.CharField(blank=True, null=True, max_length=10, verbose_name=_('CDD'))
    description = models.CharField(max_length=256, verbose_name=_('Description'))

    class Meta:
        verbose_name = _('Shelf')
        verbose_name_plural = _('Shelves')

    def __str__(self):
        return f"{_('Shelf')} {self.cdd + ' - ' if self.cdd else ''} {self.description}"


class Subject(models.Model):
    cdd = models.PositiveIntegerField(primary_key=True, validators=[MaxValueValidator(999)], verbose_name=_('CDD'))
    description = models.CharField(max_length=256, verbose_name=_('Description'))

    class Meta:
        verbose_name = _('Subject')
        verbose_name_plural = _('Subjects')

    def __str__(self):
        return self.description


class Translator(models.Model):
    name = models.CharField(max_length=256, verbose_name=_('Name'))

    class Meta:
        verbose_name = _('Translator')
        verbose_name_plural = _('Translators')

    def __str__(self):
        return self.name


class Collection(models.Model):
    name = models.CharField(max_length=256, verbose_name=_('Name'))
    # publisher = models.ForeignKey(Publisher, on_delete=models.PROTECT, verbose_name=_('Publisher'))

    class Meta:
        verbose_name = _('Collection')
        verbose_name_plural = _('Collections')

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=256, verbose_name=_('Name'))
    year_of_birth = models.PositiveIntegerField(blank=True, null=True, verbose_name=_('Year of birth'))
    year_of_death = models.PositiveIntegerField(blank=True, null=True, verbose_name=_('Year of death'))
    pha = models.PositiveIntegerField(blank=True, null=True, verbose_name=_('PHA'))
    pha_label = models.CharField(max_length=10, blank=True, null=True, verbose_name=_('PHA Label'))
    observation = models.TextField(blank=True, null=True, verbose_name=_('Observation'))

    class Meta:
        verbose_name = _('Author')
        verbose_name_plural = _('Authors')

    def __str__(self):
        return self.name


class Book(models.Model):
    physical_id = models.PositiveIntegerField(unique=True, verbose_name=_('Physical ID'))
    title = models.CharField(max_length=1024, verbose_name=_('Title'))
    authors = models.ManyToManyField(Author, verbose_name=_('Authors'))
    translators = models.ManyToManyField(Translator, blank=True, verbose_name=_('Translators'))
    collection = models.ForeignKey(Collection, on_delete=models.PROTECT, blank=True, null=True, verbose_name=_('Collection'))
    subjects = models.ManyToManyField(Subject, verbose_name=_('Subjects'))
    volume = models.PositiveIntegerField(blank=True, null=True, verbose_name=_('Volume'))
    edition = models.PositiveIntegerField(blank=True, null=True, verbose_name=_('Edition'))
    local = models.CharField(max_length=100, blank=True, null=True, verbose_name=_('Local'))
    publisher = models.ForeignKey(Publisher, on_delete=models.PROTECT, verbose_name=_('Publisher'))
    year = models.IntegerField(blank=True, null=True, verbose_name=_('Year'))
    page_count = models.PositiveIntegerField(blank=True, null=True, verbose_name=_('Page count'))
    isbn = models.CharField(max_length=13, blank=True, null=True, verbose_name=_('ISBN'))
    pha = models.CharField(max_length=20, blank=True, null=True, verbose_name=_('PHA'))
    shelf = models.ForeignKey(Shelf, on_delete=models.PROTECT, verbose_name=_('Shelf'))
    observations = models.TextField(max_length=2048, blank=True, null=True, verbose_name=_('Observations'))

    class Meta:
        verbose_name = _('Book')
        verbose_name_plural = _('Books')

    @admin.display(description=_('Authors'))
    def authors_str(self):
        return ', '.join(str(author) for author in self.authors.all())

    @admin.display(description=_('Subjects'))
    def subjects_str(self):
        return ', '.join(str(subject) for subject in self.subjects.all())

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

from .models import *


class DefaultModelAdmin(admin.ModelAdmin):
    list_per_page = 100


class PublisherAdmin(DefaultModelAdmin):
    search_fields = ('name',)
    ordering = ('name',)


class ShelfAdmin(DefaultModelAdmin):
    search_fields = ('ddc', 'description',)
    ordering = ('ddc',)


class SubjectAdmin(DefaultModelAdmin):
    search_fields = ('ddc', 'description',)
    ordering = ('ddc',)


class TranslatorAdmin(DefaultModelAdmin):
    search_fields = ('name',)
    ordering = ('name',)


class CollectionAdmin(DefaultModelAdmin):
    search_fields = ('name',)
    ordering = ('name',)


class AuthorAdmin(DefaultModelAdmin):
    search_fields = ('name',)
    ordering = ('name',)


class BookAdmin(DefaultModelAdmin):
    list_display = (
        'physical_id',
        'isbn',
        'title',
        'authors_str',
        'edition',
        'year',
        'subjects_str',
        'shelf',
        'publisher',
        'collection',
    )
    list_display_links = ('physical_id', 'isbn', 'title',)
    search_fields = (
        'physical_id',
        'title',
        'isbn',
        'pha',
        'observations',
        'authors__name',
        'subjects__ddc',
        'subjects__description',
        'publisher__name',
        'collection__name',
    )
    filter_horizontal = ('authors', 'translators', 'subjects',)


admin.site.register(Publisher, PublisherAdmin)
admin.site.register(Shelf, ShelfAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(Translator, TranslatorAdmin)
admin.site.register(Collection, CollectionAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Book, BookAdmin)

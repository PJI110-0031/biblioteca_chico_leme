from .forms import BookForm
from .models import *


class DefaultModelAdmin(admin.ModelAdmin):
    list_per_page = 100


class PublisherAdmin(DefaultModelAdmin):
    search_fields = ('name',)
    ordering = ('name',)


class ShelfAdmin(DefaultModelAdmin):
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
        'publisher__name',
        'collection__name',
    )
    autocomplete_fields = ('collection', 'publisher', 'shelf', 'authors', 'translators',)


admin.site.register(Publisher, PublisherAdmin)
admin.site.register(Shelf, ShelfAdmin)
admin.site.register(Translator, TranslatorAdmin)
admin.site.register(Collection, CollectionAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Book, BookAdmin, form=BookForm)

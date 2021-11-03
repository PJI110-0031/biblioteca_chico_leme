from django import forms
from django.utils.translation import gettext as _

from books.models import Book


class BookForm(forms.ModelForm):
    physical_id = forms.IntegerField(label=_('Physical ID'), initial=Book.next_physical_id)

    class Meta:
        model = Book
        fields = '__all__'

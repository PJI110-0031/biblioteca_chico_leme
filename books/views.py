from django.core.exceptions import BadRequest
from django.shortcuts import render

from .models import Book


def index(request):
    if 'search' in request.GET and request.GET['search']:
        search_text = request.GET['search']

        if len(search_text) < 3:
            raise BadRequest("Search query must have at least 3 characters")

        result = Book.search_by_text(search_text)

        return render(request, 'index.html', {'books': result, 'search_text': search_text})

    return render(request, 'index.html', {'books': []})

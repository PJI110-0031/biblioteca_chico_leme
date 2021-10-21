from django.shortcuts import render

from .models import Book


def index(request):
    if 'search' in request.GET and request.GET['search']:
        search_text = request.GET['search']

        result = Book.objects.filter(Book.search_query(search_text)).distinct()

        return render(request, 'index.html', {'books': result, 'search_text': search_text})

    return render(request, 'index.html', {'books': Book.objects.all()})

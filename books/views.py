from django.shortcuts import render

from .models import Book


def index(request):
    return render(request, 'index.html', {'books': Book.objects.all()})

from django.contrib import admin
from .models import Book, Genre, BookInstance, Author


# Регистриция моделей в админ панели
admin.site.register(Book)
admin.site.register(Genre)
admin.site.register(BookInstance)
admin.site.register(Author)

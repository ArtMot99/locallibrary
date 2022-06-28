from django.contrib import admin
from .models import Book, Genre, BookInstance, Author, Language


# Регистриция моделей в админ панели
# admin.site.register(Book)
admin.site.register(Genre)
# admin.site.register(BookInstance)
# admin.site.register(Author)
admin.site.register(Language)


@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    pass


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    pass


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')


admin.site.register(Author, AuthorAdmin)

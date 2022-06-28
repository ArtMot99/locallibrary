from django.contrib import admin
from .models import Book, Genre, BookInstance, Author, Language


# Регистриция моделей в админ панели
@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    pass


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    pass


@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'status', 'due_back', 'id')
    list_filter = ('status', 'due_back')
    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back')
        }),
    )


class BookInstanceInline(admin.TabularInline):
    model = BookInstance


# todo Выдает ошибку, когда пытаюсь добавить вывод жанра в админ панель.
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'language')  # 'display_genre'
    inlines = [BookInstanceInline]

    # def display_genre(self):
    #     """
    #     Creates a string for the Genre. This is required to display genre in Admin.
    #
    #     :return:
    #     """
    #     return ', '.join([genre.name for genre in self.genre.all()[:3]])
    # display_genre.short_description = 'Genre'


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]

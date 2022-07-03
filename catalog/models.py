from django.db import models
from django.urls import reverse
import uuid
from django.contrib.auth.models import User
from datetime import date


class Genre(models.Model):
    """
    Модель для хранения жанра книги
    """
    name = models.CharField(max_length=200, help_text='Введите жанр книги')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Language(models.Model):
    """
    Модель для представления языков книг
    """
    name = models.CharField(max_length=200, help_text='Введите оригинальный язык книги')

    class Meta:
        verbose_name = 'Язык'
        verbose_name_plural = 'Языки'

    def __str__(self):
        return self.name


class Book(models.Model):
    """
    Модель для отдельной книги
    """
    title = models.CharField(max_length=200)
    # Foreign Key used because book can only have one author, but authors can have multiple books
    # Author as a string rather than object because it hasn't been declared yet in the file.
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    summary = models.TextField(max_length=1000, help_text='Введите краткое описаные книги')
    isbn = models.CharField('ISBN', max_length=13, help_text='13 Символов <a href="https://www.isbn-international.org'
                                                             '/content/what-isbn">ISBN number</a>')
    # ManyToManyField used because genre can contain many books. Books can cover many genres.
    # Genre class has already been defined so we can specify the object above.
    genre = models.ManyToManyField(Genre, help_text='Выберите жанр для данной книги')
    language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['title', 'author']
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'

    def __str__(self):
        """
        Строка для отображения модели обьекта

        :return:
        """
        return self.title

    def get_absolute_url(self):
        """
        Возвращает url для доступа к определенному екземпляру книги

        :return:
        """
        return reverse('book-detail', args=[str(self.id)])


class BookInstance(models.Model):
    """
    BookInstance представляет собой определённую копию книги, которую кто-то может брать взаймы, и включает информацию
    о том, доступна ли копия или в какой день она ожидается, «отпечаток» или сведения о версии, а также уникальный
    идентификатор книги в библиотеке.
    """
    # используется для поля id, чтобы установить его как primary_key для этой модели.
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Уникальный идентификатор конкретной книги')
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    # используется для данных due_back (при которых ожидается, что книга появится после заимствования или обслуживания).
    # Это значение может быть blank или null (необходимо, когда книга доступна)
    due_back = models.DateField(null=True, blank=True)
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )
    # это CharField, который определяет список choice/selection. Как вы можете видеть, мы определяем кортеж, содержащий
    # кортежи пар ключ-значение и передаём его аргументу выбора
    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='m', help_text='Доступность книги')

    class Meta:
        ordering = ['due_back']
        verbose_name = 'Книжный экземпляр'
        verbose_name_plural = 'Книжные экземпляры'
        permissions = (("can_mark_returned", "Set book as returned"),)

    def __str__(self):
        return f'{self.id} ({self.book.title})'

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False


class Author(models.Model):
    """
    Модель, представляющая автора
    """
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'

    def get_absolute_url(self):
        """
        Возвращает URL-адрес для доступа к конкретному экземпляру автора

        :return:
        """
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        return f'{self.last_name} {self.first_name}'


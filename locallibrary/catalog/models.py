from django.db import models
from django.urls import reverse
import uuid # Требуется для уникальных экземпляров книг

# Create your models here.
class Genre(models.Model):
    """
    Модель, представляющая жанр книги (например, научная фантастика, документальная литература).
    """
    name = models.CharField(max_length=200, help_text="Укажите жанр книги (например, научная фантастика, французская поэзия и т. д.)")

    def __str__(self):
        """
        Строка для представления объекта модели (на сайте администратора и т. д.).
        """
        return self.name

class Book(models.Model):
    """
    Модель, представляющая книгу (но не конкретный экземпляр книги).
    """
    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    # Используется внешний ключ, поскольку у книги может быть только один автор, но у авторов может быть несколько книг.

    # Создавать как строку, а не как объект, поскольку он еще не объявлен в файле.
    summary = models.TextField(max_length=1000, help_text="Введите краткое описание книги")
    isbn = models.CharField('ISBN', max_length=13, help_text='13 characters <a href="https://www.isbn-international.org/content/what-isbn">ISBN номер</a>')

    genre = models.ManyToManyField(Genre, help_text="Выберите жанр этой книги")
    # ManyToManyField используется, поскольку жанр может содержать множество книг. Книги могут охватывать многие жанры.
    # Класс жанра уже определен, поэтому мы можем указать объект выше.

    def __str__(self):
        """
        Строка для представления объекта модели.
        """
        return self.title


    def get_absolute_url(self):
        """
        Возвращает URL-адрес для доступа к определенному экземпляру книги.
        """
        return reverse('book-detail', args=[str(self.id)])

    def display_genre(self):
        """
        Создает строку для жанра. Это необходимо для отображения жанра в администраторе.
        """
        return ', '.join([genre.name for genre in self.genre.all()[:3]])

    display_genre.short_description = 'Genre'

class BookInstance(models.Model):
    """
    Модель, представляющая конкретный экземпляр книги (т. е. ее можно взять в библиотеке).
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Уникальный идентификатор этой конкретной книги во всей библиотеке")
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)

    LOAN_STATUS = (
        ('о', 'Обслуживание'),
        ('в', 'В кредит'),
        ('д', 'Доступный'),
        ('с', 'Сдержанный'),
    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='m', help_text='Забронировать наличие')

    class Meta:
        ordering = ["due_back"]


    def __str__(self):
        """
        Строка для представления объекта модели.
        """
        return '{0} ({1})'.format(self.id, self.book.title)

class Author(models.Model):
    """
    Модель, представляющая автора.
    """
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Умер', null=True, blank=True)

    def get_absolute_url(self):
        """
        Возвращает URL-адрес для доступа к конкретному экземпляру автора.

        """
        return reverse('автор-деталь', args=[str(self.id)])


    def __str__(self):
        """
        Строка для представления объекта модели.
        """
        return '{0} ({1})'.format(self.last_name, self.first_name)

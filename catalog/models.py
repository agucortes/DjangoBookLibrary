from django.db import models
from django.db.models import UniqueConstraint
from django.db.models.functions.text import Lower
from django.urls import reverse
from pip._vendor.chardet.metadata.languages import Language


# Create your models here.

class Genre (models.Model):
    """Modelo de genero literario"""

    name = models.CharField(max_length=200, help_text="Ingrese el nombre del genero")

    def __str__(self):
        return self.name

class Book (models.Model):
    """Modelo que representa un libro, un solo ejemplar"""

    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True )

    summary = models.TextField(max_length=1000, help_text="ingrese una breve descripcion del libro")

    isbn = models.CharField('ISBN', max_length=13, help_text="13 caracteres de ISBN")

    genre = models.ManyToManyField(Genre, help_text="Seleccione un genero para este libro")

    language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['title', 'author']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book_detail', args=[str(self.id)])
    def display_genre(self):
        return ', '.join([genre.name for genre in self.genre.all()[:3]])

    display_genre.short_description = 'Genre'


import  uuid
class BookInstance (models.Model):
    """Modelo que representa una copia especifica del libro"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="ID unico para este libro en la biblioteca")
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)


    LOAN_STATUS=(
        ('m','Maintenance'),
        ('o', 'On Loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='m', help_text="Disponibilidad del libro")

    class Meta:
        ordering = ["due_back"]

    def __str__(self):

        return '%s (%s)' % (self.id, self.book.title)

class Author(models.Model):
    """Modelo que representa un autor"""

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    date_of_birth = models.DateField(null=True, blank=True)

    date_of_death = models.DateField('Died',null=True, blank=True)

    def get_absolute_url(self):

        return reverse('author_detail', args=[str(self.id)])

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)

class Language(models.Model):
    """modelo para representar un idioma"""
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        """Returns the url to access a particular language instance."""
        return reverse('language-detail', args=[str(self.id)])

    class Meta:
        constraints = [
            UniqueConstraint(
                Lower('name'),
                name='language_name_case_insensitive_unique',
                violation_error_message="Language already exists (case insensitive match)"
            ),
        ]

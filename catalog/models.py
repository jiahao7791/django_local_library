from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
import uuid
from datetime import date
# Create your models here.
#Genre Model
class Genre(models.Model):
    name = models.CharField(max_length=200,help_text='Etner a book genre')

    def __str__(self):
        return self.name
    
#Language Model
class Language(models.Model):
    name = models.CharField(max_length=20,help_text='Enter the language')
    def __str__(self):
        return self.name
#Book Model
class Book(models.Model):
    title = models.CharField(max_length=200)

    author = models.ForeignKey('Author',on_delete = models.SET_NULL,null = True)

    language = models.ForeignKey(Language,on_delete=models.SET_NULL,null=True)

    summary = models.TextField(max_length=1000,help_text='Enter a brief description.')

    isbn = models.CharField('ISBN',max_length=13,unique=True,help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')

    genre = models.ManyToManyField(Genre,help_text='Select a genre for the book')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book-detail',args=[str(self.id)])
        
    def display_genre(self):
        """Create a string for the Genre. This is required to display genre in Admin."""
        return ', '.join(genre.name for genre in self.genre.all()[:3])

    display_genre.short_description = 'Genre'

#BookInstance Model
class BookInstance(models.Model):
    id = models.UUIDField(primary_key=True,default = uuid.uuid4,help_text='Unique ID for this particular book across whole library')
    book = models.ForeignKey('Book',on_delete = models.RESTRICT,null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True,blank=True)
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='m',
        help_text='Book availability',
    )
    class Meta:
        ordering = ['due_back']
        permissions = (("can_mark_returned", "Set book as returned"),)

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.id} ({self.book.title})'

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False
    


#Author Model
class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True,blank=True)
    date_of_death = models.DateField('Died',null=True,blank=True)

    class Meta:
        ordering = ['first_name','last_name']

    def __str__(self):
        return f'{self.last_name}, {self.first_name}'

    def get_absolute_url(self):
        return reverse('author-detail',args=[str(self.id)])
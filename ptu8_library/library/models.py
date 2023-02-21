from django.db import models #modeliuose atsiranda tiiiik duomenys
from django.utils.translation import gettext_lazy as _
import uuid

class Genre(models.Model): #musu klase bus django duomenu modelis
    name = models.CharField(_('name'), max_length=50) #skliaustuose, ka matys vartotojas

    def __str__(self) -> str:
        return self.name

class Author(models.Model):
    first_name = models.CharField(_('first name'), max_length=100)
    last_name = models.CharField(_('last name'), max_length=100)

    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}'

    class Meta: #aprasomoji klase moduliui, tai tiesiog ordering nurodom
        ordering = ['last_name', 'first_name']

class Book(models.Model):
    title = models.CharField(_('title'), max_length=255, db_index=True)
    author = models.ForeignKey(
        Author,
        on_delete=models.PROTECT, #jeigu istrintu knyga, tai neleisim istriinti kol bent viena bus knyga
        related_name='books', #isduos visa autoriaus knygos sarasa
        verbose_name=_('author')
    )
    summary = models.TextField(_('summary'), max_length=4000, null=True, blank=True) #null leidzia duomenu bazej null reiksme, o blank, kad galima palikti tuscia
    genre = models.ManyToManyField(
        Genre,
        help_text=_('select genre(s) for this book'),
        verbose_name=_('genre(s)')
    )

    def __str__(self) -> str:
        return f"{self.author} - {self.title}"
    
    class Meta:
        ordering = ['title']

class BookInstance(models.Model):
    id = models.UUIDField(_('ID'), primary_key=True, default=uuid.uuid4, help_text=_('Unique ID for book copy')) #special kodukas, kad ir ta pati knyga bus, bet tures skirtinga nuemriuka
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE, #istrins visas kopijas, jei knyga istrinsim
        related_name='book_instances',
        verbose_name=_('book'),
    )
    due_back = models.DateField(_('due_back'), null=True, blank=True, db_index=True)
    
    LOAN_STATUS = (
        ('m', _('managed')),
        ('r', _('reserved')),
        ('t', _('taken')),
        ('a', _('available')),
        ('u', _('unavailable')),
    )
    
    status = models.CharField(_('status'), max_length=1, choices=LOAN_STATUS, default='a')

    def __str__(self) -> str:
        return f"{self.id}: {self.book}"
    
    class Meta:
        ordering = ['due_back']
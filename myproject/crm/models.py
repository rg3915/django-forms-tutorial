from django.db import models
from django.urls import reverse_lazy

from myproject.core.models import (
    Active,
    Address,
    Document,
    TimeStampedModel,
    UuidModel
)


class Person(UuidModel, TimeStampedModel, Address, Document, Active):
    first_name = models.CharField('nome', max_length=50, help_text='Digite somente o primeiro nome.')
    last_name = models.CharField('sobrenome', max_length=50, null=True, blank=True)  # noqa E501
    email = models.EmailField(null=True, blank=True)

    class Meta:
        ordering = ('first_name',)
        verbose_name = 'pessoa'
        verbose_name_plural = 'pessoas'

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name or ""}'.strip()

    def __str__(self):
        return self.full_name

    def get_absolute_url(self):
        return reverse_lazy('crm:person_detail', kwargs={'pk': self.pk})

    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
        }


class Photo(models.Model):
    photo = models.ImageField('foto', upload_to='')
    person = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        verbose_name='foto',
        related_name='photos',
    )

    class Meta:
        ordering = ('pk',)
        verbose_name = 'foto'
        verbose_name_plural = 'fotos'

    def __str__(self):
        return str(self.person)

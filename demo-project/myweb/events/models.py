from django.db import models

class Venue(models.Model):
    name = models.CharField('Venue name', max_length=120)
    adres = models.CharField(max_length=300)
    zip_code = models.CharField('Zip code', max_length=20)
    phone = models.CharField('Contact phone', max_length=16)
    web = models.URLField('Website address')
    email_adress = models.EmailField('Email address')

class Events(models.Model):
    name = models.CharField('Event name', max_length=120)
    event_date = models.DateTimeField('Event date')
    venue = models.CharField()
    manager = models.CharField('Manager name', max_length=120)
    description = models.TextField(blank=true)

    def __str__(self):
        return self.name
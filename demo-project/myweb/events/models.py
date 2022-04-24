from django.db import models

class Venue(models.Model):
    name = models.CharField('Venue name', max_length=120)
    adres = models.CharField(max_length=300)
    zip_code = models.CharField('Zip code', max_length=20)
    phone = models.CharField('Contact phone', max_length=16)
    web = models.URLField('Website address')
    email_adress = models.EmailField('Email address')

    def __str__(self):
        return self.name

class MyClubUser(models.Model):
    first_name =  models.CharField("User name", max_length=30)
    last_name = models.CharField("User last name", max_length=50)
    email = models.EmailField("User email", max_length=254)

    def __str__(self):
        return self.first_name + ' ' + self.last_name

class Event(models.Model):
    name = models.CharField('Event name', max_length=120)
    event_date = models.DateTimeField('Event date')
    venue = models.ForeignKey(Venue, blank=True, null=True, on_delete=models.CASCADE) #cascade is used to remove all connected data when table or entry is removed
    manager = models.CharField('Manager name', max_length=120)
    description = models.TextField(blank=True)
    attendees = models.ManyToManyField(MyClubUser, blank=True)

    def __str__(self):
        return self.name
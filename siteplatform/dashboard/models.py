from distutils.command.upload import upload
from django.db import models

# Create your models here.
class Firewalls(models.Model):
    mgmt_ip = models.GenericIPAddressField(max_length=14)
    state = models.BooleanField()
    hostname = models.CharField(max_length=50)
    vendor = models.CharField(max_length=20)
    premise_code = models.CharField(max_length=5)
    software_version = models.CharField(max_length=12)
    configuration_file = models.FileField(upload_to="media",blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.hostname

#class FirewallConfiguration(models.Model):
#    configuration_name = models.CharField(max_length=60)
#    configuration_file = models.FieldFile.save(save: pat, blank=True)
#https://stackoverflow.com/questions/7514964/django-how-to-create-a-file-and-save-it-to-a-models-filefield
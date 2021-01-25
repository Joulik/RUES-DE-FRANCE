from django.db import models

# Create your models here.
class StreetQuery(models.Model):
    street_name = models.CharField(max_length=128)
    #town_name = models.CharField(max_length=128)
from django.db import models

# Create your models here.
class StreetQuery(models.Model):
    street_name = models.CharField(max_length=128)
    #town_name = models.CharField(max_length=128)

class FranceRues(models.Model):
    voie = models.CharField(max_length=100)
    code_post = models.IntegerField()
    nom_comm = models.CharField(max_length=100)

class CommuneDepartementRegion(models.Model):
    code_commune_INSEE = models.CharField(max_length=6,null=False,blank=True)
    nom_commune_postal = models.CharField(max_length=50,null=False,blank=True)
    code_postal = models.IntegerField(blank=True,null=True)
    libelle_acheminement = models.CharField(max_length=50,null=False,blank=True)
    ligne_5 = models.CharField(max_length=40,null=False,blank=True)
    latitude = models.FloatField(blank=True,null=True,default=None)
    longitude = models.FloatField(blank=True,null=True,default=None)
    code_commune = models.IntegerField(blank=True,null=True)
    article = models.CharField(max_length=5,null=False,blank=True)
    nom_commune = models.CharField(max_length=50,null=False,blank=True) 
    nom_commune_complet = models.CharField(max_length=50,null=False,blank=True)
    code_departement = models.CharField(max_length=3,null=False,blank=True)
    nom_departement = models.CharField(max_length=30,null=False,blank=True)
    code_region = models.IntegerField(blank=True,null=True)
    nom_region = models.CharField(max_length=50,null=False,blank=True)
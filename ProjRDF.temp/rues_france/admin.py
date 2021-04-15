from django.contrib import admin
from rues_france.models import StreetQuery,FranceRues,CommuneDepartementRegion 

# Register your models here.
admin.site.register(StreetQuery)
admin.site.register(FranceRues)
admin.site.register(CommuneDepartementRegion)
import os
##configure settings for project
os.environ.setdefault("DJANGO_SETTINGS_MODULE",'ProjRDF.settings')

import django
django.setup()

from rues_france.models import FranceRues,CommuneDepartementRegion
import pandas as pd

# df=pd.read_csv('France_Rues.csv',sep=',')
# print(df)
# row_iter = df.iterrows()
# objs = [
#     FranceRues(
#         voie = row['voie'],
#         code_post  = row['code_post'],
#         nom_comm  = row['nom_comm'],
#     )
#     for index, row in row_iter
# ]
# FranceRues.objects.bulk_create(objs)

df = pd.read_csv('communes-departement-region.csv',sep=",") #, keep_default_na=False)
df.dropna(subset=['latitude','longitude'],inplace=True)
df['code_region'].fillna(0,inplace=True)
print(df)
row_iter = df.iterrows()
objs = [
    CommuneDepartementRegion(
        code_commune_INSEE = row['code_commune_INSEE'],
        nom_commune_postal = row['nom_commune_postal'],
        code_postal  = row['code_postal'],
        libelle_acheminement  = row['libelle_acheminement'],
        ligne_5 = row['ligne_5'],
        latitude = row['latitude'],
        longitude = row['longitude'],
        code_commune = row['code_commune'],
        article = row['article'],
        nom_commune = row['nom_commune'], 
        nom_commune_complet = row['nom_commune_complet'],
        code_departement = row['code_departement'],
        nom_departement = row['nom_departement'],
        code_region = row['code_region'],
        nom_region = row['nom_region'],
    )

    for index, row in row_iter
]
CommuneDepartementRegion.objects.bulk_create(objs)


    
    
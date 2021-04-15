from django.urls import path
from rues_france import views

urlpatterns = [
    #path("index",views.index,name="index"),
    path("",views.street_query,name='street_query'),
    path("most_requested.html/",views.most_requested,name='most_requested'),
]
from django import forms
from rues_france.models import StreetQuery

class StreetQueryForm(forms.ModelForm): #create class for new street query
    #place cross validation here in case needed

    class Meta(): #create inline class
        model = StreetQuery
        fields = '__all__' #use all field attributes
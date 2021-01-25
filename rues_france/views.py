from django.shortcuts import render
#from django.db.models import annotate
from rues_france.forms import StreetQueryForm
from rues_france.models import StreetQuery

# Create your views here.
def index(request):
    #print('Calling index')
    return render(request,'rues_france/index.html')

def street_query(request):

    #print('calling street')
    form = StreetQueryForm()

    if request.method == 'POST':
        form = StreetQueryForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            #return index(request)
        else:
            print("Form invalid")

    return render(request,'rues_france/index.html',{'form':form})

def most_requested(request):
    #most_requested_list = StreetQuery.objects.raw('SELECT * FROM rues_france_streetquery GROUP BY street_name')
    most_requested_list = StreetQuery.objects.raw('SELECT * FROM rues_france_streetquery GROUP BY street_name ORDER BY COUNT(street_name) DESC')
    for p in most_requested_list:
        print(p.street_name)
    most_requested_dict = {"most_requested_street" : most_requested_list}
    return render(request,'rues_france/most_requested.html',context=most_requested_dict)
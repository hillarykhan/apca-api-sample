from django.shortcuts import render
from django.shortcuts import HttpResponse

# Create your views here.
def Choropleth(request):
    return HttpResponse("<h1> The Choropleth Map Will Be Here! </h1>")


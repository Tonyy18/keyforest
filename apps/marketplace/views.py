from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def market_index(request):
    return render(request, "marketplace/index.html")

def search(request, query):
    return render(request, "marketplace/search.html")
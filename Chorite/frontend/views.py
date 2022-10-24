from django.shortcuts import render

# Create your views here.
def index(request):
    '''Return index and homepage of the app'''
    return render(request, "frontend/home.html")
    

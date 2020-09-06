from django.shortcuts import render, redirect

# Create your views here.
def index(request):
    return render(request, 'index.html')

def home(request):
    return render(request, 'music.html')

def search(request):
    search = request.POST('song')
    search.replace(" ", "%20")
    
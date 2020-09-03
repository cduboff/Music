from django.shortcuts import render, redirect

# Create your views here.
def index(request):
    return render(request, 'music.html')

def search(request):
    search = request.POST('song')
    search.replace(" ", "%20")
    request.GET('https://api.spotify.com/v1/search?q=tania%20bowra&type=artist&Authorization:%20Bearer:%205d76ac0e1b4c4d75b7627674b8129495')
    return render(request, 'music.html')
    # GET https://api.spotify.com/v1/search
    # "https://api.spotify.com/v1/search?q=tania%20bowra&type=artist" -H "Authorization: Bearer 5d76ac0e1b4c4d75b7627674b8129495"
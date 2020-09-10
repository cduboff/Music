from django.shortcuts import render, redirect
from .models import User, Posts
from django.contrib import messages
import bcrypt
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyOAuth
from spotipy.oauth2 import SpotifyClientCredentials


cid ="77e602fc63fa4b96acff255ed33428d3" 
secret = "f627bccaf8f14bc58195d7bf578f3590"

# # Create your views here
def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == 'POST':
        errors = User.objects.validator(request.POST)
        print(errors)
        if len(errors) > 0:
            for key, values in errors.items():
                messages.error(request, values)
            return redirect('/')
    password = request.POST['password']
    confirm_pw = request.POST['confirm_pw']
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    conf_hash = bcrypt.hashpw(confirm_pw.encode(), bcrypt.gensalt()).decode()
    new_user = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email_address=request.POST['email_address'], username = request.POST['username'], password=pw_hash, confirm_pw=conf_hash, birthday=request.POST['birthday'])
    request.session['name'] = new_user.first_name
    request.session['user_id'] = new_user.id
    return redirect('/home')

def login(request):
    if request.method == 'GET':
        return redirect('/')
    if not User.objects.authenticate(request.POST['username'], request.POST['password']):
        print(request.POST['username'], request.POST['password'])
        messages.error(request, 'Invalid Username/Password')
    if request.method == 'POST':
        logged_user = User.objects.filter(username=request.POST['username'])
        print(logged_user)
        if len(logged_user) > 0:
            logged_user = logged_user[0]
            print(logged_user.password)
            if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
                print(logged_user.password)
                request.session['name'] = logged_user.first_name
                request.session['user_id'] = logged_user.id
                return redirect('/home')
    return redirect('/')

def home(request):
    auth_manager = SpotifyClientCredentials()
    sp = spotipy.Spotify(auth_manager=auth_manager)
    context = {
        'user': User.objects.all(),
        'posts': Posts.objects.all(),
        'spotify': sp.user_playlists('spotify'),
    }

    return render(request, 'music.html', context)

def logout(request):
    request.session.flush()
    return redirect('/')

def edit_profile(request, id):
    if not User in request.session:
        return redirect('/')
    context = {
        'user': User.objects.get(id=id)
    }
    return render(request, 'edit.html', context)

def spotify(request):
    q = request.POST['query']
    q.replace(" ", "%20")
    return redirect('https://api.spotify.com/v1/search')

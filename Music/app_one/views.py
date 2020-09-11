from django.shortcuts import render, redirect
from .models import User, Posts
from django.contrib import messages
import bcrypt
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyOAuth
from spotipy.oauth2 import SpotifyClientCredentials

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
    }
    return render(request, 'music.html', context)

def logout(request):
    request.session.flush()
    return redirect('/')

def edit_profile(request, id):
    context = {
        'user': User.objects.get(id=id)
    }
    return render(request, 'edit.html', context)

def post(request):
    if request.method == 'POST':
        errors = Posts.objects.validator(request.POST)
        print(errors)
        if len(errors) > 0:
            for key, values in errors.items():
                messages.error(request, values)
            return redirect('/home')
        test_post = Posts.objects.create(content=request.POST['content'], poster=User.objects.get(id=request.session['user_id']))
        print(test_post)
    return redirect('/home')

def delete(request, id):
    Posts.objects.get(id=id).delete()
    return redirect('/home')

def edit_user(request, id):
    user = User.objects.get(id=id)
    if request.method == 'POST':
        errors = User.objects.edit(request.POST)
        print(errors)
        if len(errors) > 0:
            for key, values in errors.items():
                messages.error(request, values)
            return redirect(f'/edit_prof/{user.id}')
        user.username = request.POST['username']
        user.email_address = request.POST['email_address']
        user.save()
        print(user.username, user.email_address)
    return redirect('/home')

def spotify(request):
    auth_manager = SpotifyClientCredentials()
    sp = spotipy.Spotify(auth_manager=auth_manager)
    q = request.POST['q']
    result = sp.search(q)
    print(result)
    request.session['result'] = []
    # request.session['album'] = []
    for i in range(len(result['tracks']['items'])):
        result_obj = {}
        result_obj['name'] = result['tracks']['items'][i]['album']['name']
        result_obj['link'] = result['tracks']['items'][i]['external_urls']['spotify']
        request.session['result'].append(result_obj)
        print(result['tracks']['items'][i]['external_urls']['spotify'])
    # for i in range(len(result['tracks']['items'])):
    #     print(result['tracks']['items'][i]['external_urls']['spotify'])
    #     request.session['result'].append(result['tracks']['items'][i]['external_urls']['spotify'])
    #     request.session['album'].append(result['tracks']['items'][i]['album']['name'])
    return redirect('/home')
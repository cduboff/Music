from django.shortcuts import render, redirect
from .models import User, Posts
from django.contrib import messages
import bcrypt

# # Create your views here.
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
    new_user = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email_address=request.POST['email_address'], password=pw_hash, confirm_pw=conf_hash, birthday=request.POST['birthday'])
    request.session['name'] = new_user.first_name
    request.session['user_id'] = new_user.id
    return redirect('/home')

def login(request):
    if request.method == 'GET':
        return redirect('/')
    if not User.objects.authenticate(request.POST['username'], request.POST['password']):
        print(request.POST['username'], request.POST['password'])
        messages.error(request, 'Invalid Username/Password')
        return redirect('/')
    if request.method == 'POST':
        logged_user = User.objects.filter(username=request.POST['username'])
        if len(logged_user) > 0:
            logged_user = logged_user[0]
            if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
                request.session['name'] = logged_user.first_name
                request.session['user_id'] = logged_user.id
                return redirect('/home')

def home(request):
    context = {
        'user': User.objects.all(),
        'posts': Posts.objects.all(),
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

# def search(request):
#     search = request.POST('song')
#     search.replace(" ", "%20")

# def index(request):
#     params = {
#         'response_type': 'code',
#         'client_id': '77e602fc63fa4b96acff255ed33428d3',
#         'redirect_uri': 'http://localhost:7000/callback',
#         'challenge_method': 'S256'
#     }
#     return redirect(f'https://accounts.spotify.com/authorize/response_type={params["response_type"]}&client_id={params["client_id"]}&redirect_uri={params["redirect_uri"]}&challenge_method={params["challenge_method"]}')

def sign_in(request):
    params = {
        'response_type': 'code',
        'client_id': '77e602fc63fa4b96acff255ed33428d3',
        'redirect_uri': 'https://localhost:7000/callback',
    }
    return redirect(f'https://accounts.spotify.com/authorize/client_id={params["client_id"]}&response_type={params["response_type"]}&redirect_uri={params["redirect_uri"]}')

# def access(request):
#     params = {

#     }
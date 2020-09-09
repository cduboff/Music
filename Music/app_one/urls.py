from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.sign_in),
    path('home', views.home),
    path('reg', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('edit_prof/<int:id>', views.edit_profile),
]
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('home', views.home),
    path('reg', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('edit_prof/<int:id>', views.edit_profile),
    path('sign', views.spotify),
    path('search', views.post),
    path('delete_post/<int:id>', views.delete),
    path('edit/<int:id>', views.edit_user),
    path('view_user/<int:id>', views.view_user),
    path('like/<int:id>', views.post_like),
    path('comment/<int:id>', views.post_comment),
    path('like_comment/<int:id>', views.comment_like),
    path('delete_comment/<int:id>', views.delete_comment),
]
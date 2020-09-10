from django.db import models
from datetime import datetime
import re, bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9,+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
class UserManager(models.Manager):
    def validator(self, form):
        errors = {}
        if len(form['first_name']) < 2:
            errors['first_name'] = "First name must be at least 2 characters!"
        if len(form['last_name']) < 2:
            errors['first_name'] = "Last name must be at least 2 characters!"
        if len(form['username']) < 5:
            errors['username'] = "Username must be at least 5 characters:"
        email_check = self.filter(email_address=form['email_address'])
        if email_check:
            errors['email_address'] = "Email already in use"
        if len(form['password']) < 8:
            errors['password'] = "Password must be at least 8 characters!"
        if form['confirm_pw'] != form['password']:
            errors['confirm_pw'] = "Password and Confirmation Password do not match"
        return errors

    def authenticate(self, username, password):
        users = self.filter(username=username)
        if not users:
            return False

        user = users[0]
        return bcrypt.checkpw(password.encode(), user.password.encode())

class PostManager(models.Manager):
    def validator(self, form):
        errors = {}
        if len(form['content']) < 10:
            errors['content'] = "Post must be at least 10 characters!"
        return errors
# Create your models here.
class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    username = models.CharField(max_length=45)
    email_address = models.CharField(max_length=45)
    password = models.CharField(max_length=16)
    confirm_pw = models.CharField(max_length=16)
    birthday = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Posts(models.Model):
    poster = models.ForeignKey(User, related_name="posts", on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = PostManager()
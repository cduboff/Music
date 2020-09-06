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
        email_check = self.filter(email=form['email'])
        if email_check:
            errors['email'] = "Email already in use"
        if len(form['password']) < 8:
            errors['password'] = "Password must be at least 8 characters!"
        if form['confirm_pw'] != form['password']:
            errors['confirm_pw'] = "Password and Confirmation Password do not match"
        return errors

    def authenticate(self, email, password):
        users = self.filter(email=email)
        if not users:
            return False
        user = users[0]
        return bcrypt.checkpw(password.encode(), user.password.encode())

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

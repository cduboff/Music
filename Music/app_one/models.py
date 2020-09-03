from django.db import models
from datetime import datetime

# Create your models here.
class User(models.Model):
    first_name = CharField(max_length=255)
    last_name = CharField(max_length=255)
    username = CharField(max_length=45)
    email_address = CharField(max_length=45)
    password = CharField(max_length=16)
    confirm_pw = CharField(max_length=16)
    created_at = DateTimeField(auto_add_now=True)
    updated_at = DateTimeField(auto_now=True)
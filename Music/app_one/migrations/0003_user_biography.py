# Generated by Django 3.0.8 on 2020-09-13 20:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_one', '0002_posts'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='biography',
            field=models.TextField(default='no bio'),
            preserve_default=False,
        ),
    ]
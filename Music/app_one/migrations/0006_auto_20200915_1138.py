# Generated by Django 3.0.8 on 2020-09-15 15:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_one', '0005_posts_song_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='posts',
            name='likes',
            field=models.ManyToManyField(related_name='likes', to='app_one.User'),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('liked', models.ManyToManyField(related_name='liked', to='app_one.User')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment', to='app_one.Posts')),
                ('poster', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment', to='app_one.User')),
            ],
        ),
    ]

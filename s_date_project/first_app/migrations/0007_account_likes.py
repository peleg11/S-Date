# Generated by Django 2.2.5 on 2020-01-06 02:59

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first_app', '0006_merge_20200106_0218'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='user_likes', to=settings.AUTH_USER_MODEL),
        ),
    ]

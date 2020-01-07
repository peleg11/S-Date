# Generated by Django 2.2.5 on 2020-01-06 03:01

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first_app', '0007_account_likes'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='blocked',
            field=models.ManyToManyField(blank=True, related_name='blocked_users', to=settings.AUTH_USER_MODEL),
        ),
    ]

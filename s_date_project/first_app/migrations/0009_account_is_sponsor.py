# Generated by Django 2.2.5 on 2020-01-06 07:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first_app', '0008_account_blocked'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='is_sponsor',
            field=models.BooleanField(default=False),
        ),
    ]

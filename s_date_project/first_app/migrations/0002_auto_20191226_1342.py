# Generated by Django 2.2.5 on 2019-12-26 11:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('first_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='city',
            field=models.CharField(default='None', max_length=100),
        ),
        migrations.AlterField(
            model_name='account',
            name='country',
            field=models.CharField(default='None', max_length=100),
        ),
        migrations.AlterField(
            model_name='account',
            name='firstname',
            field=models.CharField(default='None', max_length=30),
        ),
        migrations.AlterField(
            model_name='account',
            name='hobbies',
            field=models.CharField(default='None', max_length=255),
        ),
        migrations.AlterField(
            model_name='account',
            name='lastname',
            field=models.CharField(default='None', max_length=30),
        ),
        migrations.CreateModel(
            name='FriendRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('from_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from_user', to=settings.AUTH_USER_MODEL)),
                ('to_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Friend',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('current_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='owner', to=settings.AUTH_USER_MODEL)),
                ('users', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

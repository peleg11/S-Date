from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from .models import Account
import django_filters
from django.conf import settings
from django.db import models

class UserFilter (django_filters.FilterSet):
    class Meta:
        model = Account
        fields= ['username', 'firstname', 'lastname', 'country', 'city', 'disabillity', 'hobbies']

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.conf import settings
from django.urls import reverse
from datetime import datetime
from django.utils.text import slugify
from django.db.models import Model
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.base import ObjectDoesNotExist

#import misaka

#User = get_user_model()
# Create your models here.
class MyAccountManager(BaseUserManager):
    def create_user(self, email, username ,firstname, lastname, country, city, birthdate, disabillity, hobbies ,password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')
    #    if not firstname or lastname:
    #        raise ValueError('This field cannot be empty')

        user = self.model(
			email=self.normalize_email(email),
			username=username,
            firstname=firstname,
            lastname=lastname,
            country=country,
            city=city,
            birthdate=birthdate,
            disabillity=disabillity,
            hobbies=hobbies,
            #profile_pic=profile_pic,

		)

        user.set_password(password)
        user.save(using=self._db)
        #admin=Account.objects.get(id=1)
        #Friend.make_friend(Friend, user, admin)
        #Friend.users.add(admin)
        return user

    def create_superuser(self, email, username, password,firstname, lastname, country, city, birthdate, disabillity, hobbies):
        #user=self.model(
        user = self.create_user(
            email=self.normalize_email(email),
			password=password,
			username=username,
            firstname=firstname,
            lastname=lastname,
            country=country,
            city=city,
            birthdate=birthdate,
            disabillity=disabillity,
            hobbies=hobbies,
            #profile_pic=profile_pic,
		)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class Account(AbstractBaseUser):

    STATUS = [
        ('visual', 'Visual impairment'),
        ('talk', 'Speech impairment'),
        ('autism', 'Autism'),
        ('legs', 'Legs disabillity'),
        ('hands', 'Hands disabillity'),
        ('other', 'Other'),
    ]
    firstname 				= models.CharField(max_length=30,default='None')
    lastname 				= models.CharField(max_length=30,default='None')
    email 					= models.EmailField(verbose_name="email", max_length=60, unique=True)
    username 				= models.CharField(max_length=30, unique=True)
    country 				= models.CharField(max_length=100,default='None')
    city 			    	= models.CharField(max_length=100,default='None')
    date_joined				= models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login				= models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin				= models.BooleanField(default=False)
    is_active				= models.BooleanField(default=True)
    is_staff				= models.BooleanField(default=False)
    is_superuser			= models.BooleanField(default=False)
    birthdate               =models.DateTimeField(verbose_name='birthdate', null=True, blank=True)
    disabillity             = models.CharField(max_length=200, choices=STATUS, default='other',)
    hobbies 				= models.CharField(max_length=255,default='None')
    profile_pic = models.ImageField(upload_to='profile_pics', blank=True, default='/profile_pics/blank_profile_pic.jpg')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','firstname', 'lastname',  'country', 'city', 'birthdate', 'disabillity', 'hobbies']

    objects = MyAccountManager()

    def __str__(self):
        return self.email

	# For checking permissions. to keep it simple all admin have ALL permissons
    def has_perm(self, perm, obj=None):
        return self.is_admin

	# Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
    def has_module_perms(self, app_label):
        return True

class BlogPost(models.Model):
	title 					= models.CharField(max_length=50, null=False, blank=False)
	body 					= models.TextField(max_length=5000, null=False, blank=False)
	image		 			= models.ImageField(upload_to='post_img', null=True, blank=True)
	date_published 			= models.DateTimeField(auto_now_add=True, verbose_name="date published")
	date_updated 			= models.DateTimeField(auto_now=True, verbose_name="date updated")
	author 					= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	slug 					= models.SlugField(blank=True, unique=True)

	def __str__(self):
		return self.title

class Post(models.Model):
    post = models.CharField(max_length=500)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    #user = models.ForeignKey(User , on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    #slug 					= models.SlugField(blank=True, unique=False)

class Friend(models.Model):
    users = models.ManyToManyField(settings.AUTH_USER_MODEL)
    current_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='owner', null=True)

    @classmethod
    def make_friend(cls, current_user, new_friend):
        friend, created = cls.objects.get_or_create(
            current_user=current_user
        )
        friend.users.add(new_friend)

    @classmethod
    def lose_friend(cls, current_user, new_friend):
        friend, created = cls.objects.get_or_create(
            current_user=current_user
        )
        friend.users.remove(new_friend)

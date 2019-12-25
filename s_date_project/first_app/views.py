from django.views.generic import TemplateView
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.base import ObjectDoesNotExist
#from first_app.forms import UserForm, UserProfileInfoForm
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User, AbstractBaseUser, BaseUserManager
#from .models import UserProfileInfo
from django.contrib.auth import authenticate,login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from django.views.decorators.csrf import csrf_exempt #This is to exclude the token authentication for the post request.
                                                     #should be resolved if needed
#POSTS:
from braces.views import SelectRelatedMixin
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import Http404
from django.views import generic

from . import forms
from . import models
# Create your views here.

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout

from .forms import RegistrationForm, AccountAuthenticationForm, AccountUpdateForm, HomeForm, UpdateBlogPostForm
from .models import BlogPost, Account, Post, Friend



def registration_view(request):
    registered = False
    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(email=email, password=raw_password)
            login(request, account)
            registered = True
            return redirect('home_page')

        else:
            context['registration_form'] = form

    else:
        form = RegistrationForm()
        context['registration_form'] = form
    return render(request, 'first_app/reg_page.html', context)


def logout_view(request):
	logout(request)
	return redirect('/')


def login_view(request):

	context = {}

	user = request.user
	if user.is_authenticated:
		return redirect('profile_page')

	if request.POST:
		form = AccountAuthenticationForm(request.POST)
		if form.is_valid():
			email = request.POST['email']
			password = request.POST['password']
			user = authenticate(email=email, password=password)

			if user:
				login(request, user)
				return redirect("profile_page")

	else:
		form = AccountAuthenticationForm()

	context['login_form'] = form

	# print(form)
	return render(request, "first_app/log.html", context)


def account_view(request):

	if not request.user.is_authenticated:
			return redirect("user_login")

	context = {}
	if request.POST:
		form = AccountUpdateForm(request.POST, instance=request.user)
		if form.is_valid():
			form.initial = {
					"email": request.POST['email'],
					"username": request.POST['username'],
                    "firstname": request.POST['firstname'],
                    "lastname": request.POST['lastname'],
                    "country": request.POST['country'],
                    "city": request.POST['city'],
                    "disabillity": request.POST['disabillity'],
                    "birthdate": request.POST['birthdate'],
                    "hobbies": request.POST['hobbies'],
                    "profile_pic": request.POST['profile_pic'],
			}
			form.save()
			context['success_message'] = "Updated"
    #            render(request, "first_app/settings.html", context)


	else:
		form = AccountUpdateForm(

			initial={
					"email": request.user.email,
					"username": request.user.username,
                    "firstname": request.user.firstname,
                    "lastname": request.user.lastname,
                    "country": request.user.country,
                    "city": request.user.city,
                    "disabillity": request.user.disabillity,
                    "birthdate": request.user.birthdate,
                    "hobbies": request.user.hobbies,
                    "profile_pic": request.user.profile_pic,
				}
			)

	context['account_form'] = form

	blog_posts = Post.objects.filter(user=request.user)
	context['blog_posts'] = blog_posts

	return render(request, "first_app/settings.html", context)


def must_authenticate_view(request):
	return render(request, 'first_app/reg_page.html', {})

def index(request):
    return render(request,'first_app/home_page.html')
def base(request):
    return render(request,'first_app/base.html')
def profile(request):
    return render(request,'first_app/profile_page.html')
#def events(request):
#    all_obj=UserProfileInfo.objects.all()
#    return render(request,'first_app/events.html',{'Users_view': all_obj})
#def show_profile(request):
#    all_obj=UserProfileInfo.objects.all()
    #context={
    #'username':obj.user,
    #'pic':obj.profile_pic
    #'object':obj
    #}
#    return render(request,'first_app/events.html',{'Users_view': all_obj})

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home_page'))

@login_required
def special(request):
    return HttpResponse("You are logged in!")


#    def get(request):
#        form = HomeForm()
#        posts = Post.objects.all().order_by('-created')
#
#        args = {
#            'form': form, 'posts': posts,
#            }
#        return render(request, 'first_app/user_login.html', args)

def post(request):
    if request.POST:
        form = HomeForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            #author = Account.objects.filter(username=user.username).first()
            author=request.user
            post.user = request.user
            post.save()

            text = form.cleaned_data['post']
            form = HomeForm()
            return redirect('profile_page')

            args = {'form': form, 'text': text}
            return render(request, 'first_app/profile_page.html', args)
    else:
        form = HomeForm()
        posts = Post.objects.all().order_by('-created')
        users = Account.objects.exclude(id=request.user.id)
    #    try:
        Friend.make_friend(current_user=request.user,new_friend=Account.objects.get(id=1))
        friend = Friend.objects.get(current_user=request.user)
        friends = friend.users.all()
    #    except Friend.DoesNotExist:
    #            go = None

        args = {
            'form': form, 'posts': posts, 'users': users, 'friends': friends
            }
        return render(request, 'first_app/profile_page.html', args)

def change_friends(request, operation, pk):
    friend = Account.objects.get(pk=pk)
    if operation == 'add':
        Friend.make_friend(request.user, friend)
    elif operation == 'remove':
        Friend.lose_friend(request.user, friend)
    return redirect('profile_page')

def view_profile(request, pk=None):
    if pk:
        user = Account.objects.get(pk=pk)
    else:
        user = request.user
    args = {'user': user}
    return render(request, 'first_app/profile_info.html', args)

@csrf_exempt
def audio_data(request):
    if request.method == 'POST':

        #Authenticating API
        gmaps = googlemaps.Client(key='YOUR_API_KEY')

        #Calling google geocode API with query as a Address
        geocode_result = gmaps.geocode(request.POST['send'])

        #geocode_result will return a JSON, contents can be extracted
        #for example
        x = geocode_result[0]['geometry']['location']['lat'] #get latitute for the query
        y = geocode_result[0]['geometry']['location']['lng'] #get longitude for the query

    else:
        message = "Please check the POST call"
        return HttpResponse(message)

def detail_blog_view(request,pk):

	context = {}

	blog_post = get_object_or_404(Post.objects.filter(pk=pk))
	context['blog_post'] = blog_post
#    context = blog_post
	return render(request, 'first_app/post_detail.html', context)

def create_blog_view(request):

	context = {}

	user = request.user
	#if not user.is_authenticated:
	#	return redirect('must_authenticate')

	form = HomeForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		obj = form.save(commit=False)
		author = Account.objects.filter(email=user.email).first()
		obj.author = author
		obj.save()
		form = HomeForm()

	context['form'] = form

	return render(request, "first_app/create_post.html", context)

def edit_blog_view(request,pk):

	context = {}

	user = request.user
	if not user.is_authenticated:
		return redirect("must_authenticate")

    #post=Post.objects.get()
	blog_post = get_object_or_404(Post.objects.filter(pk=pk))
    #context['blog_post'] = blog_post
	if blog_post.user != user:
		return HttpResponse('You are not the author of that post.')

	if request.POST:
		form = UpdateBlogPostForm(request.POST or None, request.FILES or None, instance=blog_post)
		if form.is_valid():
			obj = form.save(commit=False)
			obj.save()
			context['success_message'] = "Updated"
			blog_post = obj

	form = UpdateBlogPostForm(
			initial = {
				#	"title": blog_post.title,
					"text": blog_post.post,
				#	"image": blog_post.image,
			}
		)

	context['form'] = form
	return render(request, 'first_app/edit_post.html', context)

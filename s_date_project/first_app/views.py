from django.views.generic import TemplateView
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.base import ObjectDoesNotExist
from django.core import mail
from s_date_project.settings import EMAIL_HOST_USER

from django.contrib.sessions.models import Session
from django.utils import timezone

from django.core.mail import send_mail

# from first_app.forms import UserForm, UserProfileInfoForm
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User, AbstractBaseUser, BaseUserManager
# from .models import UserProfileInfo
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from django.views.decorators.csrf import \
    csrf_exempt  # This is to exclude the token authentication for the post request.
# should be resolved if needed
# POSTS:
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

from .forms import RegistrationForm, AccountAuthenticationForm, AccountUpdateForm, HomeForm, UpdateBlogPostForm, \
    CreateBlogPostForm, InvitaionForm, active_form
from .models import BlogPost, Account, Post, Friend, FriendRequest

from .filters import UserFilter

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist

from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.views.generic import RedirectView

def news(request):
    return render(request,'first_app/news.html')

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

    # form2 = forms.InvitaionForm()
    # if request.method == 'POST':
    # form2=forms.InvitaionForm(request.POST)
    # send_mail('Hello from Sdate Project', 'Someone wants you to join our website! check it out at: https://127.0.0.1:8000', settings.EMAIL_HOST_USER, str(form2['Email'].value()), fail_silently=True)
    # return render(request, 'first_app/success.html')
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
    return render(request, 'first_app/home_page.html')


def base(request):
    return render(request, 'first_app/base.html')


def profile(request):
    return render(request, 'first_app/profile_page.html')


# def events(request):
#    all_obj=UserProfileInfo.objects.all()
#    return render(request,'first_app/events.html',{'Users_view': all_obj})
# def show_profile(request):
#    all_obj=UserProfileInfo.objects.all()
# context={
# 'username':obj.user,
# 'pic':obj.profile_pic
# 'object':obj
# }
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

def post(request, pk=1):
    if request.POST:
        form = HomeForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            # author = Account.objects.filter(username=user.username).first()
            author = request.user
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
        # post=None
        # post=get_object_or_404(Post.objects.filter(pk=pk))
        for post in posts:
            is_liked = False
            if post.likes.filter(id=request.user.id).exists():
                is_liked = True
        users = Account.objects.exclude(id=request.user.id)
        sent_friend_requests = FriendRequest.objects.filter(from_user=request.user)
        sent_requests = FriendRequest.objects.filter(from_user=request.user).filter(from_user=request.user)
        user_request_list = []
        #    for requests in sent_friend_requests:
        #    user_request_list.append(sent_requests.get(from_user=request.user))
        users_requests = Account.objects.filter(id__in=user_request_list)

        rec_friend_requests = FriendRequest.objects.filter(to_user=request.user)
        #    try:
        Friend.make_friend(current_user=request.user, new_friend=Account.objects.get(id=1))
        friend = Friend.objects.get(current_user=request.user)
        friends = friend.users.all()

        button_status = 'none'
        if request.user not in friend.users.all():
            button_status = 'not_friend'
        # if FriendRequest.objects.filter(from_user=request.user).filter(to_user=request.user):
        #    button_status = 'friend_request_sent'
        # if we have sent him a friend request

        if len(FriendRequest.objects.filter(from_user=request.user).filter(to_user=request.user)) == 1:
            button_status = 'friend_request_sent'

        active_sessions = Session.objects.filter(expire_date__gte=timezone.now())
        user_id_list = []
        for session in active_sessions:
            data = session.get_decoded()
            user_id_list.append(data.get('_auth_user_id', None))
        online_users = Account.objects.filter(id__in=user_id_list)

        args = {
            'form': form, 'posts': posts, 'users': users, 'friends': friends, 'is_liked': is_liked,
            'total_likes': post.total_likes(), 'users_requests': users_requests, 'button_status': button_status,
            'sent_friend_requests': sent_friend_requests, 'sent_requests': sent_requests,
            'rec_friend_requests': rec_friend_requests, 'online_users': online_users
        }
        return render(request, 'first_app/profile_page.html', args)


def change_friends(request, operation, pk):
    friend = Account.objects.get(pk=pk)
    if operation == 'add':
        # if request.user.is_authenticated:
        #    button_status='friend_request_sent'
        #    user = get_object_or_404(Account.objects.filter(pk=pk))
        #    frequest, created = FriendRequest.objects.get_or_create(
        #		from_user=request.user,
        #		to_user=user)
        Friend.make_friend(request.user, friend)
    elif operation == 'remove':
        Friend.lose_friend(request.user, friend)
    return redirect('profile_page')


def view_profile(request, pk=None):
    form2 = forms.InvitaionForm()
    if request.method == 'POST':
        form2 = forms.InvitaionForm(request.POST)
        recepient = str(form2['Email'].value())
        send_mail('Hello from Sdate Project',
                  'Someone wants you to join our website! check it out at: https://127.0.0.1:8000', EMAIL_HOST_USER,
                  [recepient], fail_silently=False)
        return render(request, 'first_app/success.html')

    if pk:
        user = Account.objects.get(pk=pk)
    else:
        user = request.user
    args = {'user': user}
    return render(request, 'first_app/profile_info.html', args)


@csrf_exempt
def audio_data(request):
    if request.method == 'POST':

        # Authenticating API
        gmaps = googlemaps.Client(key='YOUR_API_KEY')

        # Calling google geocode API with query as a Address
        geocode_result = gmaps.geocode(request.POST['send'])

        # geocode_result will return a JSON, contents can be extracted
        # for example
        x = geocode_result[0]['geometry']['location']['lat']  # get latitute for the query
        y = geocode_result[0]['geometry']['location']['lng']  # get longitude for the query

    else:
        message = "Please check the POST call"
        return HttpResponse(message)


def detail_blog_view(request, pk):
    context = {}

    blog_post = get_object_or_404(Post.objects.filter(pk=pk))
    context['blog_post'] = blog_post
    #    context = blog_post
    return render(request, 'first_app/post_detail.html', context)


def create_blog_view(request):
    form = HomeForm(request.POST)
    if form.is_valid():
        post = form.save(commit=False)
        # author = Account.objects.filter(username=user.username).first()
        author = request.user
        post.user = request.user
        post.save()

        #    text = form.cleaned_data['post']
        form = HomeForm()
        return redirect('profile_page')
    args = {'form': form, }
    return render(request, 'first_app/create_post.html', args)


# context = {}

# user = request.user
# if not user.is_authenticated:
#	return redirect('must_authenticate')

# form = CreateBlogPostForm(request.POST)
# if form.is_valid():
#	obj = form.save(commit=False)
#	author = request.user
#	obj.author = author


#	obj.save()
#	form = CreateBlogPostForm()

# return redirect('profile_page')

# args = {'form': form, 'text': text}
# return render(request, 'first_app/profile_page.html', args)
#    return (request, 'profile_page', {})
# context['form'] = form


# return render(request, "first_app/create_post.html", context)

def edit_blog_view(request, pk):
    context = {}

    user = request.user
    if not user.is_authenticated:
        return redirect("must_authenticate")

    # post=Post.objects.get()
    blog_post = get_object_or_404(Post.objects.filter(pk=pk))
    # context['blog_post'] = blog_post
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
        initial={
            #	"title": blog_post.title,
            "text": blog_post.post,
            #	"image": blog_post.image,
        }
    )

    context['form'] = form
    return render(request, 'first_app/edit_post.html', context)


def search(request):
    user_list = Account.objects.all()
    user_filter = UserFilter(request.GET, queryset=user_list)
    friend = Friend.objects.get(current_user=request.user)
    friends = friend.users.all()

    return render(request, 'first_app/user_list.html', {'filter': user_filter})


def send_friend_request(request, pk):
    if request.user.is_authenticated:
        # button_status = 'friend_request_sent'
        # button_status='friend_request_sent'
        # button_status = 'friend_request_sent'
        user = get_object_or_404(Account.objects.filter(pk=pk))
        frequest, created = FriendRequest.objects.get_or_create(
            from_user=request.user,
            to_user=user)
        # button_status='friend_request_sent'
        return redirect('profile_page')


def cancel_friend_request(request, pk):
    if request.user.is_authenticated:
        user = get_object_or_404(Account.objects.filter(pk=pk))
        frequest = FriendRequest.objects.filter(
            from_user=request.user,
            to_user=user).first()
        frequest.delete()
        return redirect('profile_page')


def accept_friend_request(request, pk):
    from_user = get_object_or_404(Account.objects.filter(pk=pk))
    frequest = FriendRequest.objects.filter(from_user=from_user, to_user=request.user).first()
    user1 = frequest.to_user
    user2 = from_user
    Friend.make_friend(request.user, user2)
    Friend.make_friend(request.user, user1)
    frequest.delete()
    return redirect('profile_page')


def delete_friend_request(request, pk):
    from_user = get_object_or_404(Account.objects.filter(pk=pk))
    frequest = FriendRequest.objects.filter(from_user=from_user, to_user=request.user).first()
    frequest.delete()
    return redirect('profile_page')


def get_current_users():
    active_sessions = Session.objects.filter(expire_date__gte=timezone.now())
    user_id_list = []
    for session in active_sessions:
        data = session.get_decoded()
        user_id_list.append(data.get('_auth_user_id', None))
    # Query all logged in users based on id list
    return Account.objects.filter(id__in=user_id_list)


def like_post(request):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    # post = Post.objects.get(id=request.POST.get('post_id'))
    is_liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        is_liked = False

    else:
        post.likes.add(request.user)
        is_liked = True
    return HttpResponseRedirect(post.get_absolute_url())


#    return render (request, 'first_app/profile_page.html', {})

def deactivate(request):
    if request.method == 'POST':
        form = active_form(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = active_form(instance=request.user)
        args = {'form': form}
        return render(request, "first_app/deactivate.html", args)
from django.shortcuts import render, redirect, get_object_or_404
from s_date_project.settings import EMAIL_HOST_USER
from notify.signals import notify
from django.contrib.sessions.models import Session
from django.utils import timezone
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import \
    csrf_exempt  # This is to exclude the token authentication for the post request.
# should be resolved if needed
from braces.views import SelectRelatedMixin
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import Http404
from django.views import generic
from . import forms
from . import models
from .forms import RegistrationForm, AccountAuthenticationForm, AccountUpdateForm, HomeForm, UpdateBlogPostForm, \
    CreateBlogPostForm, InvitaionForm, active_form
from .models import BlogPost, Account, Post, Friend, FriendRequest
from .filters import UserFilter
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.template.loader import render_to_string
from django.views.generic import RedirectView

# VIEWS:
def friends(request):
    user_list = Account.objects.all()
    user_filter = UserFilter(request.GET, queryset=user_list)
    friend = Friend.objects.get(current_user=request.user)
    friends = friend.users.all().filter(is_active=True)
    x = Account.objects.count()
    y = friends.count()
    args = {
        'friends': friends, 'online_users': user_list, 'x': x, 'y': y,
    }
    return render(request, 'first_app/friends.html', args)


def news(request):
    return render(request, 'first_app/news.html')


def events(request):
    return render(request, 'first_app/events.html')


def first_article(request):
    return render(request, 'first_app/articles/first_article.html')


def second_article(request):
    return render(request, 'first_app/articles/second_article.html')


def registration_view(request):
    registered = False
    context = {}
    if request.POST:
        form = RegistrationForm(request.POST,request.FILES)
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

    return render(request, "first_app/log.html", context)


def account_view(request):
    if not request.user.is_authenticated:
        return redirect("user_login")
    form2 = forms.InvitaionForm()
    if request.method == 'POST':
        if request.POST.get("InvitaionForm"):
            form2 = forms.InvitaionForm(request.POST)
            recepient = str(form2['Email'].value())
            send_mail('Hello from Sdate Project',
                      'Someone wants you to join our website! check it out at: https://127.0.0.1:8000', EMAIL_HOST_USER,
                      [recepient], fail_silently=False)
            return render(request, 'first_app/success.html')

    context = {}
    if request.POST:
        form = AccountUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            if 'profile_pic' in request.FILES:
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
                    "profile_pic": request.FILES['profile_pic'],

                }
            else:
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
                }
            form.save()
            context['success_message'] = "Updated"

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

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home_page'))


def post(request):
    if request.POST:
        form = HomeForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
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
        x = Account.objects.filter(is_active=True).count()
        users = Account.objects.exclude(id=request.user.id)
        user = Account.objects.get(id=request.user.id)
        block_user_list = user.blocked.all()
        sent_friend_requests = FriendRequest.objects.filter(from_user=request.user)
        rec_friend_requests = FriendRequest.objects.filter(to_user=request.user)
        Friend.make_friend(current_user=request.user, new_friend=Account.objects.get(id=1))
        friend = Friend.objects.get(current_user=request.user)
        friends = friend.users.all().filter(is_active=True)

        active_sessions = Session.objects.filter(expire_date__gte=timezone.now())
        user_id_list = []
        for session in active_sessions:
            data = session.get_decoded()
            user_id_list.append(data.get('_auth_user_id', None))
        online_users = Account.objects.filter(id__in=user_id_list)

        args = {
            'form': form, 'posts': posts, 'users': users, 'x': x, 'block_user_list': block_user_list,
            'friends': friends, 'sent_friend_requests': sent_friend_requests,
             'rec_friend_requests': rec_friend_requests, 'online_users': online_users
        }
        return render(request, 'first_app/profile_page.html', args)


def change_friends(request, operation, pk):
    friend = Account.objects.get(pk=pk)
    from_user = get_object_or_404(Account.objects.filter(pk=pk))
    frequest = FriendRequest.objects.filter(from_user=from_user, to_user=request.user).first()

    if operation == 'add':
        Friend.make_friend(request.user, friend)
        Friend.make_friend(friend, request.user)
        frequest.delete()
    elif operation == 'remove':
        Friend.lose_friend(request.user, friend)
        Friend.lose_friend(friend, request.user)
    return redirect('profile_page')


def view_profile(request, pk=None):
    friend = Friend.objects.get(current_user=request.user)
    friends = friend.users.all()

    if pk:
        user = Account.objects.get(pk=pk)
        block_user_list = user.blocked.all()


    else:
        user = request.user
        block_user_list = user.blocked.all()
    args = {'user': user, 'friends': friends, 'total_likes': user.total_likes(), 'block_user_list': block_user_list, }
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

    return render(request, 'first_app/post_detail.html', context)


def create_blog_view(request):
    form = HomeForm(request.POST)
    if form.is_valid():
        post = form.save(commit=False)
        author = request.user
        post.user = request.user
        post.save()

        form = HomeForm()
        return redirect('profile_page')
    args = {'form': form, }
    return render(request, 'first_app/create_post.html', args)


def edit_blog_view(request, pk):
    context = {}

    user = request.user
    if not user.is_authenticated:
        return redirect("must_authenticate")
    blog_post = get_object_or_404(Post.objects.filter(pk=pk))
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
            "text": blog_post.post,
        }
    )

    context['form'] = form
    return render(request, 'first_app/edit_post.html', context)


def search(request):
    user_list = Account.objects.all().filter(is_active=True)
    user_filter = UserFilter(request.GET, queryset=user_list)
    friend = Friend.objects.get(current_user=request.user)
    friends = friend.users.all()
    return render(request, 'first_app/user_list.html', {'filter': user_filter, 'online_users': user_list})

def send_friend_request(request, pk):
    if request.user.is_authenticated:
        user = get_object_or_404(Account.objects.filter(pk=pk))
        user2 = request.user.firstname + ' ' + request.user.lastname
        notify.send(request.user, recipient=user, actor_text=user2, verb='sent you friend request', nf_type='default')
        frequest, created = FriendRequest.objects.get_or_create(from_user=request.user, to_user=user)
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


def like_post(request):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    user = request.user.firstname + ' ' + request.user.lastname
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        notify.send(request.user, recipient=post.user, actor_text=user, verb='removed his like from your post',
                    nf_type='default')

    else:
        post.likes.add(request.user)
        notify.send(request.user, recipient=post.user, actor_text=user, verb='liked your post', nf_type='default')
    return HttpResponseRedirect(post.get_absolute_url())


def like_user(request):
    request_user = get_object_or_404(Account, id=request.POST.get('user_id'))
    user = request.user.firstname + ' ' + request.user.lastname
    if request_user.likes.filter(id=request.user.id).exists():
        request_user.likes.remove(request.user)

    else:
        request_user.likes.add(request.user)
        notify.send(request.user, recipient=request_user, actor_text=user, verb='liked your profile', nf_type='default')
    return HttpResponseRedirect(request_user.get_absolute_url())


def block_user(request, operation, pk):
    request_user = Account.objects.get(pk=pk)
    if operation == 'remove':
        request.user.blocked.remove(request_user)

    elif operation == 'add':
        request.user.blocked.add(request_user)
    return HttpResponseRedirect(request_user.get_absolute_url())


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

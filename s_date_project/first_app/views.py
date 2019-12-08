from django.shortcuts import render
from first_app.forms import UserForm, UserProfileInfoForm
# from django.contrib.auth.models import auth, User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm


# Create your views here.

def index(request):
    return render(request, 'first_app/home_page.html')


def base(request):
    return render(request, 'first_app/base.html')


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home_page'))


@login_required
def special(request):
    return HttpResponse("You are logged in!")


def register(request):
    registered = False

    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():

            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()

            registered = True
        else:
            print(user_form.errors, profile_form.errors)

    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm

    return render(request, 'first_app/reg_page.html',
                  {'user_form': user_form,
                   'profile_form': profile_form,
                   'registered': registered})


"""
def user_login(request):
    if request.method == 'POST':
        username=request.POST['username']
        password=request.POST['password']

        user = auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request,user)
            return redirect("/")
        else:
            messages.info(request,"Invalid credentials")
            return redirect('user_login')
    else:
         return render(request,'first_app/log.html')

"""


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # user = auth.authenticate(username=username, password=password)
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('base'))

            else:
                return HttpResponse("ACCOUNT NOT ACTIVE")

        else:
            print("someone tried to login and failed")
            print("Username: {} and password: {}".format(username, password))
            return HttpResponse("Invalid login details supplied")
    else:
        return render(request, 'first_app/registration/login.html', {})

# from django import forms
from django.contrib.auth.models import User
# from first_app.models import MyAccountManager, Account
# from first_app import models

from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import authenticate

from .models import Account, Post


class InvitaionForm(forms.Form):
    Email = forms.EmailField(max_length=254, help_text='Required. Add a valid email address.')

    def __str__(self):
        return self.Email


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Add a valid email address.')

    class Meta:
        model = Account
        fields = (
            'email', 'username', 'password1', 'password2', 'firstname', 'lastname', 'country', 'city', 'birthdate',
            'disabillity', 'hobbies', 'profile_pic')


class AccountAuthenticationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ('email', 'password')

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            if not authenticate(email=email, password=password):
                raise forms.ValidationError("Invalid login")


class AccountUpdateForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = (
            'email', 'username', 'firstname', 'lastname', 'country', 'city', 'birthdate', 'disabillity', 'hobbies',
            'profile_pic', 'is_active')

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            account = Account.objects.exclude(pk=self.instance.pk).get(email=email)
        except Account.DoesNotExist:
            return email
        raise forms.ValidationError('Email "%s" is already in use.' % account)

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            account = Account.objects.exclude(pk=self.instance.pk).get(username=username)
        except Account.DoesNotExist:
            return username
        raise forms.ValidationError('Username "%s" is already in use.' % username)


class HomeForm(forms.ModelForm):
    post = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Write something to post...'
        }
    ))

    class Meta:
        model = Post
        fields = ('post',)


class UpdateBlogPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['post', ]

    def save(self, commit=True):
        blog_post = self.instance
        # blog_post.title = self.cleaned_data['title']
        blog_post.post = self.cleaned_data['post']

        #	if self.cleaned_data['image']:
        #		blog_post.image = self.cleaned_data['image']

        if commit:
            blog_post.save()
        return blog_post


class CreateBlogPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['post', ]


# class UserForm(forms.ModelForm):
#    password = forms.CharField(widget=forms.PasswordInput())

#    class Meta():
#        model = MyAccountManager
#        fields = ('username','email','password')

# class UserProfileInfoForm(forms.ModelForm):
#    class Meta():
#        model = UserProfileInfo
#        fields = ('profile_pic', )

# class PostForm(forms.ModelForm):
#    class Meta:
#        fields = ('message',)
#        model = models.Post

#    def __init__(self, *args, **kwargs):
#        user = kwargs.pop("user", None)
#        super().__init__(*args, **kwargs)
# if user is not None:
#    self.fields["group"].queryset = (
#        models.Group.objects.filter(
#            pk__in=user.groups.values_list("group__pk")
#        )
#    )

class active_form(AccountUpdateForm):
    class Meta:
        model = Account
        fields = ('is_active',)

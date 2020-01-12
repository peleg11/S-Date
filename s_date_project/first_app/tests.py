from django.test import TestCase, Client
from django.contrib.auth import get_user_model,authenticate
from first_app import admin
from first_app.models import Friend, Post, FriendRequest, BlogPost, Account
from django.db import models
from django.test import RequestFactory
from django.urls import reverse
from first_app import views
import json
from django.utils import timezone
from django.contrib.sessions.models import Session
# test for deleting user
class DeleteUserCase(TestCase):

    # create regular user and admin user to show the different priviliges and add them to test's database
    def setUp(self):

        self.user = get_user_model().objects.create_user(username='regularuser', password='12test12', email='regularuser@example.com', firstname='user', lastname='user', country= 'country', city='city', birthdate= '2000-10-20', disabillity= 'disabillity', hobbies='hobbies', is_sponsor=False,profile_pic='profile_pic')
        self.user.save()

        self.adminuser = get_user_model().objects.create_superuser(username='adminuser', password='admin', email='adminuser@example.com', firstname='user', lastname='user', country= 'country', city='city', birthdate= '2000-10-20', disabillity= 'disabillity', hobbies='hobbies', is_sponsor=False,profile_pic='profile_pic')
        self.adminuser.save()

    # deleting the users from test's database
    def tearDown(self):
        self.user.delete()
        self.adminuser.delete()

    # function to check if regular user has premission to delete user. suppose to return False.
    def test_ForRegularUser(self):
        self.assertTrue(self.user.has_perm('auth.delete_userprofileinfo'))

    # function to check if admin user has premission to delete user. suppose to return True.
    def test_ForAdminUser(self):
        self.assertTrue(self.adminuser.has_perm('auth.delete_userprofileinfo'))

# test for view user in website database

class ViewUserCase(TestCase):

    # create regular user and admin user to show the different priviliges and add them to test's database
    def setUp(self):

        self.user = get_user_model().objects.create_user(username='regularuser', password='12test12', email='regularuser@example.com', firstname='user', lastname='user', country= 'country', city='city', birthdate= '2000-10-20', disabillity= 'disabillity', hobbies='hobbies', is_sponsor=False,profile_pic='profile_pic')
        self.user.save()

        self.adminuser = get_user_model().objects.create_superuser(username='adminuser', password='admin', email='adminuser@example.com', firstname='user', lastname='user', country= 'country', city='city', birthdate= '2000-10-20', disabillity= 'disabillity', hobbies='hobbies',is_sponsor=False, profile_pic='profile_pic')
        self.adminuser.save()

    # deleting the users from test's database
    def tearDown(self):
        self.user.delete()
        self.adminuser.delete()

    # function to check if regular user has premission to view user delails in database. suppose to return False.
    def test_ForRegularUser(self):
        self.assertTrue(self.user.has_perm('auth.view_userprofileinfo'))

    # function to check if admin user has premission to view user delails in database. suppose to return True.
    def test_ForAdminUser(self):
        self.assertTrue(self.adminuser.has_perm('auth.view_userprofileinfo'))


# test for login user to website

class SigninTest(TestCase):

    # create regular user and  and add it to test's database
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='test', password='12test12', email='test@example.com', firstname='user', lastname='user', country= 'country', city='city', birthdate= '2000-10-20', disabillity= 'disabillity', hobbies='hobbies', is_sponsor=False,profile_pic='profile_pic')
        self.user.save()

    # deleting the user from test's database
    def tearDown(self):
        self.user.delete()

    # test if can sign in with correct username and password. suppose to turn True.
    def test_correct(self):
        user = authenticate(username='test', password='12test12')
        self.assertTrue((user is not None) and user.is_authenticated)

    # test if can sign in with wrong username. suppose to turn False.
    def test_wrong_username(self):
        user = authenticate(username='wrong', password='12test12')
        self.assertTrue(user is not None and user.is_authenticated)

    # test if can sign in with wrong password. suppose to turn False.
    def test_wrong_pssword(self):
        user = authenticate(username='test', password='wrong')
        self.assertTrue(user is not None and user.is_authenticated)


class TestUserMethods(TestCase):

    # create 2 useres
    def setUp(self):
        self.user1 = Account.objects.create(username='user1', password='12test12', email='user1@example.com', firstname='user', lastname='user', country= 'country', city='city', birthdate= '2000-10-20 00:00:00+00:00', disabillity= 'disabillity', hobbies='hobbies', is_sponsor=False,profile_pic='profile_pic')
        self.user2 = get_user_model().objects.create_user(username='user2', password='12test12', email='user2@example.com', firstname='user', lastname='user', country= 'country', city='city', birthdate= '2000-10-20 00:00:00+00:00', disabillity= 'disabillity', hobbies='hobbies', is_sponsor=False,profile_pic='profile_pic')
        self.user3 = Account.objects.create(username='user3', password='12test12', email='user3@example.com', firstname='user', lastname='user', country= 'country', city='city', birthdate= '2000-10-20 00:00:00+00:00', disabillity= 'disabillity', hobbies='hobbies', is_sponsor=False,profile_pic='profile_pic')



        self.user2.save()
        self.user1.save()
        # add user2 to user1 like's list
        self.user1.likes.add(self.user2)
        # add user2 to user1 blocked's list
        self.user1.blocked.add(self.user2)
        # add user2 to user1 friend's list and user1 to user2 friend's list
        Friend.make_friend(self.user1,self.user2)
        Friend.make_friend(self.user2,self.user1)
        #add user3 to user1 friend's list and then remove him
        Friend.make_friend(self.user1,self.user3)
        Friend.lose_friend(self.user1,self.user3)

    def test_like_friend(self):
        self.assertTrue(self.user1.likes.filter(id=self.user2.id).exists())

    def test_blocked_friend(self):
        self.assertTrue(self.user1.blocked.filter(id=self.user2.id).exists())

    def test_add_friend(self):
        self.assertTrue(Friend.objects.get(current_user=self.user1).users.filter(id=self.user2.id).exists())
        self.assertTrue(Friend.objects.get(current_user=self.user2).users.filter(id=self.user1.id).exists())

    def test_remove_friend(self): # will return false because we removed user1 from user1 friend's list
        self.assertTrue(Friend.objects.get(current_user=self.user1).users.filter(id=self.user3.id).exists())

"""
    def test_view_profile_GET(self):
        client = Client()

        response = client.get(reverse('view_profile'))

        self.assrtEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'first_app/profile_info.html')
"""

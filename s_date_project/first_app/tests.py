from django.test import TestCase
from django.contrib.auth import get_user_model,authenticate
from first_app import admin
from django.db import models
from django.test import RequestFactory

# test for deleting user

class DeleteUserCase(TestCase):

    # create regular user and admin user to show the different priviliges and add them to test's database
    def setUp(self):

        self.user = get_user_model().objects.create_user(username='regularuser', password='12test12', email='regularuser@example.com')
        self.user.save()

        self.adminuser = get_user_model().objects.create_superuser(username='adminuser', password='admin', email='adminuser@example.com')
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

        self.user = get_user_model().objects.create_user(username='regularuser', password='12test12', email='regularuser@example.com')
        self.user.save()

        self.adminuser = get_user_model().objects.create_superuser(username='adminuser', password='admin', email='adminuser@example.com')
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
        self.user = get_user_model().objects.create_user(username='test', password='12test12', email='test@example.com')
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

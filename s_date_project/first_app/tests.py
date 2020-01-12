from django.test import TestCase, Client
from django.contrib.auth import get_user_model, authenticate
from . import admin
from .models import Friend, Post, FriendRequest, BlogPost, Account
from django.db import models
from django.test import RequestFactory
from django.urls import reverse
from . import views
import json
from django.utils import timezone
from django.contrib.sessions.models import Session
from notify.models import Notification
from notify.signals import notify
import os

# from django.conf import settings
from django.template import Context, Template
from django.test import override_settings


# test for deleting user
class DeleteUserCase(TestCase):

    # create regular user and admin user to show the different priviliges and add them to test's database
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='regularuser', password='12test12',
                                                         email='regularuser@example.com', firstname='user',
                                                         lastname='user', country='country', city='city',
                                                         birthdate='2000-10-20', disabillity='disabillity',
                                                         hobbies='hobbies', is_sponsor=False, profile_pic='profile_pic')
        self.user.save()

        self.adminuser = get_user_model().objects.create_superuser(username='adminuser', password='admin',
                                                                   email='adminuser@example.com', firstname='user',
                                                                   lastname='user', country='country', city='city',
                                                                   birthdate='2000-10-20', disabillity='disabillity',
                                                                   hobbies='hobbies', is_sponsor=False,
                                                                   profile_pic='profile_pic')
        self.adminuser.save()

    # deleting the users from test's database
    def tearDown(self):
        self.user.delete()
        self.adminuser.delete()

    # function to check if regular user has premission to delete user. suppose to return False.
    def test_ForRegularUser(self):
        self.assertFalse(self.user.has_perm('auth.delete_userprofileinfo'))

    # function to check if admin user has premission to delete user. suppose to return True.
    def test_ForAdminUser(self):
        self.assertTrue(self.adminuser.has_perm('auth.delete_userprofileinfo'))


# test for view user in website database

class ViewUserCase(TestCase):

    # create regular user and admin user to show the different priviliges and add them to test's database
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='regularuser', password='12test12',
                                                         email='regularuser@example.com', firstname='user',
                                                         lastname='user', country='country', city='city',
                                                         birthdate='2000-10-20', disabillity='disabillity',
                                                         hobbies='hobbies', is_sponsor=False, profile_pic='profile_pic')
        self.user.save()

        self.adminuser = get_user_model().objects.create_superuser(username='adminuser', password='admin',
                                                                   email='adminuser@example.com', firstname='user',
                                                                   lastname='user', country='country', city='city',
                                                                   birthdate='2000-10-20', disabillity='disabillity',
                                                                   hobbies='hobbies', is_sponsor=False,
                                                                   profile_pic='profile_pic')
        self.adminuser.save()

    # deleting the users from test's database
    def tearDown(self):
        self.user.delete()
        self.adminuser.delete()

    # function to check if regular user has premission to view user delails in database. suppose to return False.
    def test_ForRegularUser(self):
        self.assertFalse(self.user.has_perm('auth.view_userprofileinfo'))

    # function to check if admin user has premission to view user delails in database. suppose to return True.
    def test_ForAdminUser(self):
        self.assertTrue(self.adminuser.has_perm('auth.view_userprofileinfo'))


# test for login user to website

class SigninTest(TestCase):

    # create regular user and  and add it to test's database
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='test', password='12test12', email='test@example.com',
                                                         firstname='user', lastname='user', country='country',
                                                         city='city', birthdate='2000-10-20', disabillity='disabillity',
                                                         hobbies='hobbies', is_sponsor=False, profile_pic='profile_pic')
        self.user.save()

    # deleting the user from test's database
    def tearDown(self):
        self.user.delete()

    # test if can sign in with correct username and password. suppose to turn True.
    def test_correct(self):
        user = authenticate(username='test@example.com', password='12test12')
        self.assertTrue((user is not None) and user.is_authenticated)

    # test if can sign in with wrong username. suppose to turn False.
    def test_wrong_username(self):
        user = authenticate(username='wrong', password='12test12')
        self.assertFalse(user is not None and user.is_authenticated)

    # test if can sign in with wrong password. suppose to turn False.
    def test_wrong_pssword(self):
        user = authenticate(username='test', password='wrong')
        self.assertFalse(user is not None and user.is_authenticated)


class TestUserMethods(TestCase):

    # create 2 useres
    def setUp(self):
        self.user1 = Account.objects.create(username='user1', password='12test12', email='user1@example.com',
                                            firstname='user', lastname='user', country='country', city='city',
                                            birthdate='2000-10-20 00:00:00+00:00', disabillity='disabillity',
                                            hobbies='hobbies', is_sponsor=False, profile_pic='profile_pic')
        self.user2 = get_user_model().objects.create_user(username='user2', password='12test12',
                                                          email='user2@example.com', firstname='user', lastname='user',
                                                          country='country', city='city',
                                                          birthdate='2000-10-20 00:00:00+00:00',
                                                          disabillity='disabillity', hobbies='hobbies',
                                                          is_sponsor=False, profile_pic='profile_pic')
        self.user3 = Account.objects.create(username='user3', password='12test12', email='user3@example.com',
                                            firstname='user', lastname='user', country='country', city='city',
                                            birthdate='2000-10-20 00:00:00+00:00', disabillity='disabillity',
                                            hobbies='hobbies', is_sponsor=False, profile_pic='profile_pic')

        self.user2.save()
        self.user1.save()
        # add user2 to user1 like's list
        self.user1.likes.add(self.user2)
        # add user2 to user1 blocked's list
        self.user1.blocked.add(self.user2)
        # add user2 to user1 friend's list and user1 to user2 friend's list
        Friend.make_friend(self.user1, self.user2)
        Friend.make_friend(self.user2, self.user1)
        # add user3 to user1 friend's list and then remove him
        Friend.make_friend(self.user1, self.user3)
        Friend.lose_friend(self.user1, self.user3)

    def test_like_friend(self):
        self.assertTrue(self.user1.likes.filter(id=self.user2.id).exists())

    def test_blocked_friend(self):
        self.assertTrue(self.user1.blocked.filter(id=self.user2.id).exists())

    def test_add_friend(self):
        self.assertTrue(Friend.objects.get(current_user=self.user1).users.filter(id=self.user2.id).exists())
        self.assertTrue(Friend.objects.get(current_user=self.user2).users.filter(id=self.user1.id).exists())

    def test_remove_friend(self):  # will return false because we removed user1 from user1 friend's list
        self.assertFalse(Friend.objects.get(current_user=self.user1).users.filter(id=self.user3.id).exists())


"""
    def test_view_profile_GET(self):
        client = Client()

        response = client.get(reverse('view_profile'))

        self.assrtEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'first_app/profile_info.html')
"""


class deactivate_user_case(TestCase):

    # create regular with is_active attribute to false and test if he can login website
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='test@example.com', password='12test12',
                                                         email='regularuser@example.com', firstname='user',
                                                         lastname='user', country='country', city='city',
                                                         birthdate='2000-10-20', disabillity='disabillity',
                                                         hobbies='hobbies', is_sponsor=False, profile_pic='profile_pic')
        self.user.save()
        self.user.is_active = False

    # deleting the users from test's database
    def tearDown(self):
        self.user.delete()

    # function to check if user can login while hes account is deactivated, suppose to return false
    def test_deactivate_login(self):
        user = authenticate(username='test@example.com', password='12test12')
        self.assertFalse((user is not None) and user.is_authenticated)


# --------------------notify test----------------

try:
    from django.core.urlresolvers import reverse
except ImportError:
    from django.urls import reverse

import json
from django.template import Template, Context, RequestContext
from django.test.client import RequestFactory
from django.contrib.auth.models import AnonymousUser

User = get_user_model()


class NotificationManagerTest(TestCase):

    def setUp(self):
        self.recipient = User.objects.create(username='recipient',
                                             email='recipient@test.com',
                                             password='pwd@recipient')
        self.actor = User.objects.create(username='actor',
                                         email='actor@test.com',
                                         password='pwd@actor')
        self.nf_count = 10

        self.assertEqual(self.recipient.id, 1)
        self.assertEqual(self.actor.id, 2)

        for x in range(self.nf_count):
            notify.send(User, recipient=self.recipient, actor=self.actor,
                        verb='followed you')

    def test_unread(self):
        self.assertEqual(Notification.objects.unread().count(), self.nf_count)
        nf = Notification.objects.filter(recipient=self.recipient).first()
        nf.mark_as_read()
        self.assertEqual(Notification.objects.unread().count(),
                         self.nf_count - 1)

        for n in Notification.objects.unread():
            self.assertFalse(n.read)

    def test_read(self):
        self.assertEqual(Notification.objects.unread().count(), self.nf_count)
        nf = Notification.objects.filter(recipient=self.recipient).first()
        nf.mark_as_read()
        self.assertEqual(Notification.objects.read().count(), 1)

        for n in Notification.objects.read():
            self.assertTrue(n.read)

    def test_read_all(self):
        self.assertEqual(Notification.objects.unread().count(), self.nf_count)
        recipient_nfs = Notification.objects.filter(recipient=self.recipient)
        recipient_nfs.read_all()

        self.assertEqual(Notification.objects.read().count(), self.nf_count)
        self.assertEqual(Notification.objects.unread().count(), 0)

    def test_unread_all(self):
        self.assertEqual(Notification.objects.unread().count(), self.nf_count)

        recipient_nfs = Notification.objects.filter(recipient=self.recipient)
        recipient_nfs.read_all()

        self.assertEqual(Notification.objects.read().count(), self.nf_count)
        self.assertEqual(Notification.objects.unread().count(), 0)

        recipient_nfs.unread_all()

        self.assertEqual(Notification.objects.read().count(), 0)
        self.assertEqual(Notification.objects.unread().count(), self.nf_count)

    def test_delete_all_soft(self):
        self.assertEqual(Notification.objects.unread().count(), self.nf_count)

        nf = Notification.objects.filter(recipient=self.recipient).first()
        # Mark single notification as read
        nf.mark_as_read()

        self.assertEqual(Notification.objects.read().count(), 1)
        self.assertEqual(Notification.objects.unread().count(),
                         self.nf_count - 1)

        self.assertEqual(Notification.objects.active().count(), self.nf_count)
        self.assertEqual(Notification.objects.deleted().count(), 0)

        Notification.objects.delete_all()
        # Mark all as deleted
        self.assertEqual(Notification.objects.read().count(), 0)
        self.assertEqual(Notification.objects.unread().count(), 0)
        self.assertEqual(Notification.objects.active().count(), 0)
        self.assertEqual(Notification.objects.deleted().count(), self.nf_count)

        Notification.objects.active_all()
        # Mark all as active
        self.assertEqual(Notification.objects.read().count(), 1)
        self.assertEqual(Notification.objects.unread().count(),
                         self.nf_count - 1)
        self.assertEqual(Notification.objects.active().count(), self.nf_count)
        self.assertEqual(Notification.objects.deleted().count(), 0)

    #    @override_settings(NOTIFY_SOFT_DELETE=False)
    def test_delete_all_hard(self):
        self.assertEqual(Notification.objects.active().count(), self.nf_count)


class NotificationTest(TestCase):

    def setUp(self):
        self.no_of_users = 10

        users = []
        for i in range(self.no_of_users):
            users.append(
                User(username='user-%r' % i, password='pwd@user%r' % i,
                     email='user%r@test.com' % i, firstname='user', lastname='user', country='country', city='city',
                     birthdate='2000-10-20 00:00:00+00:00', disabillity='disabillity', hobbies='hobbies',
                     is_sponsor=False, profile_pic='profile_pic'))
        User.objects.bulk_create(users)
        # actor = Account.objects.create_user(username='actor', email='actor@test.com', password='pwd@actor' ,
        # firstname='user', lastname='user', country= 'country', city='city', birthdate= '2000-10-20', disabillity=
        # 'disabillity', hobbies='hobbies', is_sponsor=False,profile_pic='profile_pic')

        self.actor = User.objects.create(username='actor', email='actor@test.com', password='pwd@actor',
                                         firstname='user', lastname='user', country='country', city='city',
                                         birthdate='2000-10-20 00:00:00+00:00', disabillity='disabillity',
                                         hobbies='hobbies', is_sponsor=False, profile_pic='profile_pic')

        self.recipient = User.objects.get(username='user-0')
        self.recipient_list = User.objects.filter(
            username__startswith='u').order_by('id')

    def test_created_users(self):
        users = User.objects.all()
        self.assertEqual(users.count(), self.no_of_users + 1)
        self.assertEqual(self.recipient_list.count(), self.no_of_users)

    def test_single_user_notify(self):
        notify.send(User, recipient=self.recipient, actor=self.actor,
                    verb='poked you')
        notification = Notification.objects.get(pk=1)
        self.assertEqual(notification.recipient_id, self.recipient.id)
        timedelta = timezone.now() - notification.created
        self.assertLessEqual(timedelta.seconds, 60)

    def test_multiple_user_notify(self):
        notify.send(User, recipient_list=list(self.recipient_list),
                    actor=self.actor, verb='uploaded a new video')
        notifications = Notification.objects.filter(verb__startswith='u')
        self.assertEqual(notifications.count(), self.no_of_users)

        username_list = [u.username for u in self.recipient_list]

        for nf in notifications:
            self.assertIn(nf.recipient.username, username_list)
            timedelta = timezone.now() - nf.created
            self.assertLessEqual(timedelta.seconds, 60)


# ------------------messages-------------------
import os

# from django.conf import settings
from django.template import Context, Template
from django.test import override_settings

from pinax.messages.forms import NewMessageForm, NewMessageFormMultiple
from pinax.messages.hooks import hookset
from pinax.messages.models import Message, Thread
from pinax.messages.tests.test import TestCase


class TestCaseMixin(object):
    User = get_user_model()

    def assert_renders(self, tmpl, context, value):
        tmpl = Template(tmpl)
        self.assertEqual(tmpl.render(context).strip(), value)


class BaseTest(TestCase, TestCaseMixin):
    def setUp(self):
        self.brosner = self.User.objects.create(username='brosner', email='actor1@test.com', password='1pwd@actor',
                                         firstname='user', lastname='user', country='country', city='city',
                                         birthdate='2000-10-20 00:00:00+00:00', disabillity='disabillity',
                                         hobbies='hobbies', is_sponsor=False, profile_pic='profile_pic')
        self.jtauber = self.User.objects.create(username='jtauber', email='actor2@test.com', password='2pwd@actor',
                                         firstname='user', lastname='user', country='country', city='city',
                                         birthdate='2000-10-20 00:00:00+00:00', disabillity='disabillity',
                                         hobbies='hobbies', is_sponsor=False, profile_pic='profile_pic')


class TestMessages(BaseTest):
    def test_message_methods(self):
        """
        Test Message and Thread methods.
        """
        message_string = "You can't be serious"
        Message.new_message(
            self.brosner, [self.jtauber], "Really?", message_string)

        self.assertEqual(Thread.inbox(self.brosner).count(), 0)
        self.assertEqual(Thread.inbox(self.jtauber).count(), 1)
        self.assertEqual(Thread.unread(self.jtauber).count(), 1)

        thread = Thread.inbox(self.jtauber)[0]

        Message.new_reply(thread, self.jtauber, "Yes, I am.")

        self.assertEqual(Thread.inbox(self.brosner).count(), 1)
        # Replier's inbox count is unchanged but unread is decremented.
        self.assertEqual(Thread.inbox(self.jtauber).count(), 1)
        self.assertEqual(Thread.unread(self.jtauber).count(), 0)

        Message.new_reply(thread, self.brosner, "If you say so...")
        reply_string = "Indeed I do"
        Message.new_reply(thread, self.jtauber, reply_string)

        self.assertNotEquals(
            Thread.objects.get(pk=thread.pk).latest_message.content,
            reply_string)
        self.assertEqual(
            Thread.objects.get(pk=thread.pk).first_message.content,
            message_string)

from django.contrib import admin
#from first_app.models import UserProfileInfo
# Register your models here.
from . import models

#admin.site.register(UserProfileInfo)
admin.site.register(models.Account)
admin.site.register(models.Post)
admin.site.register(models.Friend)
admin.site.register(models.FriendRequest)

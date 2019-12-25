"""s_date_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import include
from django.urls import path
from first_app import views
from django.conf import settings
from django.conf.urls.static import static
#from first_app.views import show_profile

urlpatterns = [
    url(r'^$',views.index,name='home_page'),
    url(r'^first_app/',include('first_app.urls')),
    url(r'^logout/$',views.user_logout,name='logout'),
    url(r'special/',views.special, name='special'),
    #url(r'^user_login/$',views.base, name='base'),
    url(r'^user_login/$', views.login_view, name='user_login'),
    #url(r'^profile_page/$', views.profile, name='profile_page'),
    url(r'^profile_page/$', views.post, name='profile_page'),
    path('admin/', admin.site.urls),
    url(r'^settings/$', views.account_view, name='profile_settings'),
    #url(,views.,name='post_detail')
    url(r'^post_detail/(?P<pk>\d+)/$', views.detail_blog_view, name="post_detail"),
    path('create/', views.create_blog_view, name="create_post"),
    url(r'^edit/(?P<pk>\d+)/$', views.edit_blog_view, name="edit_post"),
    #url(r'^events/$', views.events, name='events_page'),
    path('', include('django.contrib.auth.urls')),
    url(r'^register/$', views.registration_view, name='reg_page'),
    url(r'^profile/$', views.view_profile, name='view_profile'),
    url(r'^profile/(?P<pk>\d+)/$', views.view_profile, name='view_profile_with_pk'),
     url(r'^connect/(?P<operation>.+)/(?P<pk>\d+)/$', views.change_friends, name='change_friends')
#    path('events/',show_profile),
    # POSTS:
    #url(r"^posts/", name="posts"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

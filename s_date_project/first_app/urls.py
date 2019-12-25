from django.conf.urls import url
from first_app import views

app_name = 'first_app'

urlpatterns = [
    url(r'^register/$', views.registration_view, name='reg_page'),
    url(r'^$',views.index,name='home_page'),
    url(r'^user_login/$', views.login_view, name='user_login'),
    url(r'^$',views.base, name='base'),
    url(r'^profile/$', views.view_profile, name='view_profile'),
    url(r'^profile/(?P<pk>\d+)/$', views.view_profile, name='view_profile_with_pk'),
    url(r'^settings/$', views.account_view, name='profile_settings'),
#    url(r'^profile_page/$', views.post, name='profile_page'),
    #url(r'^events/$', views.events, name='events_page'),
    #"""#POSTS:
    #url(r"^$", views.PostList.as_view(), name="all"),
    #url(r"new/$", views.CreatePost.as_view(), name="create"),
    #url(r"by/(?P<username>[-\w]+)/$",views.UserPosts.as_view(),name="for_user"),
    #url(r"by/(?P<username>[-\w]+)/(?P<pk>\d+)/$",views.PostDetail.as_view(),name="single"),
    #url(r"delete/(?P<pk>\d+)/$",views.DeletePost.as_view(),name="delete"),
    #"""
]

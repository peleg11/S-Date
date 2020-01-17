from django.conf.urls import url
from . import views
from django.urls import path

app_name = 'first_app'

urlpatterns = [
    url(r'^register/$', views.registration_view, name='reg_page'),
    url(r'^$', views.index, name='home_page'),
    url(r'^user_login/$', views.login_view, name='user_login'),
    url(r'^$', views.base, name='base'),
    url(r'^profile/$', views.view_profile, name='view_profile'),
    url(r'^profile/(?P<pk>\d+)/$', views.view_profile, name='view_profile_with_pk'),
    url(r'^settings/$', views.account_view, name='profile_settings'),
    url(r'^news/$', views.news, name='news'),
    url(r'^events/$', views.events, name='events'),
    path('deactivate/', views.deactivate, name='deactivate'),
]

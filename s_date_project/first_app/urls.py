from django.conf.urls import url
from first_app import views

app_name = 'first_app'

urlpatterns = [
    url(r'^register/$', views.register, name='reg_page'),
    url(r'^$',views.index,name='home_page'),
    url(r'^user_login/$', views.user_login, name='user_login'),
    url(r'^$',views.base, name='base'),
    url(r'^$', views.profile, name='profile_page'),
]

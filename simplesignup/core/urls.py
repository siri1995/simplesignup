from django.conf.urls import url, include
from django.contrib.auth import views as auth_views

from core import views as core_views
from core.views import *




urlpatterns = {
    url(r'^$', core_views.home, name='home'),
    url(r'^login/$', auth_views.login, {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': 'login'}, name='logout'),
    url(r'^register/$', core_views.registerationform, name='register'),



}
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.loggedIn, name="da_logged_in"),
    url(r'^home$', views.home, name = "da_home"),
    url(r'^profile/(?P<id>\d+)$', views.profilePage, name = 'da_profile'),
]

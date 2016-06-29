from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.loggedIn, name="da_logged_in"),
    url(r'^home$', views.home, name = "da_home"),
    url(r'^profile/(?P<id>\d+)$', views.profilePage, name = 'da_profile'),
    url(r'^profile/update/(?P<id>\d+)$', views.update_profile, name = 'da_update'),
    url(r'^questionaire/(?P<id>\d+)$', views.questionaire_page, name = 'da_question')

]

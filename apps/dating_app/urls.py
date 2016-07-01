from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.loggedIn, name="da_logged_in"),
    url(r'^home$', views.home, name = "da_home"),
    url(r'^profile/(?P<id>\d+)$', views.profilePage, name = 'da_profile'),
    url(r'^profile/update/$', views.update_profile, name = 'da_update'),
    url(r'^questionnaire/(?P<id>\d+)$', views.questionnaire_page, name = 'da_question'),
    url(r'^questionnaire/submit$', views.submit_questionnaire, name='da_q_submit'),
    url(r'^hoot$', views.find_match, name='da_hoot'),
    url(r'^waiting$', views.wait, name='da_waiting'),
    url(r'^endchat$', views.end_match, name='da_end_chat'),
]

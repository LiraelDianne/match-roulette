from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name = "rl_index"),
    url(r'^login$', views.login, name = "rl_login"),
    url(r'^register$', views.register, name = "rl_register"),
    url(r'^reset$', views.reset, name = "rl_reset"),
]
#url(r'^this_app/(?P<id>[0-9]+)/edit$', views.edit, name = 'my_edit'),

#url(r'comments/(?:page-(?P<page_number>\d+)/)?$', comments)

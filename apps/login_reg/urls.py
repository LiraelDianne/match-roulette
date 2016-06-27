from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name = "br_index"),
    url(r'^login$', views.login, name = "br_login"),
    url(r'^register$', views.register, name = "br_register"),
    url(r'^reset$', views.reset, name = "br_reset"),
    url(r'^home$', views.home, name = "br_home"),
]
#url(r'^this_app/(?P<id>[0-9]+)/edit$', views.edit, name = 'my_edit'),

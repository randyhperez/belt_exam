from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^travels/$', views.dashboard, name='dashboard'),
    url(r'^add/$', views.tripform, name='tripform'),
    url(r'^addTrip/$', views.addTrip, name='addTrip'),
    url(r'^destination/(?P<id>\d+)$', views.destination, name='destination'),
    url(r'^verifyJoin/(?P<id>\d+)$', views.verifyJoin, name='verifyJoin'),
    url(r'^join/(?P<id>\d+)$', views.joinTrip, name='joinTrip'),
    url(r'^verifyDelete/(?P<id>\d+)$', views.verifyDelete, name='verifyDelete'),
    url(r'^deleteTrip/(?P<id>\d+)$', views.deleteTrip, name='deleteTrip'),
]

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^log_reg/$', views.log_reg, name='log_reg'),
    url(r'^logout/$', views.logout, name='logout'),
]

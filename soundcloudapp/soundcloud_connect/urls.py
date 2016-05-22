from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^connect/', views.connect, name='connect'),
	url(r'^callback/', views.callback, name='callback'),
]
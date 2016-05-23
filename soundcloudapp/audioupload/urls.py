from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^upload/$', views.upload, name='upload'),
	url(r'^upload/success/$', views.success, name='success'),
	url(r'^upload/success/download/$', views.download_song, name='download')
]
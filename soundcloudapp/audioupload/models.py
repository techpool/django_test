from django.db import models
from soundcloud_connect.models import Soundcloud_User

# Create your models here.
class Userdata(models.Model):
	"""docstring for Userdata"""
	user = models.OneToOneField(Soundcloud_User, on_delete=models.CASCADE, null=True)
	song = models.FileField(upload_to='songs')
	track_url = models.URLField()
	profile_url = models.URLField()
	follow_checkbox = models.BooleanField()
		
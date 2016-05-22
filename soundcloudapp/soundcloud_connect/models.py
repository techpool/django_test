from django.db import models

# Create your models here.
class Soundcloud_User(models.Model):
	"""Docstring for Soundcloud_User"""
	permanent_link = models.CharField(max_length=200, default='not-present')
	access_token = models.CharField(max_length=200)
	soundcloud_id = models.IntegerField(default=0, primary_key=True)
		
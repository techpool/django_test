from django.forms import ModelForm
from .models import Userdata
import soundcloud
from django import forms
from django.conf import settings

SOUNCLOUD_CLIENT_ID = settings.SOUNCLOUD_CLIENT_ID


class SongUploadForm(ModelForm):
	class Meta:
		model = Userdata
		fields = ['song', 'track_url', 'profile_url', 'follow_checkbox']

	# Checks whether the submitted URL is a valid Soundcloud URL or not
	def clean_track_url(self):

		# Creating the soundcloud client object
		client = soundcloud.Client(client_id=SOUNCLOUD_CLIENT_ID)
		
		# Fetching the cleaned data from the form
		data = self.cleaned_data['track_url']
		
		# Resolving the URL provided by the user
		try:
			client.get('/resolve', url=data)
		except Exception as e:

			# In case the URL provided does not gives a matching resource
			# Then raise a form validation error
			if e.response.status_code == 404:
				raise forms.ValidationError("Please provide a valid Track URL")
		return data

	# Checks whether the submitted URL is a valid Soundcloud URL or not
	def clean_profile_url(self):

		# Creating the soundcloud client object
		client = soundcloud.Client(client_id=SOUNCLOUD_CLIENT_ID)
		
		# Fetching the cleaned data from the form
		data = self.cleaned_data['profile_url']
		
		# Resolving the URL provided by the user
		try:
			client.get('/resolve', url=data)
		except Exception as e:
			# In case the URL provided does not gives a matching resource
			# Then raise a form validation error
			if e.response.status_code == 404:
				raise forms.ValidationError("Please provide a valid Profile URL")
		return data
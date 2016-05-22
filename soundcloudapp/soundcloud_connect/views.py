from django.shortcuts import render
from .models import Soundcloud_User
from django.http import HttpResponse, HttpResponseRedirect
import soundcloud

from django.conf import settings

SOUNCLOUD_CLIENT_ID = settings.SOUNCLOUD_CLIENT_ID
SOUNCLOUD_CLIENT_SECRET = settings.SOUNCLOUD_CLIENT_SECRET
SOUNCLOUD_REDIRECT_URI = settings.SOUNCLOUD_REDIRECT_URI

# The view to redirect the user to the app authentication page
def connect(request):

	# Creating the soundcloud client object
	client = soundcloud.Client(client_id=SOUNCLOUD_CLIENT_ID, 
							client_secret=SOUNCLOUD_CLIENT_SECRET,
							redirect_uri=SOUNCLOUD_REDIRECT_URI)

	# Redirecting the user to the authorized URL for authorizing the app
	return HttpResponseRedirect(client.authorize_url())


# The view to handle the callback url for after authentication
# by the user for the app

def callback(request):

	# Creating the soundcloud client object
	client = soundcloud.Client(client_id=SOUNCLOUD_CLIENT_ID, 
							client_secret=SOUNCLOUD_CLIENT_SECRET,
							redirect_uri=SOUNCLOUD_REDIRECT_URI)
	
	# Retrieving the authentication code from the query string
	code = request.GET['code']

	# Retrieving the access token after exchanging the authentication code
	access_token = client.exchange_token(code)

	# Recreating the client object with the retrieved access token
	client = soundcloud.Client(access_token=access_token.access_token)
	client_info = client.get('/me')

	# Constructing the model object
	user_object = Soundcloud_User(permanent_link=client_info.permalink,
								access_token=access_token.access_token,
								soundcloud_id=client_info.id)
	
	# Saving the model instance in the database
	user_object.save()

	# Storing the soundcloud id as a session variable
	request.session['soundcloud_id'] = client_info.id

	# Redirecting to the view for upload of filess
	return HttpResponseRedirect('/audioupload/upload/')
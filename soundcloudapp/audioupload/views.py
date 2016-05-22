from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from .form import SongUploadForm
from .models import Userdata
from soundcloud_connect.models import Soundcloud_User
import soundcloud
from django.core.exceptions import ObjectDoesNotExist
import requests
from wsgiref.util import FileWrapper
import os
from django.conf import settings


SOUNCLOUD_CLIENT_ID = settings.SOUNCLOUD_CLIENT_ID


# The view to handle both POST and GET request for the upload form
def upload(request):

	# Retrieving the Soundcloud ID from the session variable
	soundcloud_id = request.session['soundcloud_id']

	# Fetching the Soundcloud details of the user
	user_details = Soundcloud_User.objects.get(soundcloud_id=soundcloud_id)
	
	# Initializing a query variables
	query = None

	# Checking whether the user has already uploaded a form or not
	try:
		query = Userdata.objects.get(user=user_details)
	except ObjectDoesNotExist as e:
		# If it does not exist then very fine
		print('Object does not exist')

	# If the user has already submitted a form,
	# Then delete the already present record and save the
	# new one
	if query:

		# Remove the uploaded media (song) as well
		path_to_song = settings.MEDIA_ROOT + query.song.url
		os.remove(path_to_song)
		query.delete()

	# In case it is a form submission or POST request
	if request.method == 'POST':
		# create a form instance and populate it with data from the request:
		form = SongUploadForm(request.POST, request.FILES)
		# check whether it's valid:
		if form.is_valid():
			
			# Process the form data and add the user instance to the appropriate
			# field
			user_data = form.save(commit=False)
			user_data.user = user_details
			user_data.save()
			form.save_m2m()

			# After a valid form submission redirect it to the success URL
			return HttpResponseRedirect('success/')

	# if a GET (or any other method) we'll create a blank form
	else:
		form = SongUploadForm()

	# The form is being rendered in the form of paragraphs
	return render(request, 'audioupload/upload.html', {'form': form.as_p()})

# View to handle the successful submission of the form
def success(request):

	# Retrieving the Soundcloud ID from the session variable
	soundcloud_id = request.session['soundcloud_id']

	# Fetching the details of the soundcloud user
	user_details = Soundcloud_User.objects.get(soundcloud_id=soundcloud_id)
	
	# Fetching the user details with the same soundcloud user data
	user_data = Userdata.objects.get(user=user_details)

	# MAking the soundclooud client object
	client = soundcloud.Client(access_token=user_details.access_token,
							client_id=SOUNCLOUD_CLIENT_ID)
	access_token = user_details.access_token
	
	# get a tracks oembed data
	track_url = user_data.track_url

	# Profile URL submitted by the user
	profile_url = user_data.profile_url

	# Initialization of a few variables
	embed_info = None
	follow_user = None
	profile_id = None
	soundcloud_player = None


	try:
	    embed_info = client.get('/oembed', url=track_url)
	    soundcloud_player = embed_info.html
	except Exception as e:
		if e.response.status_code == 404:
			print('Invalid URL provided')
 
	return render(request, 'audioupload/success.html', {'audio_player': soundcloud_player})


# View that handles the download of the user uploaded file
def download_song(request):
	soundcloud_id = request.session['soundcloud_id']
	user_details = Soundcloud_User.objects.get(soundcloud_id=soundcloud_id)
	user_data = Userdata.objects.get(user=user_details)

	client = soundcloud.Client(access_token=user_details.access_token,
							client_id=SOUNCLOUD_CLIENT_ID)
	profile_url = user_data.profile_url
	profile_id = None
	isFollowing = False
	
	try:
		follow_user = client.get('/resolve', url=profile_url)
		profile_id = follow_user.id
	except Exception as e:
		if e.response.status_code == 404:
			print('Invalid URL provided')

	try:
		followers = client.get('/me/followings/')
		follower_obj = followers.collection

		for each_follower in follower_obj:
			if each_follower.id == profile_id:
				isFollowing = True

	except Exception as e:
	    print(e)

	if user_data.follow_checkbox:
		if isFollowing:
			path_to_song = settings.MEDIA_ROOT + user_data.song.url
			file = open(path_to_song, "rb")
			response = HttpResponse(FileWrapper(file), content_type='audio/mpeg')
			response['Content-Disposition'] = 'attachment; filename=song.mp3'
			file.close()

			return response
		else:
			return HttpResponse("You must follow the user to download your track")
	else:
		if isFollowing:
			return HttpResponse("You must unfollow the user to download your track")
		else:
			path_to_song = settings.MEDIA_ROOT + user_data.song.url
			file = open(path_to_song, "rb")
			response = HttpResponse(FileWrapper(file), content_type='audio/mpeg')
			response['Content-Disposition'] = 'attachment; filename=song.jpeg'
			file.close()

	
import json

from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse, Http404


def home(request):
	"""
	Render the home page.
	"""
	context = {
		'GOOGLE_MAPS_API_KEY': settings.GOOGLE_MAPS_API_KEY,
	}
	return render(request, 'burritoscore/home.html', context)


def get_score_by_location(request, location):
	"""
	Returns the burrito score for a given location.
	"""
	if request.is_ajax():
		# LA lat/long
		lat = '34.052234'
		lng = '-118.243685'

		score = {
			'location': location,
			'score': '42',
			'lat': lat,
			'lng': lng
		}

		return HttpResponse(json.dumps(score), content_type="application/json")

	raise Http404

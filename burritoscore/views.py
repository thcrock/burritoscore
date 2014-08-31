import json
from multiprocessing import Pool

from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse, Http404
from geopy.geocoders import GoogleV3
from burritoscore.scorers.binscorer import BinScorer
from burritoscore.scorers.data import BusinessData


def home(request):
	"""
	Render the home page.
	"""
	context = {
		'GOOGLE_MAPS_API_KEY': settings.GOOGLE_MAPS_API_KEY,
	}
	return render(request, 'burritoscore/home.html', context)


def geolocate_business(business):
	"""
	If the business doesn't have coordinates, let's get them
	from the address.
	"""
	location = ' '.join(business['location']['display_address'])

	geolocator = GoogleV3(api_key=settings.GOOGLE_MAPS_API_KEY)
	address, (latitude, longitude) = geolocator.geocode(location)
	return (latitude, longitude)


def get_score_by_location(request, location):
	"""
	Returns the burrito score for a given location.
	"""
	if request.is_ajax():
		scorer = BusinessData()
		score, radius, businesses = scorer.score(location)

		return HttpResponse(json.dumps({'score': score, 'radius': radius, 'businesses': businesses.values()}), content_type="application/json")

	raise Http404

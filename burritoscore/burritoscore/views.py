import json
from multiprocessing import Pool

from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse, Http404
from geopy.geocoders import GoogleV3
from burritoscore.scorers.binscorer import BinScorer


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


def format_business(business):
	# Backfill data if it's not there and we need it.
	if 'coordinate' not in business['location']:
		lat, lng = geolocate_business(business)
		business['location']['coordinate'] = {'latitude': lat, 'longitude': lng}

	return {
		'lat': business['location']['coordinate']['latitude'],
		'lon': business['location']['coordinate']['longitude'],
		'score': business['rating'],
		'name': business['name'],
	}

def get_score_by_location(request, location):
	"""
	Returns the burrito score for a given location.
	"""
	if request.is_ajax():
		scorer = BinScorer()
		score, businesses = scorer.score(location)

		pool = Pool()
		formatted_businesses = pool.map(format_business, businesses.values())

		return HttpResponse(json.dumps({'score': score, 'businesses': formatted_businesses}), content_type="application/json")

	raise Http404

import json

from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse, Http404
from burritoscore.scorers.binscorer import BinScorer


def home(request):
	"""
	Render the home page.
	"""
	context = {
		'GOOGLE_MAPS_API_KEY': settings.GOOGLE_MAPS_API_KEY,
	}
	return render(request, 'burritoscore/home.html', context)


def format_business(business):
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
		formatted_businesses = [format_business(business) for business in businesses.values() if 'coordinate' in business['location']]

		return HttpResponse(json.dumps({'score': score, 'businesses': formatted_businesses}), content_type="application/json")

	raise Http404

import json

from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse, Http404


def home(request):
	"""
	Render the home page.
	"""
	context = {
		'GOOGLE_MAPS_API_KEY': settings.GOOGLE_MAPS_API_KEY
	}
	return render(request, 'burritoscore/home.html', context)


def get_score(request):
	"""
	Returns the burrito score for a given location.
	"""
	if request.is_ajax():
		return HttpResponse(json.dumps({'score': '42'}), content_type="application/json")

	raise Http404

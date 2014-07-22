from multiprocessing import Pool

from django.conf import settings

from yelpapi import YelpAPI
from geopy.geocoders import GoogleV3
from geopy.distance import vincenty


class BusinessData(object):
	"""
	Uses the Yelp api and geocoding to get and
	format business data the way we want.
	"""
	yelp = YelpAPI(settings.CONSUMER_KEY, settings.CONSUMER_SECRET, settings.TOKEN, settings.TOKEN_SECRET)
	geolocator = GoogleV3(api_key=settings.GOOGLE_MAPS_API_KEY)

	def get_all_near(self, location, radius, term='burrito', category_filter='mexican'):
		"""
		Gets formatted businesses near the given location within the radius.
		"""
		# Geolocate the given location
		address, (latitude, longitude) = self.geolocator.geocode(location)

		# Search by lat/lng
		search_results = self.yelp.search_query(
			ll='%s,%s' % (latitude, longitude),
			term=term,
			category_filter=category_filter,
			radius_filter=radius,
		)

		businesses = search_results['businesses']
		businesses = self._format_data((latitude, longitude), businesses)

		return businesses

	def _format_data(self, location, businesses):
		"""
		Things we care about: name, location, distance, rating, review_count
		"""
		# Get all the missing data we need
		pool = Pool()
		geolocated_businesses = pool.map(geolocate_business, businesses)
		backfilled_businesses = self._backfill_distances(geolocated_businesses)

		# Only keep the stuff we care about
		formatted_businesses = {}
		for business in backfilled_businesses:
			formatted_businesses[business['id']] = {
				'name': business['name'],
				'address': ' '.join(business['location']['display_address']),
				'lat': business['location']['coordinate']['latitude'],
				'lon': business['location']['coordinate']['longitude'],
				'distance': business['distance'],
				'rating': business['rating'],
				'review_count': business['review_count'],
			}

		return formatted_businesses

	def _backfill_distances(location, businesses):
		for business in businesses:
			if 'distance' not in business:
				business['distance'] = vincenty(location, (latitude, longitude)).meters

		return businesses


def geolocate_business(business):
	"""
	Take Yelp businesses and backfill with geodata for those missing it.
	"""
	# backfill coordinate data if necessary
	if 'coordinate' not in business['location']:
		geolocator = GoogleV3(api_key=settings.GOOGLE_MAPS_API_KEY)
		business_address = ' '.join(business['location']['display_address'])
		address, (latitude, longitude) = geolocator.geocode(business_address)
		business['location']['coordinate'] = {'latitude': latitude, 'longitude': longitude}

	return business
	
from yelpapi import YelpAPI
from django.core.management.base import BaseCommand, NoArgsCommand
from django.conf import settings
from optparse import make_option

REVIEW_COUNT_MULTIPLIER_MIN = 0.25
REVIEW_COUNT_MULTIPLIER_MAX = 1.5

class Command(BaseCommand):
    help = 'Hi'
    option_list = BaseCommand.option_list + (
        make_option('--location', '-l', dest='location'),
    )

    def scoring_function(self, business, distance_multiplier):
        review_count_multiplier = float(business['review_count']) / 100.0
        if review_count_multiplier < REVIEW_COUNT_MULTIPLIER_MIN:
            review_count_multiplier = REVIEW_COUNT_MULTIPLIER_MIN
        elif review_count_multiplier > REVIEW_COUNT_MULTIPLIER_MAX:
            review_count_multiplier = REVIEW_COUNT_MULTIPLIER_MAX

        score = distance_multiplier * review_count_multiplier * business['rating']
        print "distance multiplier is", distance_multiplier, "review count multiplier is", review_count_multiplier, "rating is", business['rating'], "for", business['name'], "score =", score
        return score

    def do_radius(self, radius, search_location):
        yelp_api = YelpAPI(settings.CONSUMER_KEY, settings.CONSUMER_SECRET, settings.TOKEN, settings.TOKEN_SECRET)
        search_results = yelp_api.search_query(
            location=search_location,
            term='burrito',
            category_filter='mexican',
            radius_filter=radius,
        )

        businesses = {}
        for row in search_results['businesses']:
            businesses[row['id']] = {
                'rating': row['rating'],
                'name': row['name'],
                'review_count': row['review_count']
            }

        return businesses

    def handle(self, **options):
        location = options['location']
        ids = set()
        # search radius in meters
        searches = (
            (500, 2.0),
            (750, 1.5),
            (1000, 1.0),
        )
        score = 0.0
        for search_radius, distance_multiplier in searches:
            businesses = self.do_radius(search_radius, location)
            for business_id, business in businesses.iteritems():
                if business_id not in ids:
                    score += self.scoring_function(business, distance_multiplier)
                    ids.add(business_id)

        print score



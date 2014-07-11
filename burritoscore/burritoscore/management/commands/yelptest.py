from yelpapi import YelpAPI
from django.core.management.base import BaseCommand, NoArgsCommand
from django.conf import settings

class Command(NoArgsCommand):
    help = 'Hi'

    def handle(self, *args, **kwargs):
        yelp_api = YelpAPI(settings.CONSUMER_KEY, settings.CONSUMER_SECRET, settings.TOKEN, settings.TOKEN_SECRET)
        search_results = yelp_api.search_query(
            location='Chicago, IL'
        )
        print search_results

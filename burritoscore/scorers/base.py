from abc import ABCMeta, abstractmethod
from django.conf import settings
from yelpapi import YelpAPI

class Scorer(object):
    __metaclass__ = ABCMeta


    def __init__(self, *args, **kwargs):
        self.yelp = YelpAPI(settings.CONSUMER_KEY, settings.CONSUMER_SECRET, settings.TOKEN, settings.TOKEN_SECRET)

    @abstractmethod
    def score(self, location):
        pass

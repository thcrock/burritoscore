from .base import Scorer
import numpy
from collections import Counter

REVIEW_COUNT_MULTIPLIER_MIN = 0.75
REVIEW_COUNT_MULTIPLIER_MAX = 1.25

class BinScorer(Scorer):

    def score(self, location):
        ids = set()
        # search radius in meters
        searches = (
            (500, 2.0),
            (750, 1.5),
            (1000, 1.0),
        )
        scores = []
        boosts = []
        for search_radius, distance_multiplier in searches:
            businesses = self.do_radius(search_radius, location)
            for business_id, business in businesses.iteritems():
                if business_id not in ids:
                    scores.append(self.scoring_function(business, distance_multiplier))
                    ids.add(business_id)
                    if business['rating'] >= 4.5 and business['review_count'] > 10:
                        boosts.append(business)

        score_bins = numpy.array([0, 3, 6, 10, 15])
        arr = numpy.array(scores)
        score_distribution = numpy.digitize(arr, score_bins)
        counter = Counter(score_distribution.tolist())
        score = 0.0
        for s, c in counter.iteritems():
            mult = 5 if c > 5 else c
            score += s * float(mult)

        # bonus time
        #print "boost", boosts
        score += len(boosts) * 5

        return score

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
        search_results = self.yelp.search_query(
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

from django.core.management.base import BaseCommand, NoArgsCommand
from optparse import make_option
from burritoscore.scorers.binscorer import BinScorer


class Command(BaseCommand):
    help = 'Hi'
    option_list = BaseCommand.option_list + (
        make_option('--location', '-l', dest='location'),
    )


    def handle(self, **options):
        scorer = BinScorer()
        score, businesses = scorer.score(options['location'])
        print score




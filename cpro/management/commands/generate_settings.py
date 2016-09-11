import time
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from django.conf import settings as django_settings
from web.tools import totalDonators
from cpro import models

def generate_settings():

        print 'Get total donators'
        total_donators = totalDonators()

        print 'Get the latest news'
        try:
            current_events = models.Event.objects.get(end__lte=timezone.now())
            latest_news = [{
                'title': event.name,
                'image': event.image_url,
                'url': event.item_url,
            } for event in current_events]
        except:
            latest_news = []

        print 'Get the characters'
        all_idols = models.Idol.objects.all().order_by('name')
        favorite_characters = [(
            idol.pk,
            idol.name,
	    idol.image_url,
        ) for idol in all_idols]

        print 'Get max stats'
        stats = {
                'hp_max': None,
                'hp_awakened_max': None,
                'vocal_max': None,
                'vocal_awakened_max': None,
                'dance_max': None,
                'dance_awakened_max': None,
                'visual_max': None,
                'visual_awakened_max': None,
                'overall_max_': None,
                'overall_awakened_max_': None,
        }
        for stat in stats.keys():
            max_stats = models.Card.objects.all().extra(select={
                    'overall_max_': 'vocal_max + dance_max + visual_max',
                    'overall_awakened_max_': 'vocal_awakened_max + dance_awakened_max + visual_awakened_max',
            }).order_by('-' + stat)[0]
            stats[stat] = getattr(max_stats, stat)
        stats['overall_max'] = stats['overall_max_']
        del(stats['overall_max_'])
        stats['overall_awakened_max'] = stats['overall_awakened_max_']
        del(stats['overall_awakened_max_'])

        print 'Save generated settings'
        s = u'\
import datetime\n\
TOTAL_DONATORS = ' + unicode(total_donators) + u'\n\
LATEST_NEWS = ' + unicode(latest_news) + u'\n\
FAVORITE_CHARACTERS = ' + unicode(favorite_characters) + u'\n\
MAX_STATS = ' + unicode(stats) + u'\n\
GENERATED_DATE = datetime.datetime.fromtimestamp(' + unicode(time.time()) + u')\n\
'
        print s
        with open(django_settings.BASE_DIR + '/' + django_settings.SITE + '_project/generated_settings.py', 'w') as f:
            print >> f, s
        f.close()

class Command(BaseCommand):
    can_import_settings = True

    def handle(self, *args, **options):
        generate_settings()

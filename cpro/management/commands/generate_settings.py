import datetime
from collections import OrderedDict
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings as django_settings
from django.utils.translation import get_language
from django.db.models import Q
from magi import urls # needed to load static_url
from magi.utils import (
        getCurrentEvents,
        staticImageURL,
)
from magi.tools import (
    generateSettings,
    totalDonatorsThisMonth,
    getStaffConfigurations,
    latestDonationMonth,
    getCharactersBirthdays,
    getUsersBirthdaysToday,
)
from cpro import models

def generate_settings():
    old_lang = get_language()
    now = timezone.now()
    ten_days_ago = now - datetime.timedelta(days=10)

    print 'Get total donators'
    total_donators = totalDonatorsThisMonth() or '\'\''

    print 'Get latest donation month'
    donation_month = latestDonationMonth(failsafe=True)

    print 'Get staff configurations'
    staff_configurations, latest_news = getStaffConfigurations()

    print 'Get the latest news'

    # Events
    current_events = getCurrentEvents(
            models.Event.objects.all(),
            starts_within=5,
            ends_within=5,
            start_field_name='beginning',
            end_field_name='end',
    )
    latest_news = [{
            'title': event.name,
            'image': event.image_url,
            'url': event.item_url,
            'hide_title': True,
            'ajax': False,
    } for event in current_events]

    # Birthdays

    def get_name_image_url_from_character(character):
        try:
                card = models.Card.objects.filter(idol=character).exclude(
                        (Q(art__isnull=True) | Q(art=''))
                        & (Q(art_awakened__isnull=True) | Q(art_awakened='')),
                ).exclude(
                        art_on_homepage=False,
                        art_awakened_on_homepage=False,
                ).order_by('-i_rarity', '-release_date')[0]
        except IndexError:
                return None, None, None
        return character.first_name, card.art_awakened_url or card.art_url, character.item_url

    latest_news = getCharactersBirthdays(
        models.Idol.objects.all(),
        get_name_image_url_from_character,
        latest_news=latest_news,
    )

    # Users birthdays
    latest_news = getUsersBirthdaysToday(
        staticImageURL('happy_birthday.png'),
        latest_news=latest_news,
        max_usernames=4,
    )

    print 'Get the characters'
    all_idols = models.Idol.objects.all().order_by('name')
    favorite_characters = [(
            idol.pk,
            idol.name,
	        idol.image_url,
    ) for idol in all_idols]

    print 'Get the starters'
    all_starters = models.Card.objects.filter(pk__in=[100001, 200001, 300001]).order_by('pk')
    starters = OrderedDict([
        (card.pk, {
            'name': card.cached_idol.name,
            'icon': card.icon_url,
        }) for card in all_starters
    ])

    print 'Get homepage cards'
    cards = models.Card.objects.exclude(
            (Q(art__isnull=True) | Q(art=''))
            & (Q(art_awakened__isnull=True) | Q(art_awakened=''))
            & (Q(transparent__isnull=True) | Q(transparent='')),
    ).exclude(
            art_on_homepage=False,
            art_awakened_on_homepage=False,
    ).order_by('-release_date')[:10]
    homepage_arts = []
    position = { 'size': 'cover', 'x': 'center', 'y': 'center' }
    for c in cards:
        if c.art_on_homepage:
            if c.art:
                homepage_arts.append({
                    'url': c.art_url,
                    'hd_url': c.art_2x_url or c.art_original_url,
                    'about_url': c.item_url,
                })
            else:
                homepage_arts.append({
                    'url': staticImageURL('backgrounds/background0.png'),
                    'foreground_url': c.transparent_url,
                    'about_url': c.item_url,
                    'position': position,
                })
        if c.art_awakened_on_homepage:
            if c.art_awakened:
                homepage_arts.append({
                    'url': c.art_awakened_url,
                    'hd_url': c.art_awakened_2x_url or c.art_awakened_original_url,
                    'about_url': c.item_url,
                })
            else:
                homepage_arts.append({
                    'url': staticImageURL('backgrounds/background1.png'),
                    'foreground_url': c.transparent_awakened_url,
                    'about_url': c.item_url,
                    'position': position,
                })
    if not homepage_arts:
        homepage_arts = [{
                'url': '//i.cinderella.pro/u/c/art/200601SR-Layla.png',
                'hd_url': '//i.cinderella.pro/u/c/art/200601SR-Layla.png',
        }]


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

    generateSettings({
        'LATEST_NEWS': latest_news,
        'TOTAL_DONATORS': total_donators,
        'DONATION_MONTH': donation_month,
        'HOMEPAGE_ARTS': homepage_arts,
        'STAFF_CONFIGURATIONS': staff_configurations,
        'FAVORITE_CHARACTERS': favorite_characters,
            'STARTERS': starters,
        'MAX_STATS': stats,
    }, imports=[
        'from collections import OrderedDict',
    ])

class Command(BaseCommand):
    can_import_settings = True

    def handle(self, *args, **options):
        generate_settings()

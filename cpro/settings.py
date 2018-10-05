# -*- coding: utf-8 -*-
from collections import OrderedDict
from django.conf import settings as django_settings
from django.utils.translation import ugettext_lazy as _
from magi.default_settings import DEFAULT_ENABLED_COLLECTIONS, DEFAULT_ENABLED_PAGES, DEFAULT_JAVASCRIPT_TRANSLATED_TERMS, DEFAULT_PROFILE_EXTRA_TABS
from magi.utils import tourldash
from cpro import models, forms, filters, collections_settings, utils

SITE_NAME = u'Cinderella Producers'
SITE_URL = 'http://cinderella.pro/'
SITE_IMAGE = 'cpro.png'
EMAIL_IMAGE = 'cpro_banner.png'
SITE_STATIC_URL = '//localhost:{}/'.format(django_settings.DEBUG_PORT) if django_settings.DEBUG else '//i.cinderella.pro/'
#SITE_STATIC_URL = '//i.cinderella.pro/'
GAME_NAME = 'IDOLM@STER Cinderella Girls Starlight Stage'
GAME_URL = 'https://itunes.apple.com/jp/app/idolmaster-cinderella-girls/id1016318735?l=en&mt=8'
GAME_DESCRIPTION = 'THE iDOLM@STER Cinderella Girls: Starlight Stage is a spin-off free-to-play rhythm game released for mobile devices.'
DISQUS_SHORTNAME = 'cinderellapro'
ACCOUNT_MODEL = models.Account
COLOR = '#4a86e8'

GOOGLE_ANALYTICS = 'UA-59453399-3'

GITHUB_REPOSITORY = ('SchoolIdolTomodachi', 'CinderellaProducers')
TWITTER_HANDLE = 'cinderella__pro'

HASHTAGS = ['imas', 'deresute', u'デレステ']

USER_COLORS = models.TYPES

GET_GLOBAL_CONTEXT = utils.globalContext

STATIC_FILES_VERSION = '15'

TOTAL_DONATORS = getattr(django_settings, 'TOTAL_DONATORS', 2) + 2
FAVORITE_CHARACTERS = getattr(django_settings, 'FAVORITE_CHARACTERS', None)
FAVORITE_CHARACTER_TO_URL = lambda link: '/idol/{pk}/{name}/'.format(pk=link.raw_value, name=tourldash(link.value))
FAVORITE_CHARACTER_NAME = _(u'{nth} Favorite Idol')

LATEST_NEWS = getattr(django_settings, 'LATEST_NEWS', 2)

EMPTY_IMAGE = 'cinderella.png'

JAVASCRIPT_TRANSLATED_TERMS = DEFAULT_JAVASCRIPT_TRANSLATED_TERMS
JAVASCRIPT_TRANSLATED_TERMS += [
    'Permalink',
    'Deleted',
]

ON_USER_EDITED = utils.onUserEdited
ON_PREFERENCES_EDITED = utils.onPreferencesEdited

DONATORS_STATUS_CHOICES = models.DONATORS_STATUS_CHOICES

PROFILE_EXTRA_TABS = OrderedDict([
    ('badges', DEFAULT_PROFILE_EXTRA_TABS['badges']),
    ('favorites', {
        'icon': 'star',
        'name': _('Favorite Cards'),
        'callback': 'loadFavoriteCards',
    }),
])

ENABLED_COLLECTIONS = DEFAULT_ENABLED_COLLECTIONS

ENABLED_PAGES = DEFAULT_ENABLED_PAGES

ENABLED_PAGES['index']['custom'] = True

ENABLED_PAGES['cardstat'] = {
    'ajax': True,
    'navbar_link': False,
    'url_variables':  [
        ('card', '\d+'),
    ],
}

ENABLED_PAGES['cardcollection'] = {
    'ajax': True,
    'navbar_link': False,
    'url_variables':  [
        ('card', '\d+'),
    ],
}

ENABLED_PAGES['addcard'] = {
    'ajax': True,
    'navbar_link': False,
    'url_variables':  [
        ('card', '\d+'),
    ],
}

ENABLED_PAGES['favoritecard'] = {
    'ajax': True,
    'navbar_link': False,
    'url_variables':  [
        ('card', '\d+'),
    ],
}

ENABLED_PAGES['account_about'] = {
    'ajax': True,
    'navbar_link': False,
    'url_variables':  [
        ('account', '\d+'),
    ],
}

# -*- coding: utf-8 -*-
from collections import OrderedDict
from django.conf import settings as django_settings
from django.utils.translation import ugettext_lazy as _
from magi.default_settings import (
    DEFAULT_ENABLED_PAGES,
    DEFAULT_JAVASCRIPT_TRANSLATED_TERMS,
    DEFAULT_NAVBAR_ORDERING,
    DEFAULT_ENABLED_NAVBAR_LISTS,
)
from magi.utils import (
    tourldash,
    getTranslatedName,
)
from cpro.utils import (
    globalContext,
    onUserEdited,
    onPreferencesEdited,
)
from cpro.raw import LICENSES
from cpro import models #, forms, filters, collections_settings, utils

############################################################
# License, game and site settings

SITE_NAME = u'Cinderella Producers'
GAME_NAME = 'IDOLM@STER Cinderella Girls Starlight Stage'
GAME_URL = 'https://itunes.apple.com/jp/app/idolmaster-cinderella-girls/id1016318735?l=en&mt=8'
GAME_DESCRIPTION = 'THE iDOLM@STER Cinderella Girls: Starlight Stage is a spin-off free-to-play rhythm game released for mobile devices.'

COLOR = '#4a86e8'

############################################################
# Images

SITE_IMAGE = 'cpro.png'
EMAIL_IMAGE = 'cpro_banner.png'
EMPTY_IMAGE = 'cinderella.png'

############################################################
# Settings per languages


############################################################
# Contact & Social

GITHUB_REPOSITORY = ('SchoolIdolTomodachi', 'CinderellaProducers')
TWITTER_HANDLE = 'cinderella__pro'

############################################################
# Homepage

HOMEPAGE_BACKGROUND = 'backgrounds/bg_5931.png'
HOMEPAGE_ART_GRADIENT = True
HOMEPAGE_ART_SIDE = 'left'
HOMEPAGE_ART_POSITION = {
    'position': 'center right',
    'size': '150%',
    'y': '40%',
    'x': '100%',
}



############################################################
# First steps

############################################################
# Activities

HASHTAGS = ['imas', 'deresute', u'デレステ']

ACTIVITY_TAGS = [
    ('cards', _('New Cards')),
    ('event', _('Event')),
    ('live', _('Live')),
    ('comedy', _('Comedy')),
    ('room', _('Room Decoration')),
    ('introduction', _('Introduce yourself')),
    ('idols', _('Idols')),
    ('anime', _('Anime')),
    ('cosplay', _('Cosplay')),
    ('fanart', _('Fan made')),
    ('merch', _('Merchandise')),
    ('community', _('Community')),
    ('unrelated', _('Unrelated')),
    ('AR Idol Date', 'AR Idol Date'),
]

############################################################
# User preferences and profiles

USER_COLORS = [
    (_type_name, _type_details['translation'], _type_name, _type_details['color'])
    for _type_name, _type_details in models.TYPES.items()
]

FAVORITE_CHARACTERS = getattr(django_settings, 'FAVORITE_CHARACTERS', None)
FAVORITE_CHARACTER_TO_URL = lambda link: '/idol/{pk}/{name}/'.format(pk=link.raw_value, name=tourldash(link.value))
FAVORITE_CHARACTER_NAME = _(u'Idol')

DONATORS_STATUS_CHOICES = models.DONATORS_STATUS_CHOICES

# todo
# APROFILE_EXTRA_TABS = OrderedDict([
#     ('badges', DEFAULT_PROFILE_EXTRA_TABS['badges']),
#     ('favorites', {
#         'icon': 'star',
#         'name': _('Favorite Cards'),
#         'callback': 'loadFavoriteCards',
#     }),
# ])

############################################################
# Staff features

############################################################
# Technical settings

SITE_URL = 'http://cinderella.pro/'

SITE_STATIC_URL = '//localhost:{}/'.format(django_settings.DEBUG_PORT) if django_settings.DEBUG else '//i.cinderella.pro/'
#SITE_STATIC_URL = '//i.cinderella.pro/'

DISQUS_SHORTNAME = 'cinderellapro'
GOOGLE_ANALYTICS = 'UA-59453399-3'

GET_GLOBAL_CONTEXT = globalContext
ACCOUNT_MODEL = models.Account

JAVASCRIPT_TRANSLATED_TERMS = DEFAULT_JAVASCRIPT_TRANSLATED_TERMS
JAVASCRIPT_TRANSLATED_TERMS += [
    'Permalink',
    'Deleted',
]

ON_USER_EDITED = onUserEdited
ON_PREFERENCES_EDITED = onPreferencesEdited

############################################################
# From settings or generated_settings

STATIC_FILES_VERSION = getattr(django_settings, 'STATIC_FILES_VERSION', None)
TOTAL_DONATORS = getattr(django_settings, 'TOTAL_DONATORS', None)
LATEST_NEWS = getattr(django_settings, 'LATEST_NEWS', None)
STAFF_CONFIGURATIONS = getattr(django_settings, 'STAFF_CONFIGURATIONS', None)
HOMEPAGE_ARTS = getattr(django_settings, 'HOMEPAGE_ARTS', None)
BACKGROUNDS = getattr(django_settings, 'BACKGROUNDS', None)
FAVORITE_CHARACTERS = getattr(django_settings, 'FAVORITE_CHARACTERS', None)

############################################################
# Customize pages

ENABLED_PAGES = DEFAULT_ENABLED_PAGES

if django_settings.DEBUG:
    for _license, _details in LICENSES.items():
        if 'redirect' in _details:
            # todo: later, should make some own pages
            ENABLED_PAGES[u'about_{}'.format(_license)] = {
                'title': _('About {thing}').format(thing=getTranslatedName(_details)),
                'redirect': _details.get('redirect', None),
                'navbar_link_list': _license,
                'new_tab': True,
            }
        for _game, _game_details in _details.get('games', {}).items():
            if 'redirect' in _game_details:
                # todo: later, should make some own pages
                ENABLED_PAGES[u'about_{}'.format(_game)] = {
                    'title': _('About {thing}').format(thing=getTranslatedName(_game_details)),
                    'redirect': _game_details.get('redirect', None),
                    'navbar_link_list': _license,
                    'new_tab': True,
                }

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


############################################################
# Customize nav bar

ENABLED_NAVBAR_LISTS = DEFAULT_ENABLED_NAVBAR_LISTS

# ENABLED_NAVBAR_LISTS['idolmaster'] = {
#     'title': getTranslatedName(ABOUT),
#     'image': ABOUT['image'],
#     'headers': [
#         (_short_name, {
#             'image': _game.get('image', None),
#             'title': getTranslatedName(_game),
#             'small': False,
#         }) for _short_name, _game in models.GAMES.items()
#         if _short_name == 'deresute' # To do remove when more game support gets added
#     ],
#     'order': [
#         'deresute',
#         'idol_list',
#     ],
# }

for _license, _details in LICENSES.items():
    ENABLED_NAVBAR_LISTS[_license] = {
        'image': _details.get('image', None),
        'title': getTranslatedName(_details),
        'icon': 'idol', # todo
        'headers': [
            (_game, {
                'image': _game_details.get('image', None),
                'title': getTranslatedName(_game_details),
                'small': False,
            }) for _game, _game_details in _details.get('games', {}).items()
        ],
        'order': [
            u'about_{}'.format(_license),
            u'{}_idol_list'.format(_license),
        ] + [
            _template.format(game=_game)
            for _template in [
                    'about_{game}',
                    '{game}/card_list',
                    '{game}/event_list',
            ]
            for _game, _game_details in _details.get('games', {}).items()
        ],
    }

# ENABLED_NAVBAR_LISTS['games'] = {
#     'icon': 'hobbies',
#     'title': _('Games'),
#     'headers': [
#         (_short_name, {
#             'image': _game.get('image', None),
#             'title': getTranslatedName(_game),
#             'small': False,
#         }) for _short_name, _game in models.GAMES.items()
#         if _short_name == 'deresute' # To do remove when more game support gets added
#     ],
#     'order': [
#         'deresute',
#         'card_list',
#         'event_list',

#         'mirishita',
#         'about_mirishita',

#         'emusute',
#         'about_emusute',

#         'shanimasu',
#         'about_shanimasu',
#     ],
# }

NAVBAR_ORDERING = [
    'idolmaster',
    'games',
] + DEFAULT_NAVBAR_ORDERING
a = [
    'account_list',
    'card_list',
    'idol_list',
    'event_list',
] + DEFAULT_NAVBAR_ORDERING

############################################################
############################################################
############################################################
############################################################


ENABLED_COLLECTIONS = {}#DEFAULT_ENABLED_COLLECTIONS



# ENABLED_COLLECTIONS['activity']['add']['before_save'] = collections_settings.activitiesBeforeSave
# ENABLED_COLLECTIONS['activity']['edit']['before_save'] = collections_settings.activitiesBeforeSave

# def filterActivitiesList(queryset, parameters, request):
#     if request.user.is_superuser and 'force_old' in request.GET:
#         if 'owner_id' in request.GET:
#             return queryset.filter(owner_id=request.GET['owner_id'])
#         return queryset
#     return queryset.filter(id__gt=2600)

# def filterActivities(queryset, parameters, request):
#     if request.user.is_superuser:
#         return queryset
#     return filterActivitiesList(queryset, parameters, request)

# ENABLED_COLLECTIONS['activity']['edit']['filter_queryset'] = filterActivities
# ENABLED_COLLECTIONS['activity']['item']['filter_queryset'] = filterActivities
# ENABLED_COLLECTIONS['activity']['add']['filter_queryset'] = filterActivities
# ENABLED_COLLECTIONS['activity']['list']['filter_queryset'] = filterActivitiesList

# ENABLED_COLLECTIONS['badge']['add']['before_save'] = collections_settings.badgesBeforeSave
# ENABLED_COLLECTIONS['badge']['edit']['before_save'] = collections_settings.badgesBeforeSave

# ENABLED_COLLECTIONS['account']['list']['distinct'] = True

# ENABLED_COLLECTIONS['account']['add']['form_class'] = collections_settings.getAccountForm
# ENABLED_COLLECTIONS['account']['add']['back_to_list_button'] = False
# ENABLED_COLLECTIONS['account']['add']['after_save'] = collections_settings.addAccountAfterSave
# ENABLED_COLLECTIONS['account']['edit']['form_class'] = forms.AccountFormAdvanced

# ENABLED_COLLECTIONS['account']['add']['otherbuttons_template'] = 'include/advancedButton'
# ENABLED_COLLECTIONS['account']['add']['extra_context'] = collections_settings.modAccountExtraContext
# ENABLED_COLLECTIONS['account']['edit']['extra_context'] = collections_settings.modAccountExtraContext
# ENABLED_COLLECTIONS['account']['add']['after_template'] = 'include/accountJSstarter'
# ENABLED_COLLECTIONS['account']['edit']['after_template'] = 'include/accountJSstarter'
# ENABLED_COLLECTIONS['account']['add']['js_files'] = ENABLED_COLLECTIONS['account']['add'].get('js_files', []) + ['mod_account']
# ENABLED_COLLECTIONS['account']['edit']['js_files'] = ENABLED_COLLECTIONS['account']['edit'].get('js_files', []) + ['mod_account']

# ENABLED_COLLECTIONS['account']['add']['redirect_after_add'] = collections_settings.redirectAfterAddAccount

# ENABLED_COLLECTIONS['account']['list']['before_template'] = 'include/beforeLeaderboard'
# ENABLED_COLLECTIONS['account']['list']['default_ordering'] = '-level'
# ENABLED_COLLECTIONS['account']['list']['filter_form'] = forms.FilterAccounts
# ENABLED_COLLECTIONS['account']['list']['filter_queryset'] = filters.filterAccounts
# ENABLED_COLLECTIONS['account']['list']['js_files'] = ENABLED_COLLECTIONS['account']['list'].get('js_files', []) + ['leaderboard']
# ENABLED_COLLECTIONS['account']['list']['extra_context'] = collections_settings.leaderboardExtraContext
# ENABLED_COLLECTIONS['account']['list']['show_add_button'] = lambda request: not request.user.is_authenticated()

# ENABLED_COLLECTIONS['user']['item']['extra_context'] = collections_settings.profileGetAccountTabs
# ENABLED_COLLECTIONS['user']['item']['js_files'] = ENABLED_COLLECTIONS['user']['item'].get('js_files', []) + ['profile_account_tabs', 'cards']

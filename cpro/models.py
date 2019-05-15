# -*- coding: utf-8 -*-
from __future__ import division
import datetime, os
from collections import OrderedDict
from django.utils import timezone
from django.utils.formats import dateformat
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _, string_concat, get_language
from django.conf import settings as django_settings
from django.utils.deconstruct import deconstructible
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Q
from magi.models import User
from magi.abstract_models import (
    BaseAccount,
    AccountAsOwnerModel,
)
from magi.item_model import (
    MagiModel,
    get_image_url,
    get_http_image_url,
    i_choices,
    getInfoFromChoices,
)
from magi.utils import (
    staticImageURL,
    split_data,
    join_data,
    AttrDict,
    tourldash,
    randomString,
    uploadItem,
    upload2x,
)
from cpro.model_choices import *
from cpro.django_translated import t

############################################################
# Models utils and variables

# Types

DEFAULT_LIGHT_BACKGROUND = 'backgrounds/background6.png'
DEFAULT_BACKGROUND = 'backgrounds/background5.png'

DERESUTE_TYPES = OrderedDict([
    ('Cute', {
        'translation': _('Cute'),
        'japanese': u'キュート',
        'color': '#FF0173',
        'light_background': 'backgrounds/background8.png',
        'background': 'backgrounds/background9.png',
    }),
    ('Cool', {
        'translation': _('Cool'),
        'japanese': u'クール',
        'color': '#0E75FF',
        'light_background': 'backgrounds/background10.png',
        'background': 'backgrounds/background11.png',
    }),
    ('Passion', {
        'translation': _('Passion'),
        'japanese': u'パッション',
        'color': '#FFAA00',
        'light_background': 'backgrounds/background12.png',
        'background': 'backgrounds/background13.png',
    }),
])

OTHER_TYPES = OrderedDict([
    ('TestCute2', {
        'translation': _('Cute'),
        'japanese': u'キュート',
        'color': '#FF0173',
        'light_background': 'backgrounds/background8.png',
        'background': 'backgrounds/background9.png',
    }),
    ('TestCool', {
        'translation': _('Cool'),
        'japanese': u'クール',
        'color': '#0E75FF',
        'light_background': 'backgrounds/background10.png',
        'background': 'backgrounds/background11.png',
    }),
    ('TestPassion', {
        'translation': _('Passion'),
        'japanese': u'パッション',
        'color': '#FFAA00',
        'light_background': 'backgrounds/background12.png',
        'background': 'backgrounds/background13.png',
    }),
])

TYPES = OrderedDict()
TYPES.update(DERESUTE_TYPES)
TYPES.update(OTHER_TYPES)

TYPE_CHOICES = [(_name, _info['translation']) for _name, _info in TYPES.items()]

############################################################
############################################################
# MagiCircles' default collections
############################################################
############################################################

############################################################
# Account

class Account(BaseAccount):
    collection_name = 'account'

    PRODUCER_RANK_CHOICES = (
        'E', 'D', 'C', 'B', 'A', 'S', 'SS'
    )
    i_producer_rank = models.PositiveIntegerField(
        _('Producer rank'), choices=i_choices(PRODUCER_RANK_CHOICES), default=0)

    friend_id = models.PositiveIntegerField(_('Game ID'), null=True)
    accept_friend_requests = models.NullBooleanField(_('Accept friend requests'), null=True)

    OS_CHOICES = (
        'Android',
        'iOs',
    )
    i_os = models.PositiveIntegerField(_('Operating system'), choices=i_choices(OS_CHOICES), null=True)
    os_icon = property(lambda _a: _a.os.lower() if _a.os else None)

    device = models.CharField(
        _('Device'), max_length=150, null=True,
        help_text=_('The model of your device. Example: Nexus 5, iPhone 4, iPad 2, ...'),
    )

    PLAY_WITH = OrderedDict([
        ('Thumbs', {
            'translation': _('Thumbs'),
            'icon': 'thumbs'
        }),
        ('Fingers', {
            'translation': _('All fingers'),
            'icon': 'fingers'
        }),
        ('Index', {
            'translation': _('Index fingers'),
            'icon': 'index'
        }),
        ('Hand', {
             'translation': _('One hand'),
            'icon': 'fingers'
        }),
        ('Other', {
            'translation': _('Other'),
            'icon': 'sausage'
        }),
    ])
    PLAY_WITH_CHOICES = [(_name, _info['translation']) for _name, _info in PLAY_WITH.items()]
    i_play_with = models.PositiveIntegerField(_('Play with'), choices=i_choices(PLAY_WITH_CHOICES), null=True)
    play_with_icon = property(getInfoFromChoices('play_with', PLAY_WITH, 'icon'))

    center = models.ForeignKey('OwnedCard', verbose_name=_('Center'), null=True, on_delete=models.SET_NULL, related_name='centers')
    starter = models.ForeignKey('Card', verbose_name=_('Starter'), on_delete=models.SET_NULL, null=True, limit_choices_to={
        'id__in': django_settings.STARTERS.keys(),
    })

    ############################################################
    # Cache center

    _cache_j_center_card = models.TextField(null=True)
    _cached_center_card_collection_name = 'card'
    _cache_center_card_fk_class = classmethod(lambda _s: Card)
    _cache_center_card_images = ['icon', 'art', 'transparent']

    def to_cache_center_card(self):
        if not self.center_id:
            return {}
        return {
            'id': self.center.card_id,
            'center': {
                'id': self.center_id,
                'awakened': self.center.awakened,
            },
            'i_type': self.center.card.i_type,
            'icon': unicode(self.center.icon),
            'art': unicode(self.center.art),
            'transparent': unicode(self.center.transparent),
            'unicode': unicode(self.center.card),
        }

    ############################################################
    # Utils

    i_type = property(lambda _s: _s.cached_center_card.i_type)
    type = property(lambda _s: _s.cached_center_card.type)
    t_type = property(lambda _s: _s.cached_center_card.t_type)

    @property
    def background_url(self):
        return staticImageURL(TYPES[self.type]['background'] if self.center_id else DEFAULT_BACKGROUND)

    @property
    def light_background_url(self):
        return staticImageURL(TYPES[self.type]['light_background'] if self.center_id else DEFAULT_LIGHT_BACKGROUND)

############################################################
############################################################
# Abstract models
############################################################
############################################################

############################################################
# Idol

class BaseIdol(MagiModel):
    owner = models.ForeignKey(User, related_name='added_idols')
    name = models.CharField(string_concat(_('Name'), ' (', _('Romaji'), ')'), max_length=100, unique=True)
    japanese_name = models.CharField(string_concat(_('Name'), ' (', t['Japanese'], ')'), max_length=100, null=True)

    @property
    def first_name(self):
        return self.name.split(' ')[-1] if self.name is not None else None

    @property
    def last_name(self):
        return self.name.split(' ')[0] if self.name is not None else None

    @property
    def t_name(self):
        return self.japanese_name if get_language() == 'ja' else self.name

    TYPE_CHOICES = TYPE_CHOICES
    i_type = models.PositiveIntegerField(_('Type'), choices=i_choices(TYPE_CHOICES))
    japanese_type = property(getInfoFromChoices('type', TYPES, 'japanese'))
    type_color = property(getInfoFromChoices('type', TYPES, 'color'))
    type_image_url = property(lambda _s: staticImageURL(_s.i_type, folder='color', extension='png'))

    age = models.PositiveIntegerField(_('Age'), null=True)
    birthday = models.DateField(_('Birthday'), null=True, help_text='The year is not used, so write whatever')
    display_birthday = property(lambda _s: dateformat.format(_s.birthday, "F d"))

    height = models.PositiveIntegerField(_('Height'), null=True, help_text='in cm')
    display_height = property(lambda _s: u'{} cm'.format(_s.height))

    weight = models.PositiveIntegerField(_('Weight'), null=True, help_text='in kg')
    display_weight = property(lambda _s: u'{} kg'.format(_s.weight))

    BLOOD_TYPE_CHOICES = [ 'O', 'A', 'B', 'AB' ]
    i_blood_type = models.PositiveIntegerField(_('Blood Type'), choices=i_choices(BLOOD_TYPE_CHOICES), null=True)

    WRITING_HAND_CHOICES = [
        ('Right', _('Right')),
        ('Left', _('Left')),
        ('Both', _('Both')),
    ]
    i_writing_hand = models.PositiveIntegerField(
        _('Writing Hand'), choices=i_choices(WRITING_HAND_CHOICES), null=True)

    bust = models.PositiveIntegerField(_('Bust'), null=True, help_text='in cm')
    display_bust = property(lambda _s: u'{} cm'.format(_s.bust))
    waist = models.PositiveIntegerField(_('Waist'), null=True, help_text='in cm')
    display_waist = property(lambda _s: u'{} cm'.format(_s.waist))
    hips = models.PositiveIntegerField(_('Hips'), null=True, help_text='in cm')
    display_hips = property(lambda _s: u'{} cm'.format(_s.hips))

    ASTROLOGICAL_SIGN_CHOICES = (
        ('Leo', _('Leo')),
        ('Aries', _('Aries')),
        ('Libra', _('Libra')),
        ('Virgo', _('Virgo')),
        ('Scorpio', _('Scorpio')),
        ('Capricorn', _('Capricorn')),
        ('Pisces', _('Pisces')),
        ('Gemini', _('Gemini')),
        ('Cancer', _('Cancer')),
        ('Sagittarius', _('Sagittarius')),
        ('Aquarius', _('Aquarius')),
        ('Taurus', _('Taurus')),
    )
    i_astrological_sign = models.PositiveIntegerField(_('Astrological Sign'), choices=i_choices(ASTROLOGICAL_SIGN_CHOICES), null=True)
    astrological_sign_image_url = property(lambda _s: staticImageURL(
        _s.i_astrological_sign, folder='i_astrological_sign', extension='png'))

    hometown = models.CharField(string_concat(_('Hometown'), ' (', t['Japanese'], ')'), max_length=100, null=True)
    romaji_hometown = models.CharField(
        string_concat(_('Hometown'), ' (', _('Romaji'), ')'), max_length=100, null=True)

    cv = models.CharField(string_concat(_('CV'), ' (', t['Japanese'], ')'), max_length=100, null=True)
    romaji_cv = models.CharField(string_concat(_('CV'), ' (', _('Romaji'), ')'), max_length=100, null=True)

    hobbies = models.CharField(_('Hobbies'), max_length=100, null=True)
    description = models.TextField(_('Description'), null=True)

    ############################################################
    # Images

    image = models.ImageField(_('Image'), upload_to=uploadItem('i'))
    signature = models.ImageField(_('Signature'), upload_to=uploadItem('i/sign'), null=True)

    ############################################################
    # Utils

    @property
    def display_name_in_list(self):
        return mark_safe(u'{img}<span style="color: {color};">{name}</span>'.format(
            img=u'<img src="{img_url}" alt="{type}">&nbsp;'.format(
                img_url=self.type_image_url,
                type=self.t_type,
            ),
            color=self.type_color,
            name=self.t_name,
        ))

    def __unicode__(self):
        return self.t_name

    class Meta(MagiModel.Meta):
        abstract = True


############################################################
############################################################
# Cinderella Girls collections
############################################################
############################################################

############################################################
# Idol

class Idol(BaseIdol):
    collection_name = 'cinderellagirls/idol'

    TYPES = DERESUTE_TYPES
    TYPE_CHOICES = [(_name, _info['translation']) for _name, _info in TYPES.items()]

    ############################################################
    # Reverse relations with totals

    reverse_related = (
        ('cards', 'cards', _('Cards')),
	('fans', 'users', _('Fans'), 'favorite_character'),
        ('events', 'events', _('Events')),
    )

    ############################################################
    # Cache totals

    _cache_total_fans_days = 2
    _cache_total_fans_last_update = models.DateTimeField(null=True)
    _cache_total_fans = models.PositiveIntegerField(null=True)
    to_cache_total_fans = lambda(_s): User.objects.filter(
        Q(preferences__favorite_character1=_s.id)
        | Q(preferences__favorite_character2=_s.id)
        | Q(preferences__favorite_character3=_s.id)
    ).count()

    _cache_total_cards_days = 2
    _cache_total_cards_last_update = models.DateTimeField(null=True)
    _cache_total_cards = models.PositiveIntegerField(null=True)
    to_cache_total_cards = lambda(_s): Card.objects.filter(idol=_s).count()

    _cache_total_events_days = 2
    _cache_total_events_last_update = models.DateTimeField(null=True)
    _cache_total_events = models.PositiveIntegerField(null=True)
    to_cache_total_events = lambda(_s): Event.objects.filter(cards__idol=_s).count()

############################################################
# Event

class Event(MagiModel):
    collection_name = 'deresute/event'

    owner = models.ForeignKey(User, related_name='added_events')
    name = models.CharField(string_concat(_('Name'), ' (', t['Japanese'], ')'), max_length=100)
    translated_name = models.CharField(
        string_concat(_('Name'), ' (translated in English)'), max_length=100, null=True)
    image = models.ImageField(_('Image'), upload_to=uploadItem('e'))
    beginning = models.DateTimeField(_('Beginning'), null=True)
    end = models.DateTimeField(_('End'), null=True)

    EVENT_KIND_CHOICES = [
        ('Token', _('Token')),
        ('Medley', _('Medley')),
        ('Coop', _('Coop')),
        ('Caravan', _('Caravan')),
        ('LIVEParade', _('LIVE Parade')),
    ]
    i_kind = models.PositiveIntegerField(_('Kind'), default=0, choices=i_choices(EVENT_KIND_CHOICES))

    t1_points = models.PositiveIntegerField(_('T{} points').format(1), null=True)
    t1_rank = models.PositiveIntegerField(_('T{} rank').format(1), null=True)
    t2_points = models.PositiveIntegerField(_('T{} points').format(2), null=True)
    t2_rank = models.PositiveIntegerField(_('T{} rank').format(2), null=True)
    t3_points = models.PositiveIntegerField(_('T{} points').format(3), null=True)
    t3_rank = models.PositiveIntegerField(_('T{} rank').format(3), null=True)
    t4_points = models.PositiveIntegerField(_('T{} points').format(4), null=True)
    t4_rank = models.PositiveIntegerField(_('T{} rank').format(4), null=True)
    t5_points = models.PositiveIntegerField(_('T{} points').format(5), null=True)
    t5_rank = models.PositiveIntegerField(_('T{} rank').format(5), null=True)

    status = property(lambda _s: getEventStatus(_s.start_date, _s.end_date, starts_within=6, ends_within=6))

    # todo
    # @property
    # def is_current(self):
    #     return (self.beginning is not None
    #             and self.end is not None
    #             and timezone.now() > self.beginning
    #             and timezone.now() < self.end)


    ############################################################
    # Cache totals

    _cache_total_cards_days = 2
    _cache_total_cards_last_update = models.DateTimeField(null=True)
    _cache_total_cards = models.PositiveIntegerField(null=True)
    to_cache_total_cards = lambda(_s): Card.objects.filter(event=_s).count()

    def __unicode__(self):
        return self.translated_name or self.name

############################################################
# Card

class Card(MagiModel):
    collection_name = 'deresute/card'
    owner = models.ForeignKey(User, related_name='added_cards')

    ############################################################
    # Main fields: idol, id, rarity, ...

    id = models.PositiveIntegerField(_('ID'), unique=True, primary_key=True, db_index=True)
    id_awakened = models.PositiveIntegerField(
        string_concat(_('ID'), ' (', _('Awakened'), ')'), unique=True, null=True)
    idol = models.ForeignKey(
        Idol, verbose_name=_('Idol'), related_name='cards', null=True, on_delete=models.SET_NULL)
    event = models.ForeignKey(Event, verbose_name=_('Event'), related_name='cards', null=True, on_delete=models.SET_NULL, blank=True)

    RARITIES = OrderedDict([
        ('N', {
            'translation': _('Normal'),
            'max_levels': (20, 30),
        }),
        ('R', {
            'translation': _('Rare'),
            'max_levels': (40, 50),
        }),
        ('SR', {
            'translation': _('Super Rare'),
            'max_levels': (60, 70),
        }),
        ('SSR', {
            'translation': _('Super Super Rare'),
            'max_levels': (80, 90),
        }),
    ])
    RARITY_CHOICES = [(_name, _info['translation']) for _name, _info in RARITIES.items()]
    i_rarity = models.PositiveIntegerField(_('Rarity'), choices=i_choices(RARITY_CHOICES))

    release_date = models.DateField(_('Release date'), default=datetime.date(2015, 9, 3), null=True)
    is_limited = models.BooleanField(_('Limited'), default=False)

    title = models.CharField(string_concat(_('Title'), ' (', t['Japanese'], ')'), max_length=100, null=True)
    translated_title = models.CharField(string_concat(_('Title'), ' (translated in English)'), max_length=100, null=True, blank=True)

    @property
    def t_title(self):
        return self.title if get_language() == 'ja' or not self.translated_title else self.translated_title

    ############################################################
    # Main fields utils

    max_levels = property(getInfoFromChoices('rarity', RARITIES, 'max_levels'))
    max_level = property(lambda _s: _s.max_levels[0])
    max_level_awakened = property(lambda _s: _s.max_levels[1])

    TYPE_CHOICES = Idol.TYPE_CHOICES
    i_type = property(lambda _s: _s.cached_idol.i_type)
    type = property(lambda _s: _s.cached_idol.type)
    t_type = property(lambda _s: _s.cached_idol.t_type)
    japanese_type = property(lambda _s: Idol.TYPES[_s.cached_idol.type]['japanese'])

    ############################################################
    # Images

    image = models.ImageField(_('Image'), upload_to=uploadItem('c'))
    image_awakened = models.ImageField(string_concat(_('Image'), ' (', _('Awakened'), ')'), upload_to=uploadItem('c/a'))

    _2x_art = models.ImageField(string_concat(_('Art'), ' (HD)'), upload_to=upload2x('c/art'), null=True)
    art = models.ImageField(_('Art'), upload_to=uploadItem('c/art'))
    art_on_homepage = models.BooleanField('Show the art on the homepage of the site?', default=True, help_text='Uncheck this if the art looks weird because the idol is not in the center')

    _2x_art_awakened = models.ImageField(string_concat(_('Art'), ' (HD ', _('Awakened'), ')'), upload_to=upload2x('c/art/a'), null=True)
    art_awakened = models.ImageField(string_concat(_('Art'), ' (', _('Awakened'), ')'), upload_to=uploadItem('c/art/a'))
    art_awakened_on_homepage = models.BooleanField('Show the awakened art on the homepage of the site?', default=True, help_text='Uncheck this if the awakened art looks weird because the idol is not in the center')

    transparent = models.ImageField(_('Transparent'), upload_to=uploadItem('c/transparent'))
    transparent_awakened = models.ImageField(string_concat(_('Transparent'), ' (', _('Awakened'), ')'), upload_to=uploadItem('c/transparent/a'))

    icon = models.ImageField(_('Icon'), upload_to=uploadItem('c/icon'))
    icon_awakened = models.ImageField(string_concat(_('Icon'), ' (', _('Awakened'), ')'), upload_to=uploadItem('c/icon/a'))

    puchi = models.ImageField(_('Puchi'), upload_to=uploadItem('c/puchi'))
    puchi_awakened = models.ImageField(string_concat(_('Puchi'), ' (', _('Awakened'), ')'), upload_to=uploadItem('c/puchi/a'))

    IMAGES = ['image', 'art', 'transparent', 'icon', 'puchi']

    ############################################################
    # Statistics fields

    hp_min = models.PositiveIntegerField(string_concat(_('Life'), ' (', _('Minimum'), ')'), default=0)
    hp_max = models.PositiveIntegerField(string_concat(_('Life'), ' (', _('Maximum'), ')'), default=0)
    hp_awakened_min = models.PositiveIntegerField(string_concat(_('Life'), ' (', _('Awakened'), ', ', _('Minimum'), ')'), default=0)
    hp_awakened_max = models.PositiveIntegerField(string_concat(_('Life'), ' (', _('Awakened'), ', ', _('Maximum'), ')'), default=0)
    vocal_min = models.PositiveIntegerField(string_concat(_('Vocal'), ' (', _('Minimum'), ')'), default=0)
    vocal_max = models.PositiveIntegerField(string_concat(_('Vocal'), ' (', _('Maximum'), ')'), default=0)
    vocal_awakened_min = models.PositiveIntegerField(string_concat(_('Vocal'), ' (', _('Awakened'), ', ', _('Minimum'), ')'), default=0)
    vocal_awakened_max = models.PositiveIntegerField(string_concat(_('Vocal'), ' (', _('Awakened'), ', ', _('Maximum'), ')'), default=0)
    dance_min = models.PositiveIntegerField(string_concat(_('Dance'), ' (', _('Minimum'), ')'), default=0)
    dance_max = models.PositiveIntegerField(string_concat(_('Dance'), ' (', _('Maximum'), ')'), default=0)
    dance_awakened_min = models.PositiveIntegerField(string_concat(_('Dance'), ' (', _('Awakened'), ', ', _('Minimum'), ')'), default=0)
    dance_awakened_max = models.PositiveIntegerField(string_concat(_('Dance'), ' (', _('Awakened'), ', ', _('Maximum'), ')'), default=0)
    visual_min = models.PositiveIntegerField(string_concat(_('Visual'), ' (', _('Minimum'), ')'), default=0)
    visual_max = models.PositiveIntegerField(string_concat(_('Visual'), ' (', _('Maximum'), ')'), default=0)
    visual_awakened_min = models.PositiveIntegerField(string_concat(_('Visual'), ' (', _('Awakened'), ', ', _('Minimum'), ')'), default=0)
    visual_awakened_max = models.PositiveIntegerField(string_concat(_('Visual'), ' (', _('Awakened'), ', ', _('Maximum'), ')'), default=0)

    ############################################################
    # Statistics utils

    @property
    def overall_min(self):
        return self.vocal_min + self.dance_min + self.visual_min
    @property
    def overall_max(self):
        return self.vocal_max + self.dance_max + self.visual_max
    @property
    def overall_awakened_min(self):
        return self.vocal_awakened_min + self.dance_awakened_min + self.visual_awakened_min
    @property
    def overall_awakened_max(self):
        return self.vocal_awakened_max + self.dance_awakened_max + self.visual_awakened_max

    def _value_for_level(self, fieldname, level=1, max_level=None, to_string=True, round_integer=True):
        if not max_level:
            max_level = self.max_level
        min = getattr(self, fieldname + '_min')
        if not min:
            min = 0
        max = getattr(self, fieldname + '_max')
        if not max:
            max = 0
        value = min + ((level - 1) / (max_level - 1)) * (max - min)
        if to_string:
            return '{0:g}'.format(int(value) if round_integer else round(value, 2))
        return value

    _local_stats = None

    @property
    def stats_percent(self):
        if not self._local_stats:
            self._local_stats = [(awakened, [{
                'stat': field,
                'name': name,
                'max': django_settings.MAX_STATS.get(field + '_max', 100),
                'value_max_level': self._value_for_level(field, level=self.max_level if not awakened else self.max_level_awakened, max_level=self.max_level if not awakened else self.max_level_awakened),
                'percent_max_level': (self._value_for_level(field, level=self.max_level if not awakened else self.max_level_awakened, max_level=self.max_level if not awakened else self.max_level_awakened, to_string=False) / django_settings.MAX_STATS.get(field + '_max', 100)) * 100,
                'javascript_levels': str({ str(level): {
                    'value': self._value_for_level(field, level=level, max_level=self.max_level if not awakened else self.max_level_awakened),
                    'percent': (self._value_for_level(field, level=level, max_level=self.max_level if not awakened else self.max_level_awakened, to_string=False) / django_settings.MAX_STATS.get(
                        field + '_max', 100)) * 100,
                } for level in range(1, (self.max_level if not awakened else self.max_level_awakened) + 1) }).replace('\'', '"'),
            } for (field, name) in [
                ('hp' + ('_awakened' if awakened else ''), _('Life')),
                ('vocal' + ('_awakened' if awakened else ''), _('Vocal')),
                ('visual' + ('_awakened' if awakened else ''), _('Visual')),
                ('dance' + ('_awakened' if awakened else ''), _('Dance')),
                ('overall' + ('_awakened' if awakened else ''), _('Overall')),
            ]
        ]) for awakened in (False, True)]
        return self._local_stats

    ############################################################
    # Skill fields

    skill_name = models.CharField('Skill name', max_length=100, null=True)
    translated_skill_name = models.CharField('Translated skill name', max_length=100, null=True, blank=True)

    SKILLS = OrderedDict([
        ('Lesser Perfect Lock', {
            'translation': _('Lesser Perfect Lock'),
            'template': u'For every {trigger_value} seconds, there is a {trigger_chance}% chance of turning all Great notes into Perfect notes in the next {skill_duration} seconds.',
            'japanese_template': u'⎾{trigger_chance}%の確率 - {skill_duration}秒⏌ {trigger_value}秒毎、GREATをPERFECTにする',
        }),
        ('Greater Perfect Lock', {
            'translation': _('Greater Perfect Lock'),
            'template': u'For every {trigger_value} seconds, there is a {trigger_chance}% chance of turning all Nice and Great notes into Perfect notes in the next {skill_duration} seconds.',
            'japanese_template': u'⎾{trigger_chance}%の確率 - {skill_duration}秒⏌ {trigger_value}秒毎、GREAT/NICEをPERFECTにする',
        }),
        ('Extreme Perfect Lock', {
            'translation': _('Extreme Perfect Lock'),
            'template': u'For every {trigger_value} seconds, there is a {trigger_chance}% chance of turning all Bad, Nice and Great notes into Perfect notes in the next {skill_duration} seconds.',
            'japanese_template': u'⎾{trigger_chance}%の確率 - {skill_duration}秒⏌ {trigger_value}秒毎、GREAT/NICE/BADをPERFECTにする',
        }),
        ('Combo Guard', {
            'translation': _('Combo Guard'),
            'template': u'For every {trigger_value} seconds, there is a {trigger_chance}% chance that Nice notes will not break the combo in the next {skill_duration} seconds.',
            'japanese_template': u'⎾{trigger_chance}%の確率 - {skill_duration}秒⏌ {trigger_value}秒毎、NICEでもCOMBOが継続する',
        }),
        ('Healer', {
            'translation': _('Healer'),
            'template': u'For every {trigger_value} seconds, there is a {trigger_chance}% chance that Perfect notes will restore {skill_value} life in the next {skill_duration} seconds.',
            'japanese_template': u'⎾{trigger_chance}%の確率 - {skill_duration}秒⏌ {trigger_value}秒毎、PERFECTでライフ{skill_value}回復',
        }),
        ('Life Guard', {
            'translation': _('Life Guard'),
            'template': u'For every {trigger_value} seconds, there is a {trigger_chance}% chance that you will not lose health in the next {skill_duration} seconds.',
            'japanese_template': u'⎾{trigger_chance}%の確率 - {skill_duration}秒⏌ {trigger_value}秒毎、ライフが減少しなくなる',
        }),
        ('Combo Bonus', {
            'translation': _('Combo Bonus'),
            'template': u'For every {trigger_value} seconds, there is a {trigger_chance}% chance that you will gain an extra {skill_value}% combo bonus in the next {skill_duration} seconds.',
            'japanese_template': u'⎾{trigger_chance}%の確率 - {skill_duration}秒⏌ {trigger_value}秒毎、COMBOボーナス{skill_value}%アップ',
        }),
        ('Perfect Score Bonus', {
            'translation': _('Perfect Score Bonus'),
            'template': u'For every {trigger_value} seconds, there is a {trigger_chance}% chance that Perfect notes will receive a {skill_value}% score bonus in the next {skill_duration} seconds.',
            'japanese_template': u'⎾{trigger_chance}%の確率 - {skill_duration}秒⏌ {trigger_value}秒毎、PERFECTのスコア{skill_value}%アップ',
        }),
        ('Overload', {
            'translation': _('Overload'),
            'template': u'For every {trigger_value} seconds, there is a {trigger_chance}% chance that Perfect notes will receive a {skill_value}% bonus and Nice and Bad notes will not break your combo in the next {skill_duration} seconds, at the cost of {skill_value2} life.',
            'japanese_template': u'⎾{trigger_chance}%の確率 - {skill_duration}秒⏌ {trigger_value}秒毎、中確率でライフを{skill_value2}消費し、間PERFECTのスコア{skill_value}%アップ、NICE/BADでもCOMBO継続',
        }),
        ('Score Bonus', {
            'translation': _('Score Bonus'),
            'template': u'For every {trigger_value} seconds, there is a {trigger_chance}% chance that Great and Perfect notes will receive a {skill_value}% score bonus in the next {skill_duration} seconds.',
            'japanese_template': u'⎾{trigger_chance}%の確率 - {skill_duration}秒⏌ {trigger_value}秒毎、PERFECT/GREATのスコア{skill_value}%アップ',
        }),
        ('All Round', {
            'translation': _('All Round'),
            'template': u'For every {trigger_value} seconds, there is a {trigger_chance}% chance that you will gain an extra {skill_value}% combo bonus and Perfect notes will restore {skill_value2} life in the next {skill_duration} seconds.',
            'japanese_template': u'⎾{trigger_chance}%の確率 - {skill_duration}秒⏌ {trigger_value}秒毎、COMBOボーナス{skill_value}%アップ、PERFECTでライフ{skill_value2}回復',
        }),
        ('Concentration', {
            'translation': _('Concentration'),
            'template': u'For every {trigger_value} seconds, there is a {trigger_chance}% chance that Perfect notes will receive a {skill_value}% score bonus but the timing window for Perfect notes is reduced in the next {skill_duration} seconds.',
            'japanese_template': u'⎾{trigger_chance}%の確率 - {skill_duration}秒⏌ {trigger_value}秒毎、高確率でわずかな間、PERFECTのスコア{skill_value}%アップ、PERFECT判定される時間が短くなる',
        }),
        ('Skill Boost', {
            'translation': _('Skill Boost'),
            'template': u'For every {trigger_value} seconds, there is a {trigger_chance}% change that currently active skills will be boosted for {skill_duration} seconds',
            'japanese_template': u'⎾{trigger_chance}%の確率 - {skill_duration}秒⏌{trigger_value}秒毎、高確率でしばらくの間、他アイドルの特技効果を大アップ',
        }),
        ('Cute/Cool/Passion Focus', {
            'translation': _('Cute/Cool/Passion Focus'),
            'template': u'For every {trigger_value} seconds, there is a {trigger_chance}% chance that Perfect notes will receive a {skill_value}% score bonus, and you will gain an extra {skill_value2}% combo bonus, but only if you have only {type} idols in your team for {skill_duration} seconds',
            'japanese_template': u'⎾{trigger_chance}%の確率 - {skill_duration}秒⏌{type}アイドルのみ編成時、{trigger_value}秒毎、高確率でしばらくの間、PERFECTのスコア{skill_value}%アップ、COMBOボーナス{skill_value2}%アップ',
        }),
        ('Encore', {
            'translation': _('Encore'),
            'template': u'For every {trigger_value} seconds, there is a {trigger_chance}% chance to activate the previous skill again for {skill_duration} seconds.',
            'japanese_template': u'⎾{trigger_chance}%の確率 - {skill_duration}秒⏌{trigger_value}秒毎、直前に発動した他アイドルの特技効果を繰り返す',
        }),
        ('Life Sparkle', {
            'translation': _('Life Sparkle'),
            'template': u'For every {trigger_value} seconds, there is a {trigger_chance}% chance that you will gain an extra combo bonus based on your current health for {skill_duration} seconds.',
            'japanese_template': u'⎾{trigger_chance}%の確率 - {skill_duration}秒⏌{trigger_value}秒毎、ライフ値が多いほどCOMBOボーナスアップ',
        }),
        ('Tricolor Synergy', {
            'translation': _('Tricolor Synergy'),
            'template': u'For every {trigger_value} seconds, there is a {trigger_chance}% chance that with all three types of idols on the team, you will gain an extra {skill_value2}% combo bonus, and Perfect notes will receive a {skill_value}% score bonus plus restore {skill_value3} life, for {skill_duration} seconds.',
            'japanese_template': u'⎾{trigger_chance}%の確率 - {skill_duration}秒⏌3タイプ全てのアイドル編成時、{trigger_value}秒毎、PERFECTのスコア{skill_value2}%アップ/ライフ{skill_value3}回復、COMBOボーナス{skill_value}%アップ',
        }),
        ('Focus', {
            'translation': _('Focus'),
            'template': u'For every {trigger_value} seconds, there is a {trigger_chance}% chance that Perfect notes will receive a {skill_value}% score bonus, and you will gain an extra {skill_value2}% combo bonus for {skill_duration} seconds',
            'japanese_template': u'⎾{trigger_chance}%の確率 - {skill_duration}秒⏌{trigger_value}秒毎、高確率でしばらくの間、PERFECTのスコア{skill_value}%アップ、COMBOボーナス{skill_value2}%アップ',
        }),
    ])
    SKILL_CHOICES = [(_name, _info['translation']) for _name, _info in SKILLS.items()]
    i_skill = models.PositiveIntegerField(_('Skill'), choices=i_choices(SKILL_CHOICES), null=True)

    # Skill variables

    trigger_value = models.FloatField('Trigger Value', null=True)
    trigger_chance_min = models.FloatField('Trigger Chance (Minimum)', null=True)
    trigger_chance_max = models.FloatField('Trigger Chance (Maximum)', null=True)
    skill_duration_min = models.FloatField('Skill Duration (Minimum)', null=True)
    skill_duration_max = models.FloatField('Skill Duration (Minimum)', null=True)
    skill_value = models.FloatField('Skill Value', null=True)
    skill_value2 = models.FloatField('Other Skill Value', null=True)
    skill_value3 = models.FloatField('Other Skill Value', null=True)

    ############################################################
    # Skill utils

    MAX_SKILL_LEVEL = 10

    skill_template = property(getInfoFromChoices('skill', SKILLS, 'template'))
    skill_japanese_template = property(getInfoFromChoices('skill', SKILLS, 'japanese_template'))

    def get_skill_details(self, level=1, japanese=False):
        if not self.has_skill:
            return None
        return (self.skill_japanese_template if japanese else self.skill_template).format(
            trigger_value='{0:g}'.format(self.trigger_value if self.trigger_value else 0),
            trigger_chance=self._value_for_level(
                'trigger_chance', level, max_level=self.MAX_SKILL_LEVEL, round_integer=False),
            skill_duration=self._value_for_level(
                'skill_duration', level, max_level=self.MAX_SKILL_LEVEL, round_integer=False),
            skill_value='{0:g}'.format(self.skill_value if self.skill_value else 0),
            skill_value2='{0:g}'.format(self.skill_value2 if self.skill_value2 else 0),
            skill_value3='{0:g}'.format(self.skill_value3 if self.skill_value3 else 0),
            type=self.japanese_type if japanese else self.t_type,
        )

    @property
    def skill_details(self):
        return self.get_skill_details()

    @property
    def japanese_skill_details(self):
        return self.get_skill_details(japanese=True)

    @property
    def javascript_all_skill_levels_details(self):
        all_levels = {
            language: {
                unicode(level): self.get_skill_details(level=level, japanese=language == 'japanese')
                for level in range(1, self.max_skill_level + 1)
            } for language in ['english', 'japanese']
        }
        return unicode(all_levels).replace('u\'', '\'').replace('\'', '"')

    ############################################################
    # Leader skill fields

    _DEFAULT_LEADER_SKILL_TEMPLATE = _('Raises {leader_skill_type} of all {idol_type} idols by {leader_skill_percent}%.')
    _DEFAULT_JAPANESE_LEADER_SKILL_TEMPLATE = u'{idol_type}の{leader_skill_type}{leader_skill_percent}％アップ'

    _LEADER_SKILL_ONLY_TYPE_TEMPLATE = _('Raises {leader_skill_type} of all {idol_type} idols by {leader_skill_percent}% when there are only {idol_type} idols on the team.')
    _JAPANESE_LEADER_SKILL_ONLY_TYPE_TEMPLATE = u'{idol_type}アイドルのみ編成時、{idol_type}の{leader_skill_type}{leader_skill_percent}％アップ'

    _ALL_APPEALS = lambda: _('{type} appeal').format(type=u'/'.join([
        unicode(t[1]) for t in STAT_CHOICES
    ]))

    LEADER_SKILLS = OrderedDict([
        (0, {
            'verbose': 'Vocal appeal [Voice]',
            'raised_statistic': lambda: _('{type} appeal').format(type=unicode(_('Vocal'))),
            'japanese_raised_statistic': 'ボーカルアピール値',
            'suffix': _('Voice'),
            'japanese_suffix': u'ボイス',
        }),
        (2, {
            'verbose': 'Visual appeal [Make-up]',
            'raised_statistic': lambda: _('{type} appeal').format(type=unicode(_('Visual'))),
            'japanese_raised_statistic': 'ビジュアルアピール値',
            'suffix': _('Make-Up'),
            'japanese_suffix': u'メイク',
        }),
        (1, {
            'verbose': 'Dance appeal [Step]',
            'raised_statistic': lambda: _('{type} appeal').format(type=unicode(_('Dance'))),
            'japanese_raised_statistic': 'ダンスアピール値',
            'suffix': _('Step'),
            'japanese_suffix': u'ステップ',
        }),
        (101, {
            'verbose': 'Vocal/Visual/Dance appeals [Brilliance]',
            'raised_statistic': _ALL_APPEALS,
            'japanese_raised_statistic': '全アピール値',
            'suffix': _('Brilliance'),
            'japanese_suffix': u'ブリリアンス',
        }),
        (105, {
            'verbose': 'Vocal/Visual/Dance appeals, when only same type in the team [Princess]',
            'template': _LEADER_SKILL_ONLY_TYPE_TEMPLATE,
            'japanese_template': _JAPANESE_LEADER_SKILL_ONLY_TYPE_TEMPLATE,
            'raised_statistic': _ALL_APPEALS,
            'japanese_raised_statistic': '全アピール値',
            'suffix': _('Princess'),
            'japanese_suffix': u'プリンセス',
        }),
        (103, {
            'verbose': 'Skill probability [Ability]',
            'raised_statistic': lambda: _('Skill probability'),
            'japanese_raised_statistic': '特技発動確率',
            'suffix': _('Ability'),
            'japanese_suffix': u'アビリティ',
        }),
        (102, {
            'verbose': 'Life [Energy]',
            'raised_statistic': lambda: _('Life'),
            'japanese_raised_statistic': 'ライフ',
            'suffix': _('Energy'),
            'japanese_suffix': u'エナジー',
        }),
        (104, {
            'verbose': 'Life, when only same type in the team [Cheer]',
            'template': _LEADER_SKILL_ONLY_TYPE_TEMPLATE,
            'japanese_template': _JAPANESE_LEADER_SKILL_ONLY_TYPE_TEMPLATE,
            'raised_statistic': lambda: _('Life'),
            'japanese_raised_statistic': 'ライフ',
            'suffix': _('Cheer'),
            'japanese_suffix': u'チアー',
        }),
        (106, {
            'verbose': 'Fan gain, end of live [Cinderella Charm]',
            'template': _('Increases fan gain by {leader_skill_percent}% when you finish a live.'),
            'japanese_template': u'LIVEクリア時、獲得ファン数が{leader_skill_percent}アップ',
            'suffix': _('Cinderella Charm'),
            'japanese_suffix': u'シンデレラチャーム',
        }),
        (107, {
            'verbose': 'Rewards, end of live [Fortune Present]',
            'template': _('Gives extra rewards when you finish a live.'),
            'japanese_template': u'LIVEクリア時、特別報酬を追加で獲得',
            'suffix': _('Fortune Present'),
            'japanese_suffix': u'フォーチュンプレゼント',
        }),
    ])
    LEADER_SKILL_CHOICES = [(_name, _info['verbose']) for _name, _info in LEADER_SKILLS.items()]
    LEADER_SKILL_WITHOUT_I_CHOICES = True
    i_leader_skill = models.PositiveIntegerField(
        'Leader Skill: What kind of stat gets raised?', null=True, choices=LEADER_SKILL_CHOICES)

    LEADER_SKILL_APPLIES = OrderedDict([
        ('Idols of the same type [Cute/Cool/Passion]', {
        }),
        ('Idols of all 3 types, when all types are in the team [Tricolor]', {
            'prefix': _('Tricolor'),
            'japanese_prefix': 'トリコロール・',
            'template': _('Raises {leader_skill_type} of all idols by {leader_skill_percent}% when there are {all_types} idols on the team.'),
            'japanese_template': '3タイプ全てのアイドル編成時、全員の{leader_skill_type}{leader_skill_percent}％アップ',
        }),
        ('Idols of all 3 types [Shiny]', {
            'prefix': _('Shiny'),
            'japanese_prefix': 'シャイニー',
            'template': _DEFAULT_LEADER_SKILL_TEMPLATE,
            'japanese_template': _DEFAULT_JAPANESE_LEADER_SKILL_TEMPLATE,
        }),
    ])
    LEADER_SKILL_APPLY_CHOICES = LEADER_SKILL_APPLIES.keys()
    i_leader_skill_apply = models.PositiveIntegerField(
        'Leader Skill: Which idols does it apply to?', choices=LEADER_SKILL_APPLIES_CHOICES)

    leader_skill_percent = models.FloatField('Leader Skill: Percentage', null=True)

    ############################################################
    # Leader skill utils

    LEADER_SKILLS_WITHOUT_PREFIX = [106, 107]

    verbose_leader_skill =  property(getInfoFromChoices('leader_skill', LEADER_SKILLS, 'verbose'))
    leader_skill_formatted_percent = property(lambda _s: '{0:g}'.format(self.leader_skill_percent or 0))

    leader_skill_suffix = property(getInfoFromChoices('leader_skill', LEADER_SKILLS, 'suffix'))
    leader_skill_japanese_suffix = property(getInfoFromChoices('leader_skill', LEADER_SKILLS, 'japanese_suffix'))

    leader_skill_prefix = property(getInfoFromChoices(
        'leader_skill_apply', LEADER_SKILL_APPLIES, 'prefix',
        default=lambda _s: None if _s.leader_skill in LEADER_SKILLS_WITHOUT_PREFIX else _s.t_type,
    ))
    leader_skill_japanese_prefix = property(getInfoFromChoices(
        'leader_skill_apply', LEADER_SKILL_APPLIES, 'japanese_prefix',
        default=lambda _s: None if _s.leader_skill in LEADER_SKILLS_WITHOUT_PREFIX else _s.japanese_type,
    ))

    leader_skill_raised_statistic = property(getInfoFromChoices('leader_skill', LEADER_SKILLS, 'raised_statistic'))
    leader_skill_japanese_raised_statistic = property(getInfoFromChoices(
        'leader_skill', LEADER_SKILLS, 'japanese_raised_statistic'))

    _leader_skill_type_template = property(getInfoFromChoices(
        'leader_skill', LEADER_SKILLS, 'template', default=_DEFAULT_LEADER_SKILL_TEMPLATE))
    _leader_skill_type_japanese_template = property(getInfoFromChoices(
        'leader_skill', LEADER_SKILLS, 'japanese_template', default=_DEFAULT_JAPANESE_LEADER_SKILL_TEMPLATE))

    leader_skill_template = property(getInfoFromChoices(
        'leader_skill_apply', LEADER_SKILL_APPLIES, 'template',
        default=lambda _s: _s.leader_skill_type_template,
    ))
    leader_skill_japanese_template = property(getInfoFromChoices(
        'leader_skill_apply', LEADER_SKILL_APPLIES, 'japanese_template',
        default=lambda _s: _s.leader_skill_type_japanese_template,
    ))

    @property
    def leader_skill(self):
        if not self.has_leader_skill:
            return None
        return u' '.join([
            part for part in [
                self.leader_skill_prefix,
                self.leader_skill_suffix,
            ] if part
        ])

    @property
    def japanese_leader_skill(self):
        if not self.has_leader_skill:
            return None
        return u' '.join([
            part for part in [
                self.leader_skill_japanese_prefix,
                self.leader_skill_japanese_suffix,
            ] if part
        ])

    @property
    def leader_skill_details(self):
        return self.leader_skill_template.format(
            leader_skill_type=self.leader_skill_raised_statistic,
            idol_type=self.t_type.lower(),
            all_types=u'/'.join([t['translation'] for t in TYPES.values()]),
            leader_skill_percent=self.leader_skill_formatted_percent,
        ) if self.has_leader_skill else None

    @property
    def japanese_leader_skill_details(self):
        return self.leader_skill_japanese_template.format(
            leader_skill_type=self.leader_skill_japanese_raised_statistic,
            idol_type=self.japanese_type,
            all_types=u'/'.join([t['japanese'] for t in TYPES.values()]),
            leader_skill_percent=self.leader_skill_formatted_percent,
        ) if self.has_leader_skill else None

    @property
    def awakened_or_not(self):
        return (False, True)

    ############################################################
    # Cache event

    _cache_j_event = models.TextField(null=True)

    def to_cache_event(self):
        if not self.event_id:
            return None
        return {
            'id': self.event_id,
            'name': self.event.name,
            'translated_name': self.event.translated_name,
            'image': self.event.image,
        }

    ############################################################
    # Cache idol

    _cache_j_idol = models.TextField(null=True)

    def to_cache_idol(self):
        return {
            'id': self.idol_id,
            'name': self.idol.name,
            'japanese_name': self.idol.japanese_name,
            'i_type': self.idol.i_type,
            'image': unicode(self.idol.image),
        }

    @classmethod
    def cached_idol_pre(self, d):
        d['t_name'] = (
            d['japanese_name']
            if get_language() == 'ja'
            else d['name']
        )
        d['unicode'] = d['t_name']

    ############################################################
    # Cache totals

    _cache_total_owners_days = 2
    _cache_total_owners_last_update = models.DateTimeField(null=True)
    _cache_total_owners = models.PositiveIntegerField(null=True)
    to_cache_total_owners = lambda(_s): User.objects.filter(accounts__ownedcards__card=_s).distinct().count()

    _cache_total_favorites_days = 2
    _cache_total_favorites_last_update = models.DateTimeField(null=True)
    _cache_total_favorites = models.PositiveIntegerField(null=True)
    to_cache_total_favorites = lambda (_s): User.objects.filter(favoritecards__card=_s).distinct().count()


    ############################################################
    # Views

    @property
    def top_html(self):
        if (hasattr(self, 'request') and self.request
            and self.request.GET.get('view', None) == 'icons'):
            view = 'icon'
        else:
            view = 'image'
        return u''.join([
            u'<img src="{}" alt="{}" class="card-image {}">'.format(
                image,
                unicode(self),
                css_classes,
            ) for (image, css_classes) in [
                (getattr(self, '{}_url'.format(view)), 'normal'),
                (getattr(self, '{}_awakened_url'.format(view)), 'awakened'),
            ] if image
        ])

    @property
    def html_attributes_in_list(self):
        return {
            'data-type': self.type,
        }

    ############################################################
    # Unicode

    def __unicode__(self):
        if self.id:
            return u'{rarity} {idol_name} {title}'.format(
                rarity=self.rarity,
                idol_name=self.cached_idol.t_name,
                title=self.t_title or '',
            )
        return u''

############################################################
# Owned Card

def _ownedcard_image_property(field, prefix='', suffix=''):
    return lambda s: (
        getattr(s.card, u'{}{}_awakened{}'.format(prefix, field, suffix))
        if s.awakened
        else getattr(s.card, u'{}{}{}'.format(prefix, field, suffix))
    )

class OwnedCard(AccountAsOwnerModel):
    collection_name = 'ownedcard'

    account = models.ForeignKey(Account, related_name='ownedcards', on_delete=models.CASCADE)
    card = models.ForeignKey(Card, related_name='owned', on_delete=models.CASCADE)

    awakened = models.BooleanField(_('Awakened'), default=False)
    max_bonded = models.BooleanField(_('Max Bonded'), default=False)
    max_leveled = models.BooleanField(_('Max Leveled'), default=False)
    star_rank = models.PositiveIntegerField(_('Star Rank'), default=1, validators=[
        MinValueValidator(1),
        MaxValueValidator(20),
    ])
    skill_level = models.PositiveIntegerField(_('Skill Level'), default=1, validators=[
        MinValueValidator(1),
        MaxValueValidator(Card.MAX_SKILL_LEVEL),
    ])
    obtained_date = models.DateField(_('Obtained Date'), null=True)

    ############################################################
    # Image utils

    icon = property(_ownedcard_image_property('icon'))
    icon_url = property(_ownedcard_image_property('icon', suffix='_url'))
    http_icon_url = property(_ownedcard_image_property('icon', prefix='http_', suffix='_url'))

    art = property(_ownedcard_image_property('art'))
    art_url = property(_ownedcard_image_property('art', suffix='_url'))
    http_art_url = property(_ownedcard_image_property('art', prefix='http_', suffix='_url'))

    transparent = property(_ownedcard_image_property('transparent'))
    transparent_url = property(_ownedcard_image_property('transparent', suffix='_url'))
    http_transparent_url = property(_ownedcard_image_property('transparent', prefix='http_', suffix='_url'))

    ############################################################
    # Unicode

    def __unicode__(self):
        if self.id and self.card_id:
            return u'{rarity} {idol_name} {title} {awakened}'.format(
                rarity=self.card.rarity,
                idol_name=self.card.cached_idol.t_name,
                title=self.card.t_title or '',
                awakened=u'({})'.format(_('Awakened')) if self.awakened else '',
            ).strip()
        return u'#{} {}'.format(self.card_id, u'({})'.format(_('Awakened')) if self.awakened else '')

############################################################
# Favorite Card

class FavoriteCard(MagiModel):
    collection_name = 'favoritecard'

    owner = models.ForeignKey(User, related_name='favoritecards')
    card = models.ForeignKey(Card, related_name='fans', on_delete=models.CASCADE)

    def __unicode__(self):
        return u'#{}'.format(self.card_id)

    class Meta:
        unique_together = (('owner', 'card'),)

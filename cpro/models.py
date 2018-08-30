# -*- coding: utf-8 -*-
from __future__ import division
import datetime, os
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _, string_concat
from django.conf import settings as django_settings
from django.utils.deconstruct import deconstructible
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Q
from web.item_model import ItemModel, get_image_url, get_http_image_url
from web.utils import split_data, join_data, AttrDict, tourldash, randomString
from web.models import User
from cpro.model_choices import *
from cpro.django_translated import t

############################################################
# Utils

@deconstructible
class uploadItem(object):
    def __init__(self, prefix, length=30):
        self.prefix = prefix
        self.length = length

    def __call__(self, instance, filename):
        _, extension = os.path.splitext(filename)
        if not extension:
            extension = '.png'
        return u'{static_uploaded_files_prefix}{prefix}/{id}{string}{extension}'.format(
            static_uploaded_files_prefix=django_settings.STATIC_UPLOADED_FILES_PREFIX,
            prefix=self.prefix,
            id=instance.id if instance.id else randomString(6),
            string=tourldash(unicode(instance)),
            extension=extension,
        )

def getAccountLeaderboard(account):
    if not account.level:
        return None
    return Account.objects.filter(level__gt=account.level).values('level').distinct().count() + 1

############################################################
# Idol

class Idol(ItemModel):
    collection_name = 'idol'

    owner = models.ForeignKey(User, related_name='added_idols')
    name = models.CharField(string_concat(_('Name'), ' (romaji)'), max_length=100, unique=True)
    japanese_name = models.CharField(string_concat(_('Name'), ' (', t['Japanese'], ')'), max_length=100, null=True)
    i_type = models.PositiveIntegerField(_('Type'), choices=TYPE_CHOICES, null=True)
    @property
    def type(self): return TYPE_DICT[self.i_type]
    @property
    def english_type(self): return ENGLISH_TYPE_DICT[self.i_type]
    age = models.PositiveIntegerField(_('Age'), null=True)
    birthday = models.DateField(_('Birthday'), null=True, help_text='The year is not used, so write whatever')
    height = models.PositiveIntegerField(_('Height'), null=True, help_text='in cm')
    weight = models.PositiveIntegerField(_('Weight'), null=True, help_text='in kg')
    i_blood_type = models.PositiveIntegerField(_('Blood Type'), choices=BLOOD_TYPE_CHOICES, null=True)
    @property
    def blood_type(self): return BLOOD_TYPE_DICT[self.i_blood_type] if self.i_blood_type else None
    i_writing_hand = models.PositiveIntegerField(_('Writing Hand'), choices=WRITING_HAND_CHOICES, null=True)
    @property
    def writing_hand(self): return WRITING_HANDS_DICT[self.i_writing_hand] if self.i_writing_hand else None
    bust = models.PositiveIntegerField(_('Bust'), null=True, help_text='in cm')
    waist = models.PositiveIntegerField(_('Waist'), null=True, help_text='in cm')
    hips = models.PositiveIntegerField(_('Hips'), null=True, help_text='in cm')
    i_astrological_sign = models.PositiveIntegerField(_('Astrological Sign'), choices=ASTROLOGICAL_SIGN_CHOICES, null=True)
    @property
    def astrological_sign(self): return ASTROLOGICAL_SIGN_DICT[self.i_astrological_sign] if self.i_astrological_sign else None
    @property
    def english_astrological_sign(self): return UNTRANSLATED_ASTROLOGICAL_SIGN_DICT[self.i_astrological_sign] if self.i_astrological_sign else None
    hometown = models.CharField(_('Hometown'), help_text='In Japanese characters.', max_length=100, null=True)
    romaji_hometown = models.CharField(_('Hometown'), help_text='In romaji.', max_length=100, null=True)
    hobbies = models.CharField(_('Hobbies'), max_length=100, null=True)
    description = models.TextField(_('Description'), null=True)
    CV = models.CharField(_('CV'), help_text='In Japanese characters.', max_length=100, null=True)
    romaji_CV = models.CharField(_('CV'), help_text='In romaji.', max_length=100, null=True)

    # Images
    image = models.ImageField(_('Image'), upload_to=uploadItem('i'))
    signature = models.ImageField(_('Signature'), upload_to=uploadItem('i/sign'), null=True)
    @property
    def signature_url(self): return get_image_url(self.signature)

    # Cache totals
    _cache_totals_days = 2
    _cache_totals_last_update = models.DateTimeField(null=True)
    _cache_total_fans = models.PositiveIntegerField(null=True)
    _cache_total_cards = models.PositiveIntegerField(null=True)
    _cache_total_events = models.PositiveIntegerField(null=True)

    def update_cache_totals(self):
        self._cache_totals_last_update = timezone.now()
        self._cache_total_fans = User.objects.filter(
            Q(preferences__favorite_character1=self.id)
            | Q(preferences__favorite_character2=self.id)
            | Q(preferences__favorite_character3=self.id)
        ).count()
        self._cache_total_cards = Card.objects.filter(idol=self).count()
        self._cache_total_events = Event.objects.filter(cards__idol=self).count()

    def force_cache_totals(self):
        self.update_cache_totals()
        self.save()

    @property
    def cached_total_fans(self):
        if not self._cache_totals_last_update or self._cache_totals_last_update < timezone.now() - datetime.timedelta(hours=self._cache_totals_days):
            self.force_cache_totals()
        return self._cache_total_fans

    @property
    def cached_total_cards(self):
        if not self._cache_totals_last_update or self._cache_totals_last_update < timezone.now() - datetime.timedelta(hours=self._cache_totals_days):
            self.force_cache_totals()
        return self._cache_total_cards

    @property
    def cached_total_events(self):
        if not self._cache_totals_last_update or self._cache_totals_last_update < timezone.now() - datetime.timedelta(hours=self._cache_totals_days):
            self.force_cache_totals()
        return self._cache_total_events

    def __unicode__(self):
        return self.name

############################################################
# Event

class Event(ItemModel):
    collection_name = 'event'

    owner = models.ForeignKey(User, related_name='added_events')
    name = models.CharField(string_concat(_('Name'), ' (', t['Japanese'], ')'), max_length=100)
    translated_name = models.CharField(string_concat(_('Name'), ' (translated in English)'), max_length=100, null=True)
    image = models.ImageField(_('Image'), upload_to=uploadItem('e'))
    beginning = models.DateTimeField(_('Beginning'), null=True)
    end = models.DateTimeField(_('End'), null=True)
    i_kind = models.PositiveIntegerField(_('Kind'), default=0, choices=EVENT_KIND_CHOICES)
    @property
    def kind(self): return EVENT_KIND_DICT[self.i_kind]
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

    @property
    def is_current(self):
        return (self.beginning is not None
                and self.end is not None
                and timezone.now() > self.beginning
                and timezone.now() < self.end)

    # Cache totals
    _cache_totals_days = 2
    _cache_totals_last_update = models.DateTimeField(null=True)
    _cache_total_cards = models.PositiveIntegerField(null=True)

    def update_cache_totals(self, pluscards=0):
        self._cache_totals_last_update = timezone.now()
        self._cache_total_cards = Card.objects.filter(event=self).count() + pluscards

    def force_cache_totals(self, pluscards=0):
        self.update_cache_totals(pluscards=pluscards)
        self.save()

    @property
    def cached_total_cards(self):
        if not self._cache_totals_last_update or self._cache_totals_last_update < timezone.now() - datetime.timedelta(hours=self._cache_totals_days):
            self.force_cache_totals()
        return self._cache_total_cards

    def __unicode__(self):
        if self.translated_name:
            return self.translated_name
        return self.name

############################################################
# Account

class Account(ItemModel):
    collection_name = 'account'

    owner = models.ForeignKey(User, related_name='accounts')
    creation = models.DateTimeField(_('Join Date'), auto_now_add=True)
    level = models.PositiveIntegerField(_('Producer Level'), null=True, validators=[
        MaxValueValidator(300),
    ])
    nickname = models.CharField(_('Nickname'), max_length=100, null=True)
    game_id = models.PositiveIntegerField(_('Game ID'), null=True)
    accept_friend_requests = models.NullBooleanField('', null=True, help_text=_('Accept friend requests'))
    device = models.CharField(_('Device'), max_length=150, null=True)
    i_play_with = models.PositiveIntegerField(_('Play with'), null=True, choices=PLAY_WITH_CHOICES)
    @property
    def play_with(self): return PLAY_WITH_DICT[self.i_play_with] if self.i_play_with is not None else None
    @property
    def has_play_with(self): return self.i_play_with is not None
    @property
    def play_with_icon(self): return PLAY_WITH_ICONS[self.i_play_with] if self.i_play_with is not None else None
    i_os = models.PositiveIntegerField(_('Operating System'), choices=OS_CHOICES, default=0)
    @property
    def has_os(self): return self.i_os is not None
    @property
    def os(self): return OS_DICT[self.i_os] if self.i_os is not None else None
    center = models.ForeignKey('OwnedCard', verbose_name=_('Center'), null=True, on_delete=models.SET_NULL, related_name='centers')
    starter = models.ForeignKey('Card', verbose_name=_('Starter'), on_delete=models.SET_NULL, null=True)
    start_date = models.DateField(_('Start Date'), null=True)
    i_producer_rank = models.PositiveIntegerField(_('Producer Rank'), choices=PRODUCER_RANK_CHOICES, default=0)
    @property
    def producer_rank(self): return PRODUCER_RANK_DICT[self.i_producer_rank]

    # Cache owner
    _cache_owner_days = 20
    _cache_owner_last_update = models.DateTimeField(null=True)
    _cache_owner_username = models.CharField(max_length=32, null=True)
    _cache_owner_email = models.EmailField(null=True)
    _cache_owner_preferences_status = models.CharField(choices=DONATORS_STATUS_CHOICES, max_length=12, null=True)
    _cache_owner_preferences_twitter = models.CharField(max_length=32, null=True)

    def force_cache_owner(self):
        """
        Recommended to use select_related('owner', 'owner__preferences') when calling this method
        """
        self._cache_owner_last_update = timezone.now()
        self._cache_owner_username = self.owner.username
        self._cache_owner_email = self.owner.email
        self._cache_owner_preferences_status = self.owner.preferences.status
        self._cache_owner_preferences_twitter = self.owner.preferences.twitter
        self.save()

    @property
    def cached_owner(self):
        if not self._cache_owner_last_update or self._cache_owner_last_update < timezone.now() - datetime.timedelta(days=self._cache_owner_days):
            self.force_cache_owner()
        return AttrDict({
            'pk': self.owner_id,
            'id': self.owner_id,
            'username': self._cache_owner_username,
            'email': self._cache_owner_email,
            'item_url': u'/user/{}/{}/'.format(self.owner_id, self._cache_owner_username),
            'preferences': AttrDict({
                'status': self._cache_owner_preferences_status,
                'twitter': self._cache_owner_preferences_twitter,
            }),
        })

    # Cache leaderboard
    _cache_leaderboard_hours = 12
    _cache_leaderboard_last_update = models.DateTimeField(null=True)
    _cache_leaderboard = models.PositiveIntegerField(null=True)

    def update_cache_leaderboard(self):
        self._cache_leaderboard_last_update = timezone.now()
        self._cache_leaderboard = getAccountLeaderboard(self)

    def force_cache_leaderboard(self):
        self.update_cache_leaderboard()
        self.save()

    @property
    def cached_leaderboard(self):
        if not self._cache_leaderboard_last_update or self._cache_leaderboard_last_update < timezone.now() - datetime.timedelta(hours=self._cache_leaderboard_hours):
            self.force_cache_leaderboard()
        return self._cache_leaderboard

    # Cache center
    _cache_center_days = 20
    _cache_center_last_update = models.DateTimeField(null=True)
    _cache_center_awakened = models.NullBooleanField(default=None)
    _cache_center_card_id = models.PositiveIntegerField(null=True)
    _cache_center_card_i_type = models.PositiveIntegerField(choices=TYPE_CHOICES, null=True)
    _cache_center_card_icon = models.ImageField(upload_to=uploadItem('c/icon'), null=True)
    _cache_center_card_art = models.ImageField(upload_to=uploadItem('c/art'), null=True)
    _cache_center_card_transparent = models.ImageField(upload_to=uploadItem('c/transparent'), null=True)
    _cache_center_card_string = models.CharField(max_length=100, null=True)

    def update_cache_center(self):
        if self.center_id:
            self._cache_center_last_update = timezone.now()
            self._cache_center_awakened = self.center.awakened
            self._cache_center_card_id = self.center.card.id
            self._cache_center_card_i_type = self.center.card.i_type
            self._cache_center_card_icon = self.center.card.icon if not self.center.awakened else self.center.card.icon_awakened
            self._cache_center_card_art = self.center.card.art if not self.center.awakened else self.center.card.art_awakened
            self._cache_center_card_transparent = self.center.card.transparent if not self.center.awakened else self.center.card.transparent_awakened
            self._cache_center_card_string = unicode(self.center.card)
        elif self._cache_center_last_update:
            self._cache_center_last_update = None
            self._cache_center_awakened = None
            self._cache_center_card_id = None
            self._cache_center_card_i_type = None
            self._cache_center_card_icon = None
            self._cache_center_card_art = None
            self._cache_center_card_transparent = None
            self._cache_center_card_string = None

    def force_cache_center(self):
        self.update_cache_center()
        self.save()

    @property
    def cached_center(self):
        if not self.center_id:
            return None
        if not self._cache_center_last_update or self._cache_center_last_update < timezone.now() - datetime.timedelta(days=self._cache_center_days):
            self.force_cache_center()
        return AttrDict({
            'pk': self.center_id,
            'id': self.center_id,
            'card_id': self._cache_center_card_id,
            'awakened': self._cache_center_awakened,
            'card': AttrDict({
                'id': self._cache_center_card_id,
                'pk': self._cache_center_card_id,
                'i_type': self._cache_center_card_i_type,
                'type': TYPE_DICT[self._cache_center_card_i_type] if self._cache_center_card_i_type is not None else None,
                'english_type': ENGLISH_TYPE_DICT[self._cache_center_card_i_type] if self._cache_center_card_i_type is not None else None,
                'icon': self._cache_center_card_icon,
                'icon_url': get_image_url(self._cache_center_card_icon),
                'art': self._cache_center_card_art,
                'art_url': get_image_url(self._cache_center_card_art),
                'transparent': self._cache_center_card_transparent,
                'transparent_url': get_image_url(self._cache_center_card_transparent),
                'string': self._cache_center_card_string,
                'item_url': u'/card/{}/{}/'.format(self._cache_center_card_id, tourldash(self._cache_center_card_string)),
                'ajax_item_url': u'/ajax/card/{}/'.format(self._cache_center_card_id),
            }),
        })

    def __unicode__(self):
        return u'{} PLv. {}'.format(self.nickname if self.nickname else self.cached_owner.username, self.level if self.level else '??')

############################################################
# Card

class Card(ItemModel):
    collection_name = 'card'

    owner = models.ForeignKey(User, related_name='added_cards')
    id = models.PositiveIntegerField(_('ID'), unique=True, primary_key=True, db_index=True)
    id_awakened = models.PositiveIntegerField(string_concat(_('ID'), ' (', _('Awakened'), ')'), unique=True, null=True)
    idol = models.ForeignKey(Idol, verbose_name=_('Idol'), related_name='cards', null=True, on_delete=models.SET_NULL)
    i_rarity = models.PositiveIntegerField(_('Rarity'), choices=RARITY_CHOICES)
    @property
    def rarity(self): return RARITY_DICT[self.i_rarity]
    @property
    def short_rarity(self): return RARITY_SHORT_DICT[self.i_rarity]

    @property
    def i_type(self): return self.cached_idol.i_type
    @property
    def type(self): return self.cached_idol.type

    @property
    def english_type(self): return self.cached_idol.english_type

    release_date = models.DateField(_('Release Date'), default=datetime.date(2015, 9, 3), null=True)
    event = models.ForeignKey(Event, verbose_name=_('Event'), related_name='cards', null=True, on_delete=models.SET_NULL, blank=True)
    is_limited = models.BooleanField(_('Limited'), default=False)
    title = models.CharField(string_concat(_('Title'), ' (', t['Japanese'], ')'), max_length=100, null=True)
    translated_title = models.CharField(string_concat(_('Title'), ' (translated in English)'), max_length=100, null=True, blank=True)

    # Images
    image = models.ImageField(_('Image'), upload_to=uploadItem('c'))
    image_awakened = models.ImageField(string_concat(_('Image'), ' (', _('Awakened'), ')'), upload_to=uploadItem('c/a'))
    @property
    def image_awakened_url(self): return get_image_url(self.image_awakened)
    @property
    def http_image_awakened_url(self): return get_http_image_url(self.image_awakened)
    art = models.ImageField(_('Art'), upload_to=uploadItem('c/art'))
    @property
    def art_url(self): return get_image_url(self.art)
    @property
    def http_art_url(self): return get_http_image_url(self.art)
    art_awakened = models.ImageField(string_concat(_('Art'), ' (', _('Awakened'), ')'), upload_to=uploadItem('c/art/a'))
    @property
    def art_awakened_url(self): return get_image_url(self.art_awakened)
    @property
    def http_art_awakened_url(self): return get_http_image_url(self.art_awakened)
    art_hd = models.ImageField(string_concat(_('Art'), ' (HD)'), upload_to=uploadItem('c/art_hd'), null=True)
    @property
    def art_hd_url(self): return get_image_url(self.art_hd)
    @property
    def http_art_hd_url(self): return get_http_image_url(self.art_hd)
    art_hd_awakened = models.ImageField(string_concat(_('Art'), ' (HD ', _('Awakened'), ')'), upload_to=uploadItem('c/art_hd/a'), null=True)
    @property
    def art_hd_awakened_url(self): return get_image_url(self.art_hd_awakened)
    @property
    def http_art_hd_awakened_url(self): return get_http_image_url(self.art_hd_awakened)
    art_on_homepage = models.BooleanField('Show the art on the homepage of the site?', default=True, help_text='Uncheck this if the art looks weird because the idol is not in the center')
    art_awakened_on_homepage = models.BooleanField('Show the awakened art on the homepage of the site?', default=True, help_text='Uncheck this if the awakened art looks weird because the idol is not in the center')
    transparent = models.ImageField(_('Transparent'), upload_to=uploadItem('c/transparent'))
    @property
    def transparent_url(self): return get_image_url(self.transparent)
    @property
    def http_transparent_url(self): return get_http_image_url(self.transparent)
    transparent_awakened = models.ImageField(string_concat(_('Transparent'), ' (', _('Awakened'), ')'), upload_to=uploadItem('c/transparent/a'))
    @property
    def transparent_awakened_url(self): return get_image_url(self.transparent_awakened)
    @property
    def http_transparent_awakened_url(self): return get_http_image_url(self.transparent_awakened)
    icon = models.ImageField(_('Icon'), upload_to=uploadItem('c/icon'))
    @property
    def icon_url(self): return get_image_url(self.icon)
    @property
    def http_icon_url(self): return get_http_image_url(self.icon)
    icon_awakened = models.ImageField(string_concat(_('Icon'), ' (', _('Awakened'), ')'), upload_to=uploadItem('c/icon/a'))
    @property
    def icon_awakened_url(self): return get_image_url(self.icon_awakened)
    @property
    def http_icon_awakened_url(self): return get_http_image_url(self.icon_awakened)
    puchi = models.ImageField(_('Puchi'), upload_to=uploadItem('c/puchi'))
    @property
    def puchi_url(self): return get_image_url(self.puchi)
    @property
    def http_puchi_url(self): return get_http_image_url(self.puchi)
    puchi_awakened = models.ImageField(string_concat(_('Puchi'), ' (', _('Awakened'), ')'), upload_to=uploadItem('c/puchi/a'))
    @property
    def puchi_awakened_url(self): return get_image_url(self.puchi_awakened)
    @property
    def http_puchi_awakened_url(self): return get_http_image_url(self.puchi_awakened)

    # Statistics
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

    # Skill
    max_skill_level = MAX_SKILL_LEVEL
    i_skill = models.PositiveIntegerField(_('Skill'), choices=SKILL_CHOICES, null=True)
    @property
    def skill(self):
        return unicode(SKILL_DICT[self.i_skill]).replace(u'Cute/Cool/Passion', unicode(self.type))
    trigger_value = models.FloatField('Trigger Value', null=True)
    trigger_chance_min = models.FloatField('Trigger Chance (Minimum)', null=True)
    trigger_chance_max = models.FloatField('Trigger Chance (Maximum)', null=True)
    skill_duration_min = models.FloatField('Skill Duration (Minimum)', null=True)
    skill_duration_max = models.FloatField('Skill Duration (Minimum)', null=True)
    skill_value = models.FloatField('Skill Value', null=True)
    skill_value2 = models.FloatField('Other Skill Value', null=True)
    skill_value3 = models.FloatField('Other Skill Value', null=True)
    skill_name = models.CharField('Skill name', max_length=100, null=True)
    translated_skill_name = models.CharField('Translated skill name', max_length=100, null=True, blank=True)

    @property
    def has_skill(self):
        return self.i_skill is not None

    def get_skill_details(self, level=1, japanese=False):
        if self.i_skill is None:
            return None
        return (JAPANESE_SKILL_SENTENCES if japanese else SKILL_SENTENCES)[self.i_skill].format(
            trigger_value='{0:g}'.format(self.trigger_value if self.trigger_value else 0),
            trigger_chance=self._value_for_level('trigger_chance', level, max_level=MAX_SKILL_LEVEL, round_integer=False),
            skill_duration=self._value_for_level('skill_duration', level, max_level=MAX_SKILL_LEVEL, round_integer=False),
            skill_value='{0:g}'.format(self.skill_value if self.skill_value else 0),
            skill_value2='{0:g}'.format(self.skill_value2 if self.skill_value2 else 0),
            skill_value3='{0:g}'.format(self.skill_value3 if self.skill_value3 else 0),
            type=JAPANESE_TYPES[self.cached_idol.i_type] if japanese else self.type,
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

    # Leader skill
    leader_skill_type = models.PositiveIntegerField('Leader Skill: What kind of stat gets raised?', choices=LEADER_SKILL_CHOICES, null=True)
    leader_skill_apply = models.PositiveIntegerField('Leader Skill: Which idols does it apply to?', choices=LEADER_SKILL_APPLIES_CHOICES, null=True)
    leader_skill_percent = models.FloatField('Leader Skill: Percentage', null=True)
    leader_skill_all = models.BooleanField(default=False, help_text='Does the leader skill work on all idols or just the ones with the same type? Check for all') # deprecated

    @property
    def has_leader_skill(self):
        return self.leader_skill_type is not None

    @property
    def leader_skill(self):
        if self.leader_skill_type is None:
            return None
        if self.leader_skill_type in LEADER_SKILLS_WITHOUT_PREFIX:
            return LEADER_SKILL_NAME_SUFFIX[self.leader_skill_type]
        return u'{prefix} {suffix}'.format(
            prefix=LEADER_SKILL_NAME_PREFIX.get(
                self.leader_skill_apply,
                self.type,
            ),
            suffix=LEADER_SKILL_NAME_SUFFIX[self.leader_skill_type],
        )

    @property
    def japanese_leader_skill(self):
        if self.leader_skill_type is None:
            return None
        if self.leader_skill_type in LEADER_SKILLS_WITHOUT_PREFIX:
            return JAPANESE_LEADER_SKILL_NAME_SUFFIX[self.leader_skill_type]
        return u'{prefix} {suffix}'.format(
            prefix=JAPANESE_LEADER_SKILL_NAME_PREFIX.get(
                self.leader_skill_apply,
                JAPANESE_TYPES[self.i_type],
            ),
            suffix=JAPANESE_LEADER_SKILL_NAME_SUFFIX[self.leader_skill_type],
        )

    @property
    def leader_skill_details(self):
        if self.leader_skill_type is None:
            return None
        return LEADER_SKILL_SENTENCES_PER_APPLIES_TO.get(
            self.leader_skill_apply,
            LEADER_SKILL_SENTENCES_PER_SKILL.get(
                self.leader_skill_type,
                LEADER_SKILL_BASE_SENTENCE,
            )).format(
                leader_skill_type=LEADER_SKILL_RAISED_STAT[self.leader_skill_type]().lower(),
                idol_type=self.type.lower(),
                all_types=u'/'.join([unicode(t[1]).lower() for t in TYPE_CHOICES]),
                leader_skill_percent='{0:g}'.format(self.leader_skill_percent if self.leader_skill_percent else 0),
            )

    @property
    def japanese_leader_skill_details(self):
        if self.leader_skill_type is None:
            return None
        return JAPANESE_LEADER_SKILL_SENTENCES_PER_APPLIES_TO.get(
            self.leader_skill_apply,
            JAPANESE_LEADER_SKILL_SENTENCES_PER_SKILL.get(
                self.leader_skill_type,
                JAPANESE_LEADER_SKILL_BASE_SENTENCE,
            )).format(
                leader_skill_type=JAPANESE_LEADER_SKILL_RAISED_STAT[self.leader_skill_type].lower(),
                idol_type=JAPANESE_TYPES[self.i_type],
                all_types=u'/'.join(JAPANESE_TYPES.values()),
                leader_skill_percent='{0:g}'.format(self.leader_skill_percent if self.leader_skill_percent else 0),
            )

    # Raw values
    @property
    def max_level(self):
        return MAX_LEVELS[self.i_rarity][0]
    @property
    def max_level_awakened(self):
        return MAX_LEVELS[self.i_rarity][1]
    @property
    def awakened_or_not(self):
        return (False, True)

    # Cache event
    _cache_event_days = 20
    _cache_event_last_update = models.DateTimeField(null=True)
    _cache_event_name = models.CharField(max_length=100, null=True)
    _cache_event_translated_name = models.CharField(max_length=100, null=True)
    _cache_event_image = models.ImageField(upload_to=uploadItem('e'), null=True, blank=True)

    def update_cache_event(self):
        if self.event_id:
            self._cache_event_last_update = timezone.now()
            self._cache_event_name = self.event.name
            self._cache_event_translated_name = self.event.translated_name
            self._cache_event_image = self.event.image
        elif self._cache_event_last_update:
            self._cache_event_last_update = None
            self._cache_event_name = None
            self._cache_event_translated_name = None
            self._cache_event_image = None

    def force_cache_event(self):
        self.update_cache_event()
        self.save()

    @property
    def cached_event(self):
        if not self.event_id:
            return None
        if not self._cache_event_last_update or self._cache_event_last_update < timezone.now() - datetime.timedelta(days=self._cache_event_days):
            self.force_cache_event()
        return AttrDict({
            'id': self.event_id,
            'pk': self.event_id,
            'name': self._cache_event_name,
            'translated_name': self._cache_event_translated_name,
            'image': self._cache_event_image,
            'image_url': get_image_url(self._cache_event_image),
            'item': u'/event/{}/{}/'.format(self.event_id, tourldash(self._cache_event_translated_name if self._cache_event_translated_name else self._cache_event_name)),
            'ajax_item_url': u'/ajax/event/{}/'.format(self.event_id),
        })

    # Cache idol
    _cache_idol_days = 20
    _cache_idol_last_update = models.DateTimeField(null=True)
    _cache_idol_name = models.CharField(max_length=100, null=True)
    _cache_idol_japanese_name = models.CharField(max_length=100, null=True)
    _cache_idol_i_type = models.PositiveIntegerField(choices=TYPE_CHOICES, null=True)
    _cache_idol_image = models.ImageField(upload_to=uploadItem('idol'), null=True, blank=True)

    def update_cache_idol(self):
        self._cache_idol_last_update = timezone.now()
        self._cache_idol_name = self.idol.name
        self._cache_idol_japanese_name = self.idol.japanese_name
        self._cache_idol_i_type = self.idol.i_type
        self._cache_idol_image = self.idol.image

    def force_cache_idol(self):
        self.update_cache_idol()
        self.save()

    @property
    def cached_idol(self):
        if not self._cache_idol_last_update or self._cache_idol_last_update < timezone.now() - datetime.timedelta(days=self._cache_idol_days):
            self.force_cache_idol()
        return AttrDict({
            'pk': self.idol_id,
            'id': self.idol_id,
            'name': self._cache_idol_name,
            'japanese_name': self._cache_idol_japanese_name,
            'i_type': self._cache_idol_i_type,
            'type': TYPE_DICT[self._cache_idol_i_type] if self._cache_idol_i_type is not None else None,
            'english_type': ENGLISH_TYPE_DICT[self._cache_idol_i_type] if self._cache_idol_i_type is not None else None,
            'image': self._cache_idol_image,
            'image_url': get_image_url(self._cache_idol_image),
            'http_image_url': get_http_image_url(self._cache_idol_image),
            'item_url': u'/idol/{}/{}/'.format(self.idol_id, tourldash(self._cache_idol_name)),
            'ajax_item_url': u'/ajax/idol/{}/'.format(self.idol_id),
        })

    # Cache totals
    _cache_totals_days = 2
    _cache_totals_last_update = models.DateTimeField(null=True)
    _cache_total_owners = models.PositiveIntegerField(null=True)
    _cache_total_favorites = models.PositiveIntegerField(null=True)

    def update_cache_totals(self):
        self._cache_totals_last_update = timezone.now()
        self._cache_total_owners = User.objects.filter(accounts__ownedcards__card=self).distinct().count()
        self._cache_total_favorites = User.objects.filter(favoritecards__card=self).distinct().count()

    def force_cache_totals(self):
        self.update_cache_totals()
        self.save()

    @property
    def cached_total_owners(self):
        if not self._cache_totals_last_update or self._cache_totals_last_update < timezone.now() - datetime.timedelta(hours=self._cache_totals_days):
            self.force_cache_totals()
        return self._cache_total_owners

    @property
    def cached_total_favorites(self):
        if not self._cache_totals_last_update or self._cache_totals_last_update < timezone.now() - datetime.timedelta(hours=self._cache_totals_days):
            self.force_cache_totals()
        return self._cache_total_favorites

    def __unicode__(self):
        if self.id:
            return u'{rarity} {idol_name} {title}'.format(
                rarity=self.short_rarity,
                idol_name=self.cached_idol.name,
                title=u'"{}"'.format(self.translated_title) if self.translated_title else u'',
            )
        return u''

############################################################
# Owned Card

class OwnedCard(ItemModel):
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
        MaxValueValidator(MAX_SKILL_LEVEL),
    ])
    obtained_date = models.DateField(_('Obtained Date'), null=True)

    # Cache account + owner
    _cache_account_days = 200
    _cache_account_last_update = models.DateTimeField(null=True)
    _cache_account_owner_id = models.PositiveIntegerField(null=True)

    def update_cache_account(self):
        self._cache_account_last_update = timezone.now()
        self._cache_account_owner_id = self.account.owner_id

    def force_cache_account(self):
        self.update_cache_account()
        self.save()

    @property
    def cached_account(self):
        if not self._cache_account_last_update or self._cache_account_last_update < timezone.now() - datetime.timedelta(days=self._cache_account_days):
            self.force_cache_account()
        return AttrDict({
            'pk': self.account_id,
            'id': self.account_id,
            'owner': AttrDict({
                'id': self._cache_account_owner_id,
                'pk': self._cache_account_owner_id,
            }),
        })

    @property
    def owner(self):
        return self.cached_account.owner

    @property
    def owner_id(self):
        return self.cached_account.owner.id

    def __unicode__(self):
        return u'#{} {}'.format(self.card_id, u'({})'.format(_('Awakened')) if self.awakened else '')

############################################################
# Favorite Card

class FavoriteCard(ItemModel):
    collection_name = 'favoritecard'

    owner = models.ForeignKey(User, related_name='favoritecards')
    card = models.ForeignKey(Card, related_name='fans', on_delete=models.CASCADE)

    def __unicode__(self):
        return u'#{}'.format(self.card_id)

    class Meta:
        unique_together = (('owner', 'card'),)

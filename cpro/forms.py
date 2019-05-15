import datetime
from django.utils.translation import ugettext_lazy as _, string_concat
from django.conf import settings as django_settings
from django.db.models.fields import BLANK_CHOICE_DASH
from django.core.files.uploadedfile import InMemoryUploadedFile, TemporaryUploadedFile
from django.core.validators import MaxValueValidator, MinValueValidator
from django import forms
from django.core.files.images import ImageFile
from magi.utils import (
    PastOnlyValidator,
)
from magi.item_model import i_choices
from magi.forms import (
    AutoForm,
    MagiForm,
    MagiFilter,
    MagiFiltersForm,
    AccountForm as _AccountForm,
    AccountFilterForm as _AccountFilterForm,
)
from cpro.raw import LICENSES
from cpro.django_translated import t
from cpro import models

############################################################
############################################################
# MagiCircles' default collections
############################################################
############################################################

############################################################
# Account

class AccountForm(_AccountForm):
    level = forms.IntegerField(required=False, label=_('Producer level'), validators=[
        MinValueValidator(1),
        MaxValueValidator(django_settings.STAFF_CONFIGURATIONS.get('max_level', 500)),
    ])

    start_date = forms.DateField(required=False, label=_('Start date'), validators=[
        MinValueValidator(LICENSES['cinderellagirls']['games']['deresute']['release_date']),
        PastOnlyValidator,
    ])

    def __init__(self, *args, **kwargs):
        super(AccountForm, self).__init__(*args, **kwargs)

        if 'center' in self.fields:
            if self.is_creating:
                del(self.fields['center'])
            else:
                self.previous_center_id = self.instance.center_id
                self.fields['center'].queryset = models.OwnedCard.objects.filter(
                    account=self.instance).select_related('card')

    def save(self, commit=False):
        instance = super(_AccountForm, self).save(commit=False)

        if self.previous_center_id != instance.center_id:
            instance.update_cache('center_card')

        if commit:
            instance.save()
        return instance

class AccountFilterForm(_AccountFilterForm):
    starter = forms.ChoiceField(label=_('Starter'), choices=BLANK_CHOICE_DASH + [
        (_starter_id, _starter_details['name'])
        for _starter_id, _starter_details in django_settings.STARTERS.items()
    ])
    center_type = forms.ChoiceField(label=string_concat(_('Center'), ' - ', _('Type')), choices=(
        BLANK_CHOICE_DASH + i_choices(models.TYPE_CHOICES)))
    center_type_filter = MagiFilter(selector='center__card__idol__i_type')

    center_rarity = forms.ChoiceField(label=string_concat(_('Center'), ' - ', _('Rarity')), choices=(
        BLANK_CHOICE_DASH + i_choices(models.Card.RARITY_CHOICES)))
    center_rarity_filter = MagiFilter(selector='center__card__i_rarity')

    def __init__(self, *args, **kwargs):
        super(AccountFilterForm, self).__init__(*args, **kwargs)
        self.reorder_fields([
            'search',
            'has_friend_id',
            'friend_id',
            'accept_friend_requests',
            'starter',
            'center_type',
            'center_rarity',
            'favorite_character',
            'color',
        ])

    class Meta(_AccountFilterForm.Meta):
        fields = _AccountFilterForm.Meta.fields + ['starter', 'accept_friend_requests']

# ############################################################
# # Idol

def getIdolForm(modelClass):
    class _IdolForm(AutoForm):
        def __init__(self, *args, **kwargs):
            super(_IdolForm, self).__init__(*args, **kwargs)
            if 'i_type' in self.fields:
                self.fields['i_type'].choices = i_choices(modelClass.TYPE_CHOICES)

        class Meta(AutoForm.Meta):
            model = modelClass
            fields = '__all__'
    return _IdolForm

class IdolFilterForm(MagiFiltersForm):
    search_fields = ['name', 'japanese_name', 'romaji_hometown', 'hometown', 'hobbies', 'cv', 'romaji_cv']
    ordering_fields = [
        ('_cache_total_fans', _('Popularity')),
        ('name', _('Name')),
        ('age', _('Age')),
        ('birthday', _('Birthday')),
        ('height', _('Height')),
        ('weight', _('Weight')),
        ('bust', _('Bust')),
        ('waist', _('Waist')),
        ('hips', _('Hips')),
    ]

    has_signature = forms.NullBooleanField(label=('Signature'))
    has_signature_filter = MagiFilter(selector='signature__isnull')

    has_cv = forms.NullBooleanField(label=('Voiced'))
    has_cv_filter = MagiFilter(selector='cv__isnull')

    class Meta(MagiFiltersForm.Meta):
        model = models.Idol
        fields = [
            'search',
            'i_type', 'has_cv',
            'i_blood_type', 'i_writing_hand', 'i_astrological_sign',
            'has_signature',
            'ordering', 'reverse_order',
        ]

# ############################################################
# # Event

# class EventForm(FormSaveOwnerOnCreation):
#     beginning = forms.DateField(label=_('Beginning'))
#     end = forms.DateField(label=_('End'))

#     def save(self, commit=False):
#         instance = super(EventForm, self).save(commit=False)
#         instance.beginning = instance.beginning.replace(hour=5, minute=59)
#         instance.end = instance.end.replace(hour=11, minute=59)
#         if commit:
#             instance.save()
#         return instance

#     class Meta:
#         model = models.Event
#         fields = ('name', 'translated_name', 'i_kind', 'image', 'beginning', 'end', 't1_points', 't1_rank', 't2_points', 't2_rank', 't3_points', 't3_rank', 't4_points', 't4_rank', 't5_points', 't5_rank')
#         optional_fields = ('translated_name', 't1_points', 't1_rank', 't2_points', 't2_rank', 't3_points', 't3_rank', 't4_points', 't4_rank', 't5_points', 't5_rank')
#         date_fields = ('beginning', 'end')

# class FilterEvents(FormWithRequest):
#     search = forms.CharField(required=False, label=t['Search'])
#     ordering = forms.ChoiceField(choices=[
#         ('end', _('End')),
#         ('name', _('Name')),
#         ('t1_points', _('T{} points').format(1)),
#         ('t1_rank', _('T{} rank').format(1)),
#     ], initial='end', required=False, label=_('Ordering'))
#     reverse_order = forms.BooleanField(initial=True, required=False, label=_('Reverse Order'))

#     def __init__(self, *args, **kwargs):
#         super(FilterEvents, self).__init__(*args, **kwargs)
#         self.fields['i_kind'].choices = BLANK_CHOICE_DASH + self.fields['i_kind'].choices
#         self.fields['i_kind'].initial = None

#     class Meta:
#         model = models.Event
#         fields = ('search', 'i_kind')
#         optional_fields = ('i_kind',)

# ############################################################
# # Card

# class CardForm(FormSaveOwnerOnCreation):
#     def __init__(self, *args, **kwargs):
#         super(CardForm, self).__init__(*args, **kwargs)
#         self.previous_event_id = None
#         self.previous_event = None
#         self.previous_idol_id = None
#         if hasattr(self, 'instance') and self.instance.pk:
#             self.previous_idol_id = self.instance.idol_id
#             if self.instance.event_id:
#                 self.previous_event_id = self.instance.event_id
#                 self.previous_event = self.instance.event
#         if self.instance and self.instance.id and 'leader_skill_apply' in self.fields:
#             self.fields['leader_skill_apply'].choices = [
#                 (i, u'{type} idols [{type}]'.format(type=self.instance.type) if i is None else v)
#                 for i, v in self.fields['leader_skill_apply'].choices
#             ]

#     def save(self, commit=False):
#         instance = super(CardForm, self).save(commit=False)
#         if self.previous_idol_id != instance.idol_id:
#             instance.update_cache_idol()
#         if self.previous_event_id != instance.event_id:
#             if instance.event:
#                 instance.event.force_cache_totals(pluscards=1)
#             if self.previous_event_id:
#                 self.previous_event.force_cache_totals(pluscards=-1)
#         if self.instance.leader_skill_type in models.LEADER_SKILLS_WITHOUT_PREFIX:
#             self.instance.leader_skill_apply = None
#         if commit:
#             instance.save()
#         return instance

#     class Meta:
#         model = models.Card
#         fields = ('id', 'id_awakened', 'idol', 'i_rarity', 'release_date', 'event', 'is_limited', 'title', 'translated_title', 'image', 'image_awakened', 'art', '_2x_art', 'art_on_homepage', 'art_awakened',  '_2x_art_awakened', 'art_awakened_on_homepage', 'transparent', 'transparent_awakened', 'icon', 'icon_awakened', 'puchi', 'puchi_awakened', 'hp_min', 'hp_max', 'hp_awakened_min', 'hp_awakened_max', 'vocal_min', 'vocal_max', 'vocal_awakened_min', 'vocal_awakened_max', 'dance_min', 'dance_max', 'dance_awakened_min', 'dance_awakened_max', 'visual_min', 'visual_max', 'visual_awakened_min', 'visual_awakened_max', 'skill_name', 'translated_skill_name', 'i_skill', 'trigger_value', 'trigger_chance_min', 'trigger_chance_max', 'skill_duration_min', 'skill_duration_max', 'skill_value', 'skill_value2', 'skill_value3', 'leader_skill_type', 'leader_skill_apply', 'leader_skill_percent')
#         optional_fields = ('id_awakened', 'release_date', 'event', 'title', 'translated_title', 'image_awakened', 'art', '_2x_art', 'art_awakened', '_2x_art_awakened', 'transparent', 'transparent_awakened', 'icon', 'icon_awakened', 'puchi', 'puchi_awakened', 'hp_min', 'hp_max', 'hp_awakened_min', 'hp_awakened_max', 'vocal_min', 'vocal_max', 'vocal_awakened_min', 'vocal_awakened_max', 'dance_min', 'dance_max', 'dance_awakened_min', 'dance_awakened_max', 'visual_min', 'visual_max', 'visual_awakened_min', 'visual_awakened_max', 'skill_name', 'translated_skill_name', 'i_skill', 'trigger_value', 'trigger_chance_min', 'trigger_chance_max', 'skill_duration_min', 'skill_duration_max', 'skill_value', 'skill_value2', 'skill_value3', 'leader_skill_type', 'leader_skill_percent', 'leader_skill_apply')
#         date_fields = ('release_date', )

class CardFilterForm(MagiFiltersForm):
    search_fields = [
        'idol__name', 'idol__japanese_name', 'title', 'translated_title',
        'skill_name', 'translated_skill_name',
    ]
    ordering_fields = [
        ('release_date', _('Release Date')),
        ('id', _('ID')),
        ('idol__name', string_concat(_('Idol'), ' (', _('Name'), ')')),
        ('i_rarity', _('Rarity')),
        ('_cache_total_owners', string_concat(_('Popularity'), ' (', _('Scouted by'), ')')),
        ('_cache_total_favorites', string_concat(_('Popularity'), ' (', _('Favorited by'), ')')),
        ('vocal_max', _('Vocal')),
        ('vocal_awakened_max', string_concat(_('Vocal'), ' (', _('Awakened'), ')')),
        ('dance_max', _('Dance')),
        ('dance_awakened_max', string_concat(_('Dance'), ' (', _('Awakened'), ')')),
        ('visual_max', _('Visual')),
        ('visual_awakened_max', string_concat(_('Visual'), ' (', _('Awakened'), ')')),
        ('hp_max', _('HP')),
        ('hp_awakened_max', string_concat(_('HP'), ' (', _('Awakened'), ')')),
    ]
    merge_fields = {
        'leader_skill': {
            'label': _('Leader skill'),
            'fields': ('i_leader_skill', 'i_leader_skill_apply'),
        },
    }

    i_type = forms.ChoiceField(label=_('Type'), choices=(
        BLANK_CHOICE_DASH + i_choices(models.Idol.TYPE_CHOICES)
    ))

    is_event = forms.NullBooleanField(label=_('Event'))
    is_event_filter = MagiFilter(selector='event__isnull')

    is_limited = forms.NullBooleanField(label=_('Limited'))
    #is_limited_filter = MagiFilter(selector=)

    has_art = forms.NullBooleanField(label=_('Art'))
    has_art_filter = MagiFilter(selector='art__isnull')

    has_2x_art = forms.NullBooleanField(label=string_concat(_('Art'), ' (HD)'))
    has_art_filter = MagiFilter(selector='_2x_art__isnull')

    def __init__(self, *args, **kwargs):
        super(CardFilterForm, self).__init__(*args, **kwargs)
        if 'leader_skill' in self.fields:
            pass#self.fields['leader_skill'].label =

    class Meta(MagiFiltersForm.Meta):
        model = models.Card
        fields = (
            'search', 'i_rarity', 'i_type', 'is_event', 'is_limited', 'has_art', 'has_2x_art',
            'i_skill', 'i_leader_skill', 'i_leader_skill_apply',
            'ordering', 'reverse_order',
        )
#         optional_fields = ('i_skill', 'i_rarity')
# class FilterCards(FormWithRequest):
#     search = forms.CharField(required=False, label=t['Search'])
#     type = forms.ChoiceField(choices=BLANK_CHOICE_DASH + models.TYPE_CHOICES, required=False, label=_('Type'))
#     leader_skill = forms.ChoiceField(required=False, initial=None, label=_('Leader Skill'), choices=(
#         BLANK_CHOICE_DASH + [
#             (u'type-{}'.format(i), models.LEADER_SKILL_NAME_SUFFIX[i])
#             for i, v in models.LEADER_SKILL_CHOICES
#         ] + [
#             (u'apply-{}'.format(i), models.LEADER_SKILL_NAME_PREFIX[i])
#             for i, v in models.LEADER_SKILL_APPLIES_CHOICES
#             if i is not None
#             ]
#     ))
#     ordering = forms.ChoiceField(choices=[
#     ], initial='level', required=False, label=_('Ordering'))
#     reverse_order = forms.BooleanField(initial=True, required=False, label=_('Reverse Order'))

#     class Meta:
#         model = models.Card
#         fields = ('search', 'i_rarity', 'type', 'is_event', 'is_limited', 'has_art', 'has_2x_art', 'i_skill', 'leader_skill', 'ordering', 'reverse_order')
#         optional_fields = ('i_skill', 'i_rarity')

# ############################################################
# # Owned Card

# class EditOwnedCardForm(FormWithRequest):
#     def __init__(self, *args, **kwargs):
#         super(EditOwnedCardForm, self).__init__(*args, **kwargs)
#         self.card = self.instance.card
#         if not self.card.has_skill:
#             del(self.fields['skill_level'])
#         if not self.card.id_awakened:
#             del(self.fields['awakened'])
#         self.previous_awakened = self.instance.awakened

#     def save(self, commit=False):
#         instance = super(EditOwnedCardForm, self).save(commit=False)
#         if self.card.i_rarity == models.RARITY_N and instance.star_rank > 5:
#             instance.star_rank = 5
#         if self.card.i_rarity == models.RARITY_R and instance.star_rank > 10:
#             instance.star_rank = 10
#         if self.card.i_rarity == models.RARITY_SR and instance.star_rank > 15:
#             instance.star_rank = 15
#         if self.previous_awakened != instance.awakened and instance.account.center_id == instance.id:
#             instance.account.center = instance
#             instance.account.force_cache_center()
#         if commit:
#             instance.save()
#         return instance

#     def clean_obtained_date(self):
#         if 'obtained_date' in self.cleaned_data:
#             if self.cleaned_data['obtained_date']:
#                 if self.cleaned_data['obtained_date'] < datetime.date(2015, 9, 2):
#                     raise forms.ValidationError(_('The game didn\'t even exist at that time.'))
#                 if self.cleaned_data['obtained_date'] > datetime.date.today():
#                     raise forms.ValidationError(_('This date cannot be in the future.'))
#         return self.cleaned_data['obtained_date']

#     class Meta:
#         model = models.OwnedCard
#         fields = ('awakened', 'max_bonded', 'max_leveled', 'star_rank', 'skill_level', 'obtained_date')
#         optional_fields = ('star_rank', 'skill_level', 'obtained_date')
#         date_fields = ('obtained_date', )

# class FilterOwnedCards(FormWithRequest):
#     search = forms.CharField(required=False, label=t['Search'])
#     i_rarity = forms.ChoiceField(choices=BLANK_CHOICE_DASH + models.RARITY_CHOICES, required=False, label=_('Rarity'))
#     account = forms.IntegerField(widget=forms.HiddenInput, min_value=0, required=True)
#     type = forms.ChoiceField(choices=BLANK_CHOICE_DASH + models.TYPE_CHOICES, required=False, label=_('Type'))
#     is_event = forms.NullBooleanField(required=False, initial=None, label=_('Event'))
#     i_skill = forms.ChoiceField(choices=BLANK_CHOICE_DASH + models.SKILL_CHOICES, required=False, label=_('Skill'))

#     def __init__(self, *args, **kwargs):
#         super(FilterOwnedCards, self).__init__(*args, **kwargs)
#         self.fields['account'].initial = self.request.GET.get('account', 1)

#     class Meta:
#         model = models.Card
#         fields = ('search', 'i_rarity', 'type', 'is_event', 'i_skill')
#         optional_fields = ('i_skill', 'i_rarity')

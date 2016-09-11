from django.utils.translation import ugettext_lazy as _, string_concat
from django.db.models.fields import BLANK_CHOICE_DASH
from django import forms
from cpro import models

class FormWithRequest(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.is_creating = not hasattr(self, 'instance') or not self.instance.pk
        super(FormWithRequest, self).__init__(*args, **kwargs)
        # Fix optional fields
        if hasattr(self.Meta, 'optional_fields'):
            for field in self.Meta.optional_fields:
                if field in self.fields:
                    self.fields[field].required = False
        # Fix dates inputs
        if hasattr(self.Meta, 'date_fields'):
            for field in self.Meta.date_fields:
                if field in self.fields:
                    self.fields[field] = date_input(self.fields[field])

    def save(self, commit=True):
        instance = super(FormWithRequest, self).save(commit=False)
        # Fix empty strings to None
        for field in self.fields.keys():
            if (hasattr(instance, field)
                and (type(getattr(instance, field)) == unicode or type(getattr(instance, field)) == str)
                and getattr(instance, field) == ''):
                setattr(instance, field, None)
        if commit:
            instance.save()
        return instance

class FormSaveOwnerOnCreation(FormWithRequest):
    def save(self, commit=True):
        instance = super(FormSaveOwnerOnCreation, self).save(commit=False)
        if self.is_creating:
            instance.owner = self.request.user
        if commit:
            instance.save()
        return instance

class DateInput(forms.DateInput):
    input_type = 'date'

def date_input(field):
    field.widget = DateInput()
    field.widget.attrs.update({
        'class': 'calendar-widget',
        'data-role': 'data',
    })
    return field

############################################################
# Account

class _AccountForm(FormWithRequest):
    def __init__(self, *args, **kwargs):
        super(_AccountForm, self).__init__(*args, **kwargs)
        if 'starter' in self.fields:
            self.fields['starter'].queryset = models.Card.objects.filter(pk__in=[100001, 200001, 300001])
            self.fields['starter'].initial = 100001

class AccountFormSimple(_AccountForm):
    class Meta:
        model = models.Account
        fields = ('game_id', 'level', 'starter')
        optional_fields = ('game_id', 'level')

class AccountFormAdvanced(_AccountForm):
    class Meta:
        model = models.Account
        fields = ('nickname', 'game_id', 'level', 'accept_friend_requests', 'device', 'play_with', 'os', 'center', 'starter', 'start_date', 'producer_rank')
        optional_fields = ('nickname', 'game_id', 'level', 'accept_friend_requests', 'device', 'play_with', 'os', 'center', 'start_date', 'producer_rank')
        date_fields = ('start_date', )

############################################################
# Idol

class IdolForm(FormSaveOwnerOnCreation):
    class Meta:
        model = models.Idol
        fields = ('name', 'japanese_name', 'i_type', 'age', 'birthday', 'height', 'weight', 'i_blood_type', 'i_writing_hand', 'bust', 'waist', 'hips', 'i_astrological_sign', 'hometown', 'romaji_hometown', 'hobbies', 'description', 'CV', 'romaji_CV', 'image', 'signature')
        optional_fields = ('japanese_name', 'i_type', 'age', 'birthday', 'height', 'weight', 'i_blood_type', 'i_writing_hand', 'bust', 'waist', 'hips', 'i_astrological_sign', 'hometown', 'romaji_hometown', 'hobbies', 'description', 'CV', 'romaji_CV', 'signature')
        date_fields = ('birthday', )

############################################################
# Event

class EventForm(FormSaveOwnerOnCreation):
    beginning = forms.DateField(label=_('Beginning'))
    end = forms.DateField(label=_('End'))

    class Meta:
        model = models.Event
        fields = ('name', 'translated_name', 'image', 'beginning', 'end', 't1_points', 't1_rank', 't2_points', 't2_rank', 't3_points', 't3_rank', 't4_points', 't4_rank', 't5_points', 't5_rank')
        optional_fields = ('translated_name', 't1_points', 't1_rank', 't2_points', 't2_rank', 't3_points', 't3_rank', 't4_points', 't4_rank', 't5_points', 't5_rank')
        date_fields = ('beginning', 'end')

############################################################
# Card

class CardForm(FormSaveOwnerOnCreation):
    class Meta:
        model = models.Card
        fields = ('id', 'id_awakened', 'idol', 'i_rarity', 'release_date', 'event', 'is_limited', 'title', 'translated_title', 'image', 'image_awakened', 'art', 'art_awakened', 'transparent', 'transparent_awakened', 'icon', 'icon_awakened', 'puchi', 'puchi_awakened', 'hp_min', 'hp_max', 'hp_awakened_min', 'hp_awakened_max', 'vocal_min', 'vocal_max', 'vocal_awakened_min', 'vocal_awakened_max', 'dance_min', 'dance_max', 'dance_awakened_min', 'dance_awakened_max', 'visual_min', 'visual_max', 'visual_awakened_min', 'visual_awakened_max', 'skill_name', 'translated_skill_name', 'i_skill', 'trigger_value', 'trigger_chance_min', 'trigger_chance_max', 'skill_duration_min', 'skill_duration_max', 'skill_value', 'skill_value2')
        optional_fields = ('id_awakened', 'release_date', 'event', 'title', 'translated_title', 'image_awakened', 'art', 'art_awakened', 'transparent', 'transparent_awakened', 'icon', 'icon_awakened', 'puchi', 'puchi_awakened', 'hp_min', 'hp_max', 'hp_awakened_min', 'hp_awakened_max', 'vocal_min', 'vocal_max', 'vocal_awakened_min', 'vocal_awakened_max', 'dance_min', 'dance_max', 'dance_awakened_min', 'dance_awakened_max', 'visual_min', 'visual_max', 'visual_awakened_min', 'visual_awakened_max', 'skill_name', 'translated_skill_name', 'i_skill', 'trigger_value', 'trigger_chance_min', 'trigger_chance_max', 'skill_duration_min', 'skill_duration_max', 'skill_value', 'skill_value2')
        date_fields = ('release_date', )

class FilterCards(FormWithRequest):
    search = forms.CharField(required=False)
    type = forms.ChoiceField(choices=BLANK_CHOICE_DASH + models.TYPE_CHOICES, required=False, label=_('Type'))
    is_event = forms.NullBooleanField(required=False, initial=None, label=_('Event'))
    is_limited = forms.NullBooleanField(required=False, initial=None, label=_('Limited'))
    has_art = forms.NullBooleanField(required=False, initial=None, label=_('Art'))
    ordering = forms.ChoiceField(choices=[
        ('release_date', _('Release Date')),
        ('id', _('ID')),
        ('i_rarity', _('Rarity')),
        ('vocal_max', _('Vocal')),
        ('vocal_awakened_max', string_concat(_('Vocal'), ' (', _('Awakened'), ')')),
        ('dance_max', _('Dance')),
        ('dance_awakened_max', string_concat(_('Dance'), ' (', _('Awakened'), ')')),
        ('visual_max', _('Visual')),
        ('visual_awakened_max', string_concat(_('Visual'), ' (', _('Awakened'), ')')),
        ('hp_max', _('HP')),
        ('hp_awakened_max', string_concat(_('HP'), ' (', _('Awakened'), ')')),
    ], initial='level', required=False)
    reverse_order = forms.BooleanField(initial=True, required=False)

    def __init__(self, *args, **kwargs):
        super(FilterCards, self).__init__(*args, **kwargs)

    class Meta:
        model = models.Card
        fields = ('search', 'i_rarity', 'type', 'is_event', 'is_limited', 'has_art', 'i_skill', 'ordering', 'reverse_order')
        optional_fields = ('i_skill', 'i_rarity')

############################################################
# Owned Card

class EditOwnedCardForm(FormWithRequest):
    class Meta:
        model = models.OwnedCard
        fields = ('awakened', 'max_bonded', 'max_leveled', 'star_rank', 'skill_level')
        date_fields = ('obtained_date', )

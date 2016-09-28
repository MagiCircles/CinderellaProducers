import datetime
from django.utils.translation import ugettext_lazy as _, string_concat
from django.conf import settings as django_settings
from django.db.models.fields import BLANK_CHOICE_DASH
from django.core.files.uploadedfile import InMemoryUploadedFile, TemporaryUploadedFile
from django import forms
from django.core.files.images import ImageFile
from cpro.utils import shrinkImageFromData
from cpro import models

class FormWithRequest(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(FormWithRequest, self).__init__(*args, **kwargs)
        self.is_creating = not hasattr(self, 'instance') or not self.instance.pk
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
            if (hasattr(instance, field)
                and field in dir(self.Meta.model)
                and type(self.Meta.model._meta.get_field(field)) == models.models.ImageField):
                image = self.cleaned_data[field]
                if image and (isinstance(image, InMemoryUploadedFile) or isinstance(image, TemporaryUploadedFile)):
                    filename = image.name
                    image = shrinkImageFromData(image.read(), filename)
                    setattr(instance, field, image)
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
    starter_id = forms.ChoiceField(choices=BLANK_CHOICE_DASH + [(id, full_name) for (id, full_name, image) in getattr(django_settings, 'STARTERS', [])], required=False, label=_('Starter'))

    def __init__(self, *args, **kwargs):
        super(_AccountForm, self).__init__(*args, **kwargs)
        if hasattr(self, 'instance') and self.instance.pk:
            self.previous_center_id = self.instance.center_id
            self.previous_level = self.instance.level
            if self.instance.starter_id:
                self.fields['starter_id'].initial = self.instance.starter_id
        else:
            self.previous_center_id = None
            self.previous_level = None
        if 'center' in self.fields:
            if self.is_creating:
                del(self.fields['center'])
            else:
                self.fields['center'].queryset = models.OwnedCard.objects.filter(account=self.instance).select_related('card')

    def clean_start_date(self):
        if 'start_date' in self.cleaned_data:
            if self.cleaned_data['start_date']:
                if self.cleaned_data['start_date'] < datetime.date(2015, 9, 2):
                    raise forms.ValidationError(_('The game didn\'t even exist at that time.'))
                if self.cleaned_data['start_date'] > datetime.date.today():
                    raise forms.ValidationError(_('This date cannot be in the future.'))
        return self.cleaned_data['start_date']

    def save(self, commit=False):
        instance = super(_AccountForm, self).save(commit=False)
        if 'starter_id' in self.cleaned_data and self.cleaned_data['starter_id']:
            instance.starter_id = self.cleaned_data['starter_id']
        # Remove starter none selected
        if 'starter_id' in self.cleaned_data and not self.cleaned_data['starter_id']:
            instance.starter_id = None
        if self.previous_center_id != instance.center_id:
            instance.update_cache_center()
        if self.previous_level != instance.level:
            instance.update_cache_leaderboard()
        if commit:
            instance.save()
        return instance

class AccountFormSimple(_AccountForm):
    class Meta:
        model = models.Account
        fields = ('game_id', 'level', 'starter_id')
        optional_fields = ('game_id', 'level')

class AccountFormAdvanced(_AccountForm):
    class Meta:
        model = models.Account
        fields = ('nickname', 'game_id', 'level', 'i_producer_rank', 'center', 'starter_id', 'start_date', 'accept_friend_requests', 'i_os', 'device', 'i_play_with')
        optional_fields = ('nickname', 'game_id', 'level', 'accept_friend_requests', 'device', 'i_play_with', 'i_os', 'center', 'starter_id', 'start_date', 'i_producer_rank')
        date_fields = ('start_date', )

class FilterAccounts(FormWithRequest):
    search = forms.CharField(required=False)
    user_type = forms.ChoiceField(choices=BLANK_CHOICE_DASH + models.TYPE_CHOICES, required=False, label=_('Type'))
    center_type = forms.ChoiceField(choices=BLANK_CHOICE_DASH + models.TYPE_CHOICES, required=False, label=string_concat(_('Center'), ' - ', _('Type')))
    center_rarity = forms.ChoiceField(choices=BLANK_CHOICE_DASH + models.RARITY_CHOICES, required=False, label=string_concat(_('Center'), ' - ', _('Rarity')))
    starter_id = forms.ChoiceField(choices=BLANK_CHOICE_DASH + [(id, full_name) for (id, full_name, image) in getattr(django_settings, 'STARTERS', [])], required=False, label=_('Starter'))
    favorite_character = forms.ChoiceField(choices=BLANK_CHOICE_DASH + [(id, full_name) for (id, full_name, image) in getattr(django_settings, 'FAVORITE_CHARACTERS', [])], required=False, label=_('Favorite Idol'))
    ordering = forms.ChoiceField(choices=[
        ('level', _('Level')),
        ('creation', _('Join Date')),
        ('start_date', _('Start Date')),
        ('i_producer_rank', _('Producer Rank')),
    ], initial='level', required=False, label=_('Ordering'))
    reverse_order = forms.BooleanField(initial=True, required=False, label=_('Reverse Order'))

    def __init__(self, *args, **kwargs):
        super(FilterAccounts, self).__init__(*args, **kwargs)
        self.fields['accept_friend_requests'].label = _('Accept friend requests')
        self.fields['accept_friend_requests'].help_text = None

    class Meta:
        model = models.Account
        fields = ('search', 'game_id', 'user_type', 'favorite_character', 'starter_id', 'center_type', 'center_rarity', 'accept_friend_requests')
        optional_fields = ('game_id',)

############################################################
# Idol

class IdolForm(FormSaveOwnerOnCreation):
    class Meta:
        model = models.Idol
        fields = ('name', 'japanese_name', 'i_type', 'age', 'birthday', 'height', 'weight', 'i_blood_type', 'i_writing_hand', 'bust', 'waist', 'hips', 'i_astrological_sign', 'hometown', 'romaji_hometown', 'hobbies', 'description', 'CV', 'romaji_CV', 'image', 'signature')
        optional_fields = ('japanese_name', 'i_type', 'age', 'birthday', 'height', 'weight', 'i_blood_type', 'i_writing_hand', 'bust', 'waist', 'hips', 'i_astrological_sign', 'hometown', 'romaji_hometown', 'hobbies', 'description', 'CV', 'romaji_CV', 'signature')
        date_fields = ('birthday', )

class FilterIdols(FormWithRequest):
    search = forms.CharField(required=False)
    type = forms.ChoiceField(choices=BLANK_CHOICE_DASH + models.TYPE_CHOICES, required=False, label=_('Type'))
    ordering = forms.ChoiceField(choices=[
        ('name', _('Name')),
        ('age', _('Age')),
        ('birthday', _('Birthday')),
        ('height', _('Height')),
        ('weight', _('Weight')),
        ('bust', _('Bust')),
        ('waist', _('Waist')),
        ('hips', _('Hips')),
    ], initial='name', required=False)
    reverse_order = forms.BooleanField(initial=False, required=False)

    def __init__(self, *args, **kwargs):
        super(FilterIdols, self).__init__(*args, **kwargs)

    class Meta:
        model = models.Idol
        fields = ('search', 'ordering', 'reverse_order', 'type', 'i_blood_type', 'i_writing_hand', 'i_astrological_sign')
        optional_fields = ('i_blood_type', 'i_writing_hand', 'i_astrological_sign')

############################################################
# Event

class EventForm(FormSaveOwnerOnCreation):
    beginning = forms.DateField(label=_('Beginning'))
    end = forms.DateField(label=_('End'))

    def save(self, commit=False):
        instance = super(EventForm, self).save(commit=False)
        instance.beginning = instance.beginning.replace(hour=5, minute=59)
        instance.end = instance.end.replace(hour=11, minute=59)
        if commit:
            instance.save()
        return instance

    class Meta:
        model = models.Event
        fields = ('name', 'translated_name', 'i_kind', 'image', 'beginning', 'end', 't1_points', 't1_rank', 't2_points', 't2_rank', 't3_points', 't3_rank', 't4_points', 't4_rank', 't5_points', 't5_rank')
        optional_fields = ('translated_name', 't1_points', 't1_rank', 't2_points', 't2_rank', 't3_points', 't3_rank', 't4_points', 't4_rank', 't5_points', 't5_rank')
        date_fields = ('beginning', 'end')

class FilterEvents(FormWithRequest):
    search = forms.CharField(required=False)
    ordering = forms.ChoiceField(choices=[
        ('end', _('End')),
        ('name', _('Name')),
        ('t1_points', _('T{} points').format(1)),
        ('t1_rank', _('T{} rank').format(1)),
    ], initial='end', required=False)
    reverse_order = forms.BooleanField(initial=True, required=False)

    def __init__(self, *args, **kwargs):
        super(FilterEvents, self).__init__(*args, **kwargs)
        self.fields['i_kind'].choices = BLANK_CHOICE_DASH + self.fields['i_kind'].choices
        self.fields['i_kind'].initial = None

    class Meta:
        model = models.Event
        fields = ('search', 'i_kind')
        optional_fields = ('i_kind',)

############################################################
# Card

class CardForm(FormSaveOwnerOnCreation):
    def __init__(self, *args, **kwargs):
        super(CardForm, self).__init__(*args, **kwargs)
        if hasattr(self, 'instance') and self.instance.pk:
            self.previous_idol_id = self.instance.idol_id
        else:
            self.previous_idol_id = None

    def save(self, commit=False):
        instance = super(CardForm, self).save(commit=False)
        if self.previous_idol_id != instance.idol_id:
            instance.update_cache_idol()
        if commit:
            instance.save()
        return instance

    class Meta:
        model = models.Card
        fields = ('id', 'id_awakened', 'idol', 'i_rarity', 'release_date', 'event', 'is_limited', 'title', 'translated_title', 'image', 'image_awakened', 'art', 'art_on_homepage', 'art_awakened', 'art_awakened_on_homepage', 'transparent', 'transparent_awakened', 'icon', 'icon_awakened', 'puchi', 'puchi_awakened', 'hp_min', 'hp_max', 'hp_awakened_min', 'hp_awakened_max', 'vocal_min', 'vocal_max', 'vocal_awakened_min', 'vocal_awakened_max', 'dance_min', 'dance_max', 'dance_awakened_min', 'dance_awakened_max', 'visual_min', 'visual_max', 'visual_awakened_min', 'visual_awakened_max', 'skill_name', 'translated_skill_name', 'i_skill', 'trigger_value', 'trigger_chance_min', 'trigger_chance_max', 'skill_duration_min', 'skill_duration_max', 'skill_value', 'skill_value2')
        optional_fields = ('id_awakened', 'release_date', 'event', 'title', 'translated_title', 'image_awakened', 'art', 'art_awakened', 'transparent', 'transparent_awakened', 'icon', 'icon_awakened', 'puchi', 'puchi_awakened', 'hp_min', 'hp_max', 'hp_awakened_min', 'hp_awakened_max', 'vocal_min', 'vocal_max', 'vocal_awakened_min', 'vocal_awakened_max', 'dance_min', 'dance_max', 'dance_awakened_min', 'dance_awakened_max', 'visual_min', 'visual_max', 'visual_awakened_min', 'visual_awakened_max', 'skill_name', 'translated_skill_name', 'i_skill', 'trigger_value', 'trigger_chance_min', 'trigger_chance_max', 'skill_duration_min', 'skill_duration_max', 'skill_value', 'skill_value2')
        date_fields = ('release_date', )

class FilterCards(FormWithRequest):
    search = forms.CharField(required=False)
    type = forms.ChoiceField(choices=BLANK_CHOICE_DASH + models.TYPE_CHOICES, required=False, label=_('Type'))
    is_event = forms.NullBooleanField(required=False, initial=None, label=_('Event'))
    is_limited = forms.NullBooleanField(required=False, initial=None, label=_('Limited'))
    is_awakened = forms.NullBooleanField(required=False, initial=None, label=_('Awakened'))
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
        fields = ('search', 'i_rarity', 'type', 'is_event', 'is_limited', 'is_awakened', 'has_art', 'i_skill', 'ordering', 'reverse_order')
        optional_fields = ('i_skill', 'i_rarity')

############################################################
# Owned Card

class EditOwnedCardForm(FormWithRequest):
    def __init__(self, *args, **kwargs):
        super(EditOwnedCardForm, self).__init__(*args, **kwargs)
        self.card = self.instance.card
        if not self.card.has_skill:
            del(self.fields['skill_level'])
        if not self.card.id_awakened:
            del(self.fields['awakened'])
        self.previous_awakened = self.instance.awakened

    def save(self, commit=False):
        instance = super(EditOwnedCardForm, self).save(commit=False)
        if self.card.i_rarity == models.RARITY_N and instance.star_rank > 5:
            instance.star_rank = 5
        if self.card.i_rarity == models.RARITY_R and instance.star_rank > 10:
            instance.star_rank = 10
        if self.card.i_rarity == models.RARITY_SR and instance.star_rank > 15:
            instance.star_rank = 15
        if self.previous_awakened != instance.awakened and instance.account.center_id == instance.id:
            instance.account.center = instance
            instance.account.force_cache_center()
        if commit:
            instance.save()
        return instance

    def clean_obtained_date(self):
        if 'obtained_date' in self.cleaned_data:
            if self.cleaned_data['obtained_date']:
                if self.cleaned_data['obtained_date'] < datetime.date(2015, 9, 2):
                    raise forms.ValidationError(_('The game didn\'t even exist at that time.'))
                if self.cleaned_data['obtained_date'] > datetime.date.today():
                    raise forms.ValidationError(_('This date cannot be in the future.'))
        return self.cleaned_data['obtained_date']

    class Meta:
        model = models.OwnedCard
        fields = ('awakened', 'max_bonded', 'max_leveled', 'star_rank', 'skill_level', 'obtained_date')
        optional_fields = ('star_rank', 'skill_level', 'obtained_date')
        date_fields = ('obtained_date', )

class FilterOwnedCards(FormWithRequest):
    search = forms.CharField(required=False)
    i_rarity = forms.ChoiceField(choices=BLANK_CHOICE_DASH + models.RARITY_CHOICES, required=False, label=_('Rarity'))
    account = forms.IntegerField(widget=forms.HiddenInput, min_value=0, required=True)
    type = forms.ChoiceField(choices=BLANK_CHOICE_DASH + models.TYPE_CHOICES, required=False, label=_('Type'))
    is_event = forms.NullBooleanField(required=False, initial=None, label=_('Event'))
    i_skill = forms.ChoiceField(choices=BLANK_CHOICE_DASH + models.SKILL_CHOICES, required=False, label=_('Skill'))

    def __init__(self, *args, **kwargs):
        super(FilterOwnedCards, self).__init__(*args, **kwargs)
        self.fields['account'].initial = self.request.GET.get('account', 1)

    class Meta:
        model = models.Card
        fields = ('search', 'i_rarity', 'type', 'is_event', 'i_skill')
        optional_fields = ('i_skill', 'i_rarity')

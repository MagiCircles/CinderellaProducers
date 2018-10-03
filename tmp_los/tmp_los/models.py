from django.utils.translation import ugettext_lazy as _
from django.db import models
from magi.models import User
from magi.item_model import MagiModel
from magi.abstract_models import BaseAccount
from magi.utils import uploadItem
from tmp_los.django_translated import t
from tmp_los.model_choices import *

class Account(BaseAccount):
    class Meta:
        pass

class Idol(MagiModel):
    collection_name = 'idol'

    owner = models.ForeignKey(User, related_name='added_idols')
    name = models.CharField(string_concat(_('Name'), ' (romaji)'), max_length=100, unique=True)
    japanese_name = models.CharField(string_concat(_('Name'), ' (', t['Japanese'], ')'), max_length=100, null=True)
    i_type = models.PositiveIntegerField(_('Type'), choices=TYPE_CHOICES, null=True)
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

    def __unicode__(self):
        return self.name

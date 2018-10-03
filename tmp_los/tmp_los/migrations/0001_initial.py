# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import magi.utils


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('_cache_owner_last_update', models.DateTimeField(null=True)),
                ('_cache_owner_username', models.CharField(max_length=32, null=True)),
                ('_cache_owner_email', models.EmailField(max_length=75, blank=True)),
                ('_cache_owner_preferences_i_status', models.CharField(max_length=12, null=True)),
                ('_cache_owner_preferences_twitter', models.CharField(max_length=32, null=True, blank=True)),
                ('_cache_owner_color', models.CharField(max_length=100, null=True, blank=True)),
                ('creation', models.DateTimeField(auto_now_add=True, verbose_name='Join date')),
                ('nickname', models.CharField(help_text="Give a nickname to your account to easily differentiate it from your other accounts when you're managing them.", max_length=200, null=True, verbose_name='Nickname')),
                ('start_date', models.DateField(null=True, verbose_name='Start date')),
                ('level', models.PositiveIntegerField(null=True, verbose_name='Level')),
                ('default_tab', models.CharField(max_length=100, null=True, verbose_name='Default tab')),
                ('_cache_leaderboards_last_update', models.DateTimeField(null=True)),
                ('_cache_leaderboard', models.PositiveIntegerField(null=True)),
                ('owner', models.ForeignKey(related_name='accounts', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Idol',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=100, verbose_name='Name (romaji)')),
                ('japanese_name', models.CharField(max_length=100, null=True, verbose_name='Name (Japanese)')),
                ('i_type', models.PositiveIntegerField(null=True, verbose_name='Type', choices=[(0, 'Cute'), (1, 'Cool'), (2, 'Passion')])),
                ('age', models.PositiveIntegerField(null=True, verbose_name='Age')),
                ('birthday', models.DateField(help_text=b'The year is not used, so write whatever', null=True, verbose_name='Birthday')),
                ('height', models.PositiveIntegerField(help_text=b'in cm', null=True, verbose_name='Height')),
                ('weight', models.PositiveIntegerField(help_text=b'in kg', null=True, verbose_name='Weight')),
                ('i_blood_type', models.PositiveIntegerField(null=True, verbose_name='Blood Type', choices=[(0, b'O'), (1, b'A'), (2, b'B'), (3, b'AB')])),
                ('i_writing_hand', models.PositiveIntegerField(null=True, verbose_name='Writing Hand', choices=[(0, 'Right'), (1, 'Left'), (2, 'Both')])),
                ('bust', models.PositiveIntegerField(help_text=b'in cm', null=True, verbose_name='Bust')),
                ('waist', models.PositiveIntegerField(help_text=b'in cm', null=True, verbose_name='Waist')),
                ('hips', models.PositiveIntegerField(help_text=b'in cm', null=True, verbose_name='Hips')),
                ('i_astrological_sign', models.PositiveIntegerField(null=True, verbose_name='Astrological Sign', choices=[(0, 'Leo'), (1, 'Aries'), (2, 'Libra'), (3, 'Virgo'), (4, 'Scorpio'), (5, 'Capricorn'), (6, 'Pisces'), (7, 'Gemini'), (8, 'Cancer'), (9, 'Sagittarius'), (10, 'Aquarius'), (11, 'Taurus')])),
                ('hometown', models.CharField(help_text=b'In Japanese characters.', max_length=100, null=True, verbose_name='Hometown')),
                ('romaji_hometown', models.CharField(help_text=b'In romaji.', max_length=100, null=True, verbose_name='Hometown')),
                ('hobbies', models.CharField(max_length=100, null=True, verbose_name='Hobbies')),
                ('description', models.TextField(null=True, verbose_name='Description')),
                ('CV', models.CharField(help_text=b'In Japanese characters.', max_length=100, null=True, verbose_name='CV')),
                ('romaji_CV', models.CharField(help_text=b'In romaji.', max_length=100, null=True, verbose_name='CV')),
                ('image', models.ImageField(upload_to=magi.utils.uploadItem(b'i'), verbose_name='Image')),
                ('signature', models.ImageField(upload_to=magi.utils.uploadItem(b'i/sign'), null=True, verbose_name='Signature')),
                ('owner', models.ForeignKey(related_name='added_idols', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]

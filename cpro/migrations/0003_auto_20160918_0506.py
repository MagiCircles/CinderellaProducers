# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import cpro.models


class Migration(migrations.Migration):

    dependencies = [
        ('cpro', '0002_auto_20160916_2110'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='_cache_event_image',
            field=models.ImageField(null=True, upload_to=cpro.models.uploadItem(b'e'), blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='_cache_event_last_update',
            field=models.DateTimeField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='_cache_event_name',
            field=models.CharField(max_length=100, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='_cache_event_translated_name',
            field=models.CharField(max_length=100, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='event',
            name='i_kind',
            field=models.PositiveIntegerField(default=0, verbose_name='Kind', choices=[(0, 'Token'), (1, 'Medley'), (2, 'Coop'), (3, 'Caravan')]),
            preserve_default=True,
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cpro', '0009_auto_20161001_0532'),
    ]

    operations = [
        migrations.AddField(
            model_name='idol',
            name='_cache_total_cards',
            field=models.PositiveIntegerField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='idol',
            name='_cache_total_events',
            field=models.PositiveIntegerField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='idol',
            name='_cache_total_fans',
            field=models.PositiveIntegerField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='idol',
            name='_cache_totals_last_update',
            field=models.DateTimeField(null=True),
            preserve_default=True,
        ),
    ]

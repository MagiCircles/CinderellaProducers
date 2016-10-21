# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cpro', '0010_auto_20161016_2319'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='_cache_total_cards',
            field=models.PositiveIntegerField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='_cache_totals_last_update',
            field=models.DateTimeField(null=True),
            preserve_default=True,
        ),
    ]

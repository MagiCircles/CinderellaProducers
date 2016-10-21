# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cpro', '0011_auto_20161021_0935'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='_cache_total_favorites',
            field=models.PositiveIntegerField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='_cache_total_owners',
            field=models.PositiveIntegerField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='_cache_totals_last_update',
            field=models.DateTimeField(null=True),
            preserve_default=True,
        ),
    ]

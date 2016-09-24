# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cpro', '0003_auto_20160918_0506'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='_cache_owner_preferences_status',
            field=models.CharField(max_length=12, null=True, choices=[(b'THANKS', b'Thanks'), (b'SUPPORTER', 'Skilled Producer'), (b'LOVER', 'Expert Producer'), (b'AMBASSADOR', 'Veteran Producer'), (b'PRODUCER', 'Ultimate Producer'), (b'DEVOTEE', 'Idol Master')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='event',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Name (Japanese)'),
            preserve_default=True,
        ),
    ]

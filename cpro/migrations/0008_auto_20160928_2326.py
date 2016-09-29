# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cpro', '0007_auto_20160928_2324'),
    ]

    operations = [
        migrations.AddField(
            model_name='favoritecard',
            name='owner',
            field=models.ForeignKey(related_name='favoritecards', default=1, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='favoritecard',
            unique_together=set([('owner', 'card')]),
        ),
        migrations.RemoveField(
            model_name='favoritecard',
            name='account',
        ),
        migrations.RemoveField(
            model_name='favoritecard',
            name='_cache_account_owner_id',
        ),
        migrations.RemoveField(
            model_name='favoritecard',
            name='_cache_account_last_update',
        ),
    ]

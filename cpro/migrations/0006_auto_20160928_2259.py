# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cpro', '0005_auto_20160928_2235'),
    ]

    operations = [
        migrations.CreateModel(
            name='FavoriteCard',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('_cache_account_last_update', models.DateTimeField(null=True)),
                ('_cache_account_owner_id', models.PositiveIntegerField(null=True)),
                ('account', models.ForeignKey(related_name='favorites', to='cpro.Account')),
                ('card', models.ForeignKey(related_name='fans', to='cpro.Card')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='card',
            name='leader_skill_all',
            field=models.BooleanField(default=False, help_text=b'Does the leader skill work on all idols or just the ones with the same type? Check for all'),
            preserve_default=True,
        ),
    ]

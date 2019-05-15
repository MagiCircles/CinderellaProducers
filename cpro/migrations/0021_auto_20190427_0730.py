# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import magi.utils


class Migration(migrations.Migration):

    dependencies = [
        ('cpro', '0020_auto_20190424_0327'),
    ]

    operations = [
        migrations.RenameField(
            model_name='account',
            old_name='_cache_leaderboard_last_update',
            new_name='_cache_leaderboards_last_update',
        ),
        migrations.RenameField(
            model_name='account',
            old_name='game_id',
            new_name='friend_id',
        ),
        migrations.RenameField(
            model_name='card',
            old_name='leader_skill_type',
            new_name='i_leader_skill',
        ),
        migrations.RemoveField(
            model_name='account',
            name='_cache_center_awakened',
        ),
        migrations.RemoveField(
            model_name='account',
            name='_cache_center_card_art',
        ),
        migrations.RemoveField(
            model_name='account',
            name='_cache_center_card_i_type',
        ),
        migrations.RemoveField(
            model_name='account',
            name='_cache_center_card_icon',
        ),
        migrations.RemoveField(
            model_name='account',
            name='_cache_center_card_id',
        ),
        migrations.RemoveField(
            model_name='account',
            name='_cache_center_card_string',
        ),
        migrations.RemoveField(
            model_name='account',
            name='_cache_center_card_transparent',
        ),
        migrations.RemoveField(
            model_name='account',
            name='_cache_center_last_update',
        ),
        migrations.RemoveField(
            model_name='account',
            name='_cache_owner_preferences_status',
        ),
        migrations.RemoveField(
            model_name='card',
            name='_cache_event_image',
        ),
        migrations.RemoveField(
            model_name='card',
            name='_cache_event_name',
        ),
        migrations.RemoveField(
            model_name='card',
            name='_cache_event_translated_name',
        ),
        migrations.RemoveField(
            model_name='card',
            name='_cache_idol_i_type',
        ),
        migrations.RemoveField(
            model_name='card',
            name='_cache_idol_image',
        ),
        migrations.RemoveField(
            model_name='card',
            name='_cache_idol_japanese_name',
        ),
        migrations.RemoveField(
            model_name='card',
            name='_cache_idol_name',
        ),
        migrations.RemoveField(
            model_name='card',
            name='_cache_totals_last_update',
        ),
        migrations.RemoveField(
            model_name='card',
            name='leader_skill_all',
        ),
        migrations.RemoveField(
            model_name='event',
            name='_cache_totals_last_update',
        ),
        migrations.RemoveField(
            model_name='idol',
            name='_cache_totals_last_update',
        ),
        migrations.RemoveField(
            model_name='ownedcard',
            name='_cache_account_owner_id',
        ),
        migrations.AddField(
            model_name='account',
            name='_cache_owner_color',
            field=models.CharField(max_length=100, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='account',
            name='_cache_owner_preferences_i_status',
            field=models.CharField(max_length=12, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='account',
            name='default_tab',
            field=models.CharField(max_length=100, null=True, verbose_name='Default tab'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='_cache_j_event',
            field=models.TextField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='_cache_j_idol',
            field=models.TextField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='_cache_total_favorites_last_update',
            field=models.DateTimeField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='_cache_total_owners_last_update',
            field=models.DateTimeField(null=True),
            preserve_default=True,
        ),
        migrations.RenameField(
            model_name='card',
            old_name='leader_skill_apply',
            new_name='i_leader_skill_apply',
        ),
        migrations.AddField(
            model_name='event',
            name='_cache_total_cards_last_update',
            field=models.DateTimeField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='idol',
            name='_cache_total_cards_last_update',
            field=models.DateTimeField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='idol',
            name='_cache_total_events_last_update',
            field=models.DateTimeField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='idol',
            name='_cache_total_fans_last_update',
            field=models.DateTimeField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ownedcard',
            name='_cache_j_account',
            field=models.TextField(null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='account',
            name='_cache_owner_email',
            field=models.EmailField(default='db0company@gmail.com', max_length=75, blank=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='account',
            name='_cache_owner_preferences_twitter',
            field=models.CharField(max_length=32, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='account',
            name='creation',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Join date'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='account',
            name='i_os',
            field=models.PositiveIntegerField(null=True, verbose_name='Operating System', choices=[(0, b'Android'), (1, b'iOs')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='account',
            name='level',
            field=models.PositiveIntegerField(null=True, verbose_name='Level'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='account',
            name='nickname',
            field=models.CharField(help_text="Give a nickname to your account to easily differentiate it from your other accounts when you're managing them.", max_length=200, null=True, verbose_name='Nickname'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='account',
            name='start_date',
            field=models.DateField(null=True, verbose_name='Start date'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='card',
            name='_2x_art',
            field=models.ImageField(upload_to=magi.utils.upload2x(b'c/art'), null=True, verbose_name='Art (HD)'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='card',
            name='_2x_art_awakened',
            field=models.ImageField(upload_to=magi.utils.upload2x(b'c/art/a'), null=True, verbose_name='Art (HD Awakened)'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='card',
            name='i_skill',
            field=models.PositiveIntegerField(null=True, verbose_name='Skill', choices=[(0, 'Lesser Perfect Lock'), (1, 'Greater Perfect Lock'), (2, 'Extreme Perfect Lock'), (3, 'Combo Guard'), (4, 'Healer'), (5, 'Life Guard'), (6, 'Combo Bonus'), (7, 'Perfect Score Bonus'), (8, 'Overload'), (9, 'Score Bonus'), (10, 'All Round'), (11, 'Concentration'), (12, 'Skill Boost'), (13, 'Cute/Cool/Passion Focus'), (14, 'Encore'), (15, 'Life Sparkle'), (16, 'Tricolor Synergy'), (17, 'Focus')]),
            preserve_default=True,
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import magi.utils


class Migration(migrations.Migration):

    dependencies = [
        ('cpro', '0019_auto_20181002_0245'),
    ]

    operations = [
        migrations.RenameField(
            model_name='card',
            old_name='art_hd',
            new_name='_2x_art',
        ),
        migrations.RenameField(
            model_name='card',
            old_name='art_hd_awakened',
            new_name='_2x_art_awakened',
        ),
    ]

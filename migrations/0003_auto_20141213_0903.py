# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lp', '0002_countdown_repeat'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='countdown',
            options={'ordering': ['updated_at', 'name', 'to_datetime'], 'verbose_name': 'Count Down', 'verbose_name_plural': 'Count Downs'},
        ),
        migrations.RenameField(
            model_name='countdown',
            old_name='icon',
            new_name='img',
        ),
    ]

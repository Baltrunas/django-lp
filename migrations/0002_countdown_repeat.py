# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='countdown',
            name='repeat',
            field=models.PositiveIntegerField(default=0, null=True, verbose_name='Repeat each in hours', blank=True),
            preserve_default=True,
        ),
    ]

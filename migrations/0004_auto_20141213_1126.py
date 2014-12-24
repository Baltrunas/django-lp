# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lp', '0003_auto_20141213_0903'),
    ]

    operations = [
        migrations.AlterField(
            model_name='countdown',
            name='img',
            field=models.ImageField(default=0, upload_to=b'img/countdown', null=True, verbose_name='Image', blank=True),
            preserve_default=True,
        ),
    ]

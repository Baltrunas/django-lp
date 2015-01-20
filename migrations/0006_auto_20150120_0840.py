# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lp', '0005_siteconfig_sms_key'),
    ]

    operations = [
        migrations.AlterField(
            model_name='siteconfig',
            name='sms_name',
            field=models.CharField(help_text='From 2 to 11 Latin characters. As senders, we endorse only the names of sites, organizations or brands.', max_length=11, verbose_name='SMS Name'),
            preserve_default=True,
        ),
    ]

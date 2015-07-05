# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20150411_1504'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='modified_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 7, 5, 1, 6, 43, 699200, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
    ]

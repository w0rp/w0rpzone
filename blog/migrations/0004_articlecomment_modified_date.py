# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_article_modified_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='articlecomment',
            name='modified_date',
            field=models.DateTimeField(auto_now=True, default=datetime.datetime(2015, 7, 5, 1, 8, 2, 931568, tzinfo=utc)),
            preserve_default=False,
        ),
    ]

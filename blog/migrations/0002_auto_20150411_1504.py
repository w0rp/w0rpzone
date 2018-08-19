# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogauthor',
            name='author',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL, help_text='', on_delete=models.CASCADE),
        ),
    ]

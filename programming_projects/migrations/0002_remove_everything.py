# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2017-03-07 19:24
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('programming_projects', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='ddoc',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='ddoc',
            name='project',
        ),
        migrations.RemoveField(
            model_name='extrasource',
            name='project',
        ),
        migrations.DeleteModel(
            name='DDoc',
        ),
        migrations.DeleteModel(
            name='ExtraSource',
        ),
        migrations.DeleteModel(
            name='Project',
        ),
    ]

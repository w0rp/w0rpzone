# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DDoc',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('location', models.CharField(max_length=255)),
                ('html', models.TextField()),
            ],
            options={
                'ordering': ('location',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ExtraSource',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('source_directory', models.CharField(max_length=65535, verbose_name='Source Directory')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('active', models.BooleanField(help_text='Switch this on to make the project public.', default=False)),
                ('time_updated', models.DateTimeField()),
                ('name', models.CharField(max_length=255, help_text='Set the name for this project, for display.', verbose_name='Project Name')),
                ('slug', models.SlugField(max_length=255, help_text='A slug for the project, used in generated output.')),
                ('language', models.CharField(max_length=255, choices=[('d', 'D')], help_text='This field will be used to decide the method used for generating documentation', verbose_name='Programming Language')),
                ('source_directory', models.CharField(max_length=65535, verbose_name='Source Directory')),
                ('source_url', models.URLField(max_length=255, help_text="Set this to a URL for the project's source code.", verbose_name='Source URL')),
                ('summary_line', models.CharField(max_length=255)),
                ('description', models.TextField(help_text='Input Markdown here to describe the project.', default='')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='extrasource',
            name='project',
            field=models.ForeignKey(related_name='extra_sources', to='programming_projects.Project'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ddoc',
            name='project',
            field=models.ForeignKey(related_name='ddocs', to='programming_projects.Project'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='ddoc',
            unique_together=set([('project', 'location')]),
        ),
    ]

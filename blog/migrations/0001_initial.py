# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('active', models.BooleanField(default=False)),
                ('creation_date', models.DateTimeField()),
                ('slug', models.SlugField(max_length=55)),
                ('title', models.CharField(max_length=55)),
                ('content', models.TextField()),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)),
            ],
            options={
                'ordering': ['-creation_date'],
                'db_table': 'blog_article',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ArticleComment',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('poster_name', models.CharField(blank=True, verbose_name='Name', max_length=255)),
                ('content', models.TextField(verbose_name='Comment')),
                ('article', models.ForeignKey(related_name='comments', to='blog.Article', on_delete=models.CASCADE)),
            ],
            options={
                'ordering': ['creation_date'],
                'db_table': 'blog_articlecomment',
                'get_latest_by': 'creation_date',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ArticleFile',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('file', models.FileField(upload_to="%Y-%m-%dT%H:%M:%SZ/")),
                ('article', models.ForeignKey(to='blog.Article', on_delete=models.CASCADE)),
            ],
            options={
                'db_table': 'blog_articlefile',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ArticleTag',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('tag', models.CharField(db_index=True, max_length=255)),
                ('article', models.ForeignKey(related_name='tags', to='blog.Article', on_delete=models.CASCADE)),
            ],
            options={
                'db_table': 'blog_articletag',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BlogAuthor',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('author', models.ForeignKey(unique=True, to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)),
            ],
            options={
                'db_table': 'blog_blogauthor',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Commenter',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('ip_address', models.GenericIPAddressField(unique=True)),
                ('time_banned', models.DateTimeField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='articletag',
            unique_together=set([('article', 'tag')]),
        ),
        migrations.AddField(
            model_name='articlecomment',
            name='commenter',
            field=models.ForeignKey(related_name='comments', to='blog.Commenter', on_delete=models.CASCADE),
            preserve_default=True,
        ),
        migrations.AlterIndexTogether(
            name='article',
            index_together=set([('creation_date', 'active')]),
        ),
    ]

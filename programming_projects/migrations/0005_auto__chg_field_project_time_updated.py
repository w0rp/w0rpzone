# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Project.time_updated'
        db.alter_column('programming_projects_project', 'time_updated', self.gf('django.db.models.fields.DateTimeField')())

    def backwards(self, orm):

        # Changing field 'Project.time_updated'
        db.alter_column('programming_projects_project', 'time_updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True))

    models = {
        'programming_projects.ddoc': {
            'Meta': {'ordering': "('location',)", 'object_name': 'DDoc', 'unique_together': "(('project', 'location'),)"},
            'html': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['programming_projects.Project']", 'related_name': "'ddocs'"})
        },
        'programming_projects.extrasource': {
            'Meta': {'object_name': 'ExtraSource'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['programming_projects.Project']", 'related_name': "'extra_sources'"}),
            'source_directory': ('django.db.models.fields.CharField', [], {'max_length': '65535'})
        },
        'programming_projects.project': {
            'Meta': {'object_name': 'Project'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'description': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255'}),
            'source_directory': ('django.db.models.fields.CharField', [], {'max_length': '65535'}),
            'source_url': ('django.db.models.fields.URLField', [], {'max_length': '255'}),
            'summary_line': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'time_updated': ('django.db.models.fields.DateTimeField', [], {})
        }
    }

    complete_apps = ['programming_projects']
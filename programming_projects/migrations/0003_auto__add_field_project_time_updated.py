# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Project.time_updated'
        db.add_column('programming_projects_project', 'time_updated',
                      self.gf('django.db.models.fields.DateTimeField')(blank=True, auto_now=True, default=datetime.datetime(2014, 3, 20, 0, 0)),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Project.time_updated'
        db.delete_column('programming_projects_project', 'time_updated')


    models = {
        'programming_projects.ddoc': {
            'Meta': {'unique_together': "(('project', 'location'),)", 'ordering': "('location',)", 'object_name': 'DDoc'},
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
            'time_updated': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now': 'True', 'default': 'datetime.datetime(2014, 3, 20, 0, 0)'})
        }
    }

    complete_apps = ['programming_projects']
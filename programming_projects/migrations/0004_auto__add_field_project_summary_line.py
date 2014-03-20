# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Project.summary_line'
        db.add_column('programming_projects_project', 'summary_line',
                      self.gf('django.db.models.fields.CharField')(max_length=255, default=''),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Project.summary_line'
        db.delete_column('programming_projects_project', 'summary_line')


    models = {
        'programming_projects.ddoc': {
            'Meta': {'ordering': "('location',)", 'unique_together': "(('project', 'location'),)", 'object_name': 'DDoc'},
            'html': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'ddocs'", 'to': "orm['programming_projects.Project']"})
        },
        'programming_projects.extrasource': {
            'Meta': {'object_name': 'ExtraSource'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'extra_sources'", 'to': "orm['programming_projects.Project']"}),
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
            'time_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True', 'default': 'datetime.datetime(2014, 3, 20, 0, 0)'})
        }
    }

    complete_apps = ['programming_projects']
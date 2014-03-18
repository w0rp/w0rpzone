# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Project'
        db.create_table('programming_projects_project', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=255)),
            ('language', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('source_directory', self.gf('django.db.models.fields.CharField')(max_length=65535)),
            ('source_url', self.gf('django.db.models.fields.URLField')(max_length=255)),
        ))
        db.send_create_signal('programming_projects', ['Project'])

        # Adding model 'ExtraSource'
        db.create_table('programming_projects_extrasource', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(related_name='extra_sources', to=orm['programming_projects.Project'])),
            ('source_directory', self.gf('django.db.models.fields.CharField')(max_length=65535)),
        ))
        db.send_create_signal('programming_projects', ['ExtraSource'])

        # Adding model 'DDoc'
        db.create_table('programming_projects_ddoc', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(related_name='ddocs', to=orm['programming_projects.Project'])),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('html', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('programming_projects', ['DDoc'])

        # Adding unique constraint on 'DDoc', fields ['project', 'location']
        db.create_unique('programming_projects_ddoc', ['project_id', 'location'])


    def backwards(self, orm):
        # Removing unique constraint on 'DDoc', fields ['project', 'location']
        db.delete_unique('programming_projects_ddoc', ['project_id', 'location'])

        # Deleting model 'Project'
        db.delete_table('programming_projects_project')

        # Deleting model 'ExtraSource'
        db.delete_table('programming_projects_extrasource')

        # Deleting model 'DDoc'
        db.delete_table('programming_projects_ddoc')


    models = {
        'programming_projects.ddoc': {
            'Meta': {'unique_together': "(('project', 'location'),)", 'object_name': 'DDoc'},
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
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255'}),
            'source_directory': ('django.db.models.fields.CharField', [], {'max_length': '65535'}),
            'source_url': ('django.db.models.fields.URLField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['programming_projects']
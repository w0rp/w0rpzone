# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Company'
        db.create_table('hording_company', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('hording', ['Company'])

        # Adding model 'Region'
        db.create_table('hording_region', (
            ('code', self.gf('django.db.models.fields.CharField')(max_length=2, primary_key=True)),
            ('name', self.gf('django.db.models.fields.TextField')(unique=True)),
        ))
        db.send_create_signal('hording', ['Region'])

        # Adding model 'Game'
        db.create_table('hording_game', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.TextField')()),
            ('developer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['hording.Company'])),
        ))
        db.send_create_signal('hording', ['Game'])

        # Adding model 'Platform'
        db.create_table('hording_platform', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.TextField')(unique=True)),
        ))
        db.send_create_signal('hording', ['Platform'])

        # Adding model 'GameRelease'
        db.create_table('hording_gamerelease', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('game', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['hording.Game'])),
            ('platform', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['hording.Platform'])),
            ('region', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['hording.Region'])),
            ('publisher', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['hording.Company'])),
            ('release_date', self.gf('django.db.models.fields.DateField')(blank=True)),
        ))
        db.send_create_signal('hording', ['GameRelease'])

        # Adding unique constraint on 'GameRelease', fields ['region', 'platform', 'publisher', 'game']
        db.create_unique('hording_gamerelease', ['region_id', 'platform_id', 'publisher_id', 'game_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'GameRelease', fields ['region', 'platform', 'publisher', 'game']
        db.delete_unique('hording_gamerelease', ['region_id', 'platform_id', 'publisher_id', 'game_id'])

        # Deleting model 'Company'
        db.delete_table('hording_company')

        # Deleting model 'Region'
        db.delete_table('hording_region')

        # Deleting model 'Game'
        db.delete_table('hording_game')

        # Deleting model 'Platform'
        db.delete_table('hording_platform')

        # Deleting model 'GameRelease'
        db.delete_table('hording_gamerelease')


    models = {
        'hording.company': {
            'Meta': {'object_name': 'Company'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {})
        },
        'hording.game': {
            'Meta': {'object_name': 'Game'},
            'developer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['hording.Company']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.TextField', [], {})
        },
        'hording.gamerelease': {
            'Meta': {'object_name': 'GameRelease', 'unique_together': "(('region', 'platform', 'publisher', 'game'),)"},
            'game': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['hording.Game']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'platform': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['hording.Platform']"}),
            'publisher': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['hording.Company']"}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['hording.Region']"}),
            'release_date': ('django.db.models.fields.DateField', [], {'blank': 'True'})
        },
        'hording.platform': {
            'Meta': {'object_name': 'Platform'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {'unique': 'True'})
        },
        'hording.region': {
            'Meta': {'object_name': 'Region'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '2', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {'unique': 'True'})
        }
    }

    complete_apps = ['hording']
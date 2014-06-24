# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'VG.is_locked'
        db.add_column(u'ssdfrontend_vg', 'is_locked',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'VG.is_locked'
        db.delete_column(u'ssdfrontend_vg', 'is_locked')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'ssdfrontend.aagroup': {
            'Meta': {'object_name': 'AAGroup'},
            'hosts': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['ssdfrontend.StorageHost']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'target': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ssdfrontend.Target']", 'null': 'True', 'blank': 'True'})
        },
        u'ssdfrontend.clumpgroup': {
            'Meta': {'object_name': 'ClumpGroup'},
            'hosts': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['ssdfrontend.StorageHost']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'target': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ssdfrontend.Target']", 'null': 'True', 'blank': 'True'})
        },
        u'ssdfrontend.lv': {
            'Meta': {'object_name': 'LV'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'lvname': ('django.db.models.fields.CharField', [], {'default': "'Not found'", 'max_length': '200'}),
            'lvsize': ('django.db.models.fields.FloatField', [], {}),
            'lvthinmapped': ('django.db.models.fields.FloatField', [], {'default': '-1'}),
            'lvuuid': ('django.db.models.fields.CharField', [], {'max_length': '200', 'primary_key': 'True'}),
            'target': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ssdfrontend.Target']"}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'vg': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ssdfrontend.VG']"})
        },
        u'ssdfrontend.profile': {
            'Meta': {'object_name': 'Profile'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_alloc_sizeGB': ('django.db.models.fields.FloatField', [], {'default': '400.0'}),
            'max_target_sizeGB': ('django.db.models.fields.FloatField', [], {'default': '100.0'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        },
        u'ssdfrontend.provisioner': {
            'Meta': {'object_name': 'Provisioner'},
            'clientiqn': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'serviceName': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'sizeinGB': ('django.db.models.fields.FloatField', [], {})
        },
        u'ssdfrontend.storagehost': {
            'Meta': {'object_name': 'StorageHost'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'dnsname': ('django.db.models.fields.CharField', [], {'max_length': '200', 'primary_key': 'True'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'ipaddress': ('django.db.models.fields.GenericIPAddressField', [], {'default': "'127.0.0.1'", 'max_length': '39'}),
            'storageip1': ('django.db.models.fields.GenericIPAddressField', [], {'default': "'127.0.0.1'", 'max_length': '39'}),
            'storageip2': ('django.db.models.fields.GenericIPAddressField', [], {'default': "'127.0.0.1'", 'max_length': '39'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'})
        },
        u'ssdfrontend.target': {
            'Meta': {'object_name': 'Target'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'iqnini': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'iqntar': ('django.db.models.fields.CharField', [], {'max_length': '200', 'primary_key': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'rkb': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'rkbpm': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'sessionup': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'sizeinGB': ('django.db.models.fields.FloatField', [], {'max_length': '200'}),
            'targethost': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ssdfrontend.StorageHost']"}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'wkb': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'wkbpm': ('django.db.models.fields.BigIntegerField', [], {'default': '0'})
        },
        u'ssdfrontend.targethistory': {
            'Meta': {'object_name': 'TargetHistory'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'deleted_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iqnini': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'iqntar': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'rkb': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'sizeinGB': ('django.db.models.fields.FloatField', [], {'max_length': '200'}),
            'wkb': ('django.db.models.fields.BigIntegerField', [], {'default': '0'})
        },
        u'ssdfrontend.vg': {
            'CurrentAllocGB': ('django.db.models.fields.FloatField', [], {'default': '-100.0', 'null': 'True'}),
            'Meta': {'object_name': 'VG'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_locked': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'maxthinavlGB': ('django.db.models.fields.FloatField', [], {'default': '-1'}),
            'opf': ('django.db.models.fields.FloatField', [], {'default': '0.7'}),
            'thintotalGB': ('django.db.models.fields.FloatField', [], {'default': '-1'}),
            'thinusedmaxpercent': ('django.db.models.fields.FloatField', [], {'default': '70'}),
            'thinusedpercent': ('django.db.models.fields.FloatField', [], {'default': '-1'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'vgfreepe': ('django.db.models.fields.FloatField', [], {'default': '-1'}),
            'vghost': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ssdfrontend.StorageHost']"}),
            'vgpesize': ('django.db.models.fields.FloatField', [], {}),
            'vgsize': ('django.db.models.fields.FloatField', [], {}),
            'vgtotalpe': ('django.db.models.fields.FloatField', [], {}),
            'vguuid': ('django.db.models.fields.CharField', [], {'max_length': '200', 'primary_key': 'True'})
        }
    }

    complete_apps = ['ssdfrontend']
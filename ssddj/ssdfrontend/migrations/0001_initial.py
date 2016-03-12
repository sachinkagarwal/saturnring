# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import ssdfrontend.models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AAGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='ClumpGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Interface',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ip', models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='IPRange',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('iprange', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Lock',
            fields=[
                ('lockname', models.CharField(max_length=100, serialize=False, primary_key=True)),
                ('locked', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='LV',
            fields=[
                ('lvname', models.CharField(default=b'Not found', max_length=200)),
                ('lvsize', models.FloatField()),
                ('lvuuid', models.CharField(max_length=200, serialize=False, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('isencrypted', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('user', models.OneToOneField(primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('max_target_sizeGB', models.FloatField(default=0)),
                ('max_alloc_sizeGB', models.FloatField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Provisioner',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('clientiqn', models.CharField(max_length=100)),
                ('sizeinGB', models.FloatField()),
                ('serviceName', models.CharField(max_length=100, validators=[ssdfrontend.models.validate_nospecialcharacters])),
            ],
        ),
        migrations.CreateModel(
            name='SnapJob',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('numsnaps', models.IntegerField(default=1)),
                ('cronstring', models.CharField(max_length=100)),
                ('lastrun', models.DateTimeField(blank=True)),
                ('nextrun', models.DateTimeField(blank=True)),
                ('created_at', models.DateTimeField(null=True, blank=True)),
                ('deleted_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('enqueued', models.BooleanField(default=False)),
                ('run_now', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='StorageHost',
            fields=[
                ('dnsname', models.CharField(max_length=200, serialize=False, primary_key=True)),
                ('ipaddress', models.GenericIPAddressField(default=b'127.0.0.1')),
                ('storageip1', models.GenericIPAddressField(default=b'127.0.0.1')),
                ('storageip2', models.GenericIPAddressField(default=b'127.0.0.1')),
                ('enabled', models.BooleanField(default=True)),
                ('snaplock', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Target',
            fields=[
                ('iqnini', models.CharField(max_length=200)),
                ('iqntar', models.CharField(max_length=200, serialize=False, primary_key=True)),
                ('sizeinGB', models.FloatField(max_length=200)),
                ('sessionup', models.BooleanField(default=False)),
                ('rkb', models.BigIntegerField(default=0)),
                ('rkbpm', models.BigIntegerField(default=0)),
                ('wkb', models.BigIntegerField(default=0)),
                ('wkbpm', models.BigIntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('storageip1', models.GenericIPAddressField(default=b'127.0.0.1')),
                ('storageip2', models.GenericIPAddressField(default=b'127.0.0.1')),
                ('isencrypted', models.BooleanField(default=False)),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('targethost', models.ForeignKey(to='ssdfrontend.StorageHost')),
            ],
        ),
        migrations.CreateModel(
            name='TargetHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('iqntar', models.CharField(max_length=200)),
                ('iqnini', models.CharField(max_length=200, null=True, blank=True)),
                ('created_at', models.DateTimeField(null=True, blank=True)),
                ('deleted_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('sizeinGB', models.FloatField(max_length=200)),
                ('rkb', models.BigIntegerField(default=0)),
                ('wkb', models.BigIntegerField(default=0)),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='VG',
            fields=[
                ('vgsize', models.FloatField()),
                ('vguuid', models.CharField(max_length=200, serialize=False, primary_key=True)),
                ('vgpesize', models.FloatField()),
                ('vgtotalpe', models.FloatField()),
                ('vgfreepe', models.FloatField(default=-1)),
                ('totalGB', models.FloatField(default=-1)),
                ('maxavlGB', models.FloatField(default=-1)),
                ('enabled', models.BooleanField(default=True)),
                ('CurrentAllocGB', models.FloatField(default=-100.0, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('is_locked', models.BooleanField(default=False)),
                ('in_error', models.BooleanField(default=False)),
                ('storemedia', models.CharField(default=b'unassigned', max_length=200, choices=[(b'unassigned', b'unassigned'), (b'PCIEcard1', b'PCIEcard1'), (b'PCIEcard2', b'PCIEcard2'), (b'PCIEcard3', b'PCIEcard3')])),
                ('is_thin', models.BooleanField(default=True)),
                ('vghost', models.ForeignKey(to='ssdfrontend.StorageHost')),
            ],
        ),
        migrations.AddField(
            model_name='snapjob',
            name='iqntar',
            field=models.ForeignKey(to='ssdfrontend.Target'),
        ),
        migrations.AddField(
            model_name='lv',
            name='target',
            field=models.ForeignKey(to='ssdfrontend.Target'),
        ),
        migrations.AddField(
            model_name='lv',
            name='vg',
            field=models.ForeignKey(to='ssdfrontend.VG'),
        ),
        migrations.AddField(
            model_name='iprange',
            name='hosts',
            field=models.ManyToManyField(to='ssdfrontend.StorageHost'),
        ),
        migrations.AddField(
            model_name='iprange',
            name='owner',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='interface',
            name='iprange',
            field=models.ManyToManyField(to='ssdfrontend.IPRange'),
        ),
        migrations.AddField(
            model_name='interface',
            name='owner',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='interface',
            name='storagehost',
            field=models.ForeignKey(to='ssdfrontend.StorageHost'),
        ),
        migrations.AddField(
            model_name='clumpgroup',
            name='hosts',
            field=models.ManyToManyField(to='ssdfrontend.StorageHost'),
        ),
        migrations.AddField(
            model_name='clumpgroup',
            name='target',
            field=models.ForeignKey(blank=True, to='ssdfrontend.Target', null=True),
        ),
        migrations.AddField(
            model_name='aagroup',
            name='hosts',
            field=models.ManyToManyField(to='ssdfrontend.StorageHost'),
        ),
        migrations.AddField(
            model_name='aagroup',
            name='target',
            field=models.ForeignKey(blank=True, to='ssdfrontend.Target', null=True),
        ),
    ]

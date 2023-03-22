# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0005_auto_20150708_1511'),
    ]

    operations = [
        migrations.CreateModel(
            name='SampleNetwork',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name=b'Network Name')),
                ('network_file', models.FileField(upload_to=b'sample-networks', verbose_name=b'Network File')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]

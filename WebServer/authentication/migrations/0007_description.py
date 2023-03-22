# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0006_samplenetwork'),
    ]

    operations = [
        migrations.CreateModel(
            name='Description',
            fields=[
                ('description', models.TextField(verbose_name=b'Description')),
                ('position', models.IntegerField(unique=True, serialize=False, verbose_name=b'Position', primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]

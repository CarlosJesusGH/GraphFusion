# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Feature',
            fields=[
                ('name', models.CharField(max_length=100, verbose_name=b'Name')),
                ('description', models.TextField(verbose_name=b'Description')),
                ('position', models.IntegerField(serialize=False, verbose_name=b'Position', primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]

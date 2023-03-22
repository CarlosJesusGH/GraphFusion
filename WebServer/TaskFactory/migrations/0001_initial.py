# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('taskId', models.AutoField(serialize=False, verbose_name=b'Task ID', primary_key=True)),
                ('taskName', models.CharField(max_length=100, verbose_name=b'Task Name')),
                ('finished', models.BooleanField(default=False, verbose_name=b'Task Finished')),
                ('error_occurred', models.BooleanField(default=False, verbose_name=b'Error Occurred')),
                ('task_type', models.CharField(default=b'', max_length=100, verbose_name=b'Task Type', choices=[(b'Alignment', b'Alignment'), (b'Properties', b'Properties'), (b'PairwiseAnalysis', b'PairwiseAnalysis'), (b'DataVsModel', b'DataVsModel')])),
                ('started_at', models.DateTimeField(auto_now_add=True)),
                ('finished_at', models.DateTimeField(null=True, blank=True)),
                ('operational_directory', models.CharField(max_length=100, verbose_name=b'Operational Directory')),
                ('error_text', models.TextField(default=b'', verbose_name=b'Error Text', blank=True)),
                ('user', models.ForeignKey(related_name='User', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]

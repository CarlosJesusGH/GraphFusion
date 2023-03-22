# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TaskFactory', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='task_type',
            field=models.CharField(default=b'', max_length=100, verbose_name=b'Task Type', choices=[(b'Alignment', b'Alignment'), (b'Properties', b'Properties'), (b'PairwiseAnalysis', b'PairwiseAnalysis'), (b'DataVsModel', b'DataVsModel'), (b'CanonicalCorrelation', b'CanonicalCorrelation')]),
            preserve_default=True,
        ),
    ]

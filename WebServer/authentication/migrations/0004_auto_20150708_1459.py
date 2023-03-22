# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_auto_20150708_1448'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feature',
            name='image',
            field=models.ImageField(upload_to=b'media/features', verbose_name=b'Image', blank=True),
            preserve_default=True,
        ),
    ]

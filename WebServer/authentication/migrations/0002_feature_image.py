# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='feature',
            name='image',
            field=models.ImageField(upload_to=b'', verbose_name=b'Image', blank=True),
            preserve_default=True,
        ),
    ]

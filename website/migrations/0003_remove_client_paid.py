# -*- coding: utf-8 -*-
# Generated by Django 1.11.24 on 2019-11-12 01:14
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0002_auto_20191111_1815'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='client',
            name='paid',
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.11.24 on 2019-11-21 02:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0003_remove_client_paid'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reminder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('in_progress', models.BooleanField(default=False)),
            ],
        ),
    ]

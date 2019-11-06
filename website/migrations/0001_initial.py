# -*- coding: utf-8 -*-
# Generated by Django 1.11.24 on 2019-11-05 03:01
from __future__ import unicode_literals

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=254)),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None)),
                ('total_amount_due', models.DecimalField(decimal_places=2, max_digits=5)),
                ('payment_amount', models.DecimalField(decimal_places=2, max_digits=5)),
                ('next_payment_date', models.DateField()),
                ('paid', models.BooleanField(default=False)),
            ],
        ),
    ]

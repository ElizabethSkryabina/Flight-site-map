# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-22 08:51
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('flightapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='airport',
            name='airport_name',
        ),
    ]

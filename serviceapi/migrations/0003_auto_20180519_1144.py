# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-05-19 14:44
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('serviceapi', '0002_auto_20180519_1006'),
    ]

    operations = [
        migrations.AlterField(
            model_name='endrecord',
            name='call_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='serviceapi.StartRecord'),
        ),
    ]

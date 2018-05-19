# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class StartRecord(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    call_id = models.BigIntegerField(unique=True)
    source = models.CharField(max_length=11)
    destination = models.CharField(max_length=11)

class EndRecord(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    call_id = models.ForeignKey(StartRecord, db_column='call_id')

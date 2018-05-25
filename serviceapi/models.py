# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class StartRecord(models.Model):
    id = models.BigIntegerField(primary_key=True, unique=True)
    timestamp = models.DateTimeField()
    call_id = models.BigIntegerField(unique=True)
    source = models.CharField(max_length=11)
    destination = models.CharField(max_length=11)

    def __init__(self, id, timestamp, call_id, source, destination):
        self.id = id
        self.timestamp = timestamp
        self.call_id = call_id
        self.source = source
        self.destination = destination

class EndRecord(models.Model):
    id = models.BigIntegerField(primary_key=True, unique=True)
    timestamp = models.DateTimeField()
    call_id = models.ForeignKey(StartRecord, to_field='call_id', unique=True)

    def __init__(self, id, timestamp, call_id):
        self.id = id
        self.timestamp = timestamp
        self.call_id = call_id

class CostRecord(models.Model):
    call_id = models.ForeignKey(EndRecord, to_field='call_id', unique=True)
    cost = models.FloatField()

    def __init__(self, call_id, cost):
        self.call_id = call_id
        self.cost = cost

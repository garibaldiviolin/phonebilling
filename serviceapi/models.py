# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from serviceapi.utils import RecordType


class StartRecord(models.Model):
    ''' Represents the call start record received from the REST API'''
    id = models.BigIntegerField(primary_key=True, unique=True)
    timestamp = models.DateTimeField()
    call_id = models.BigIntegerField(unique=True)
    source = models.CharField(max_length=11)
    destination = models.CharField(max_length=11)

    @property
    def type(self):
        return RecordType.START.value


class EndRecord(models.Model):
    ''' Represents the call end record received from the REST API.
    It also stores the call's cost
    '''
    id = models.BigIntegerField(primary_key=True, unique=True)
    timestamp = models.DateTimeField()
    start = models.ForeignKey(
        StartRecord, to_field='call_id', on_delete=models.CASCADE
    )
    cost = models.FloatField()

    @property
    def type(self):
        return RecordType.END.value

    @property
    def call_id(self):
        return self.start_id

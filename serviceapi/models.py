# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from serviceapi.utils import RecordType


class StartRecord(models.Model):
    ''' Represents the start call record received from the REST API'''
    id = models.BigIntegerField(primary_key=True, unique=True)
    timestamp = models.DateTimeField()
    call_id = models.BigIntegerField(unique=True)
    source = models.CharField(max_length=11)
    destination = models.CharField(max_length=11)


class EndRecord(models.Model):
    ''' Represents the end call record received from the REST API.
    It also stores the calculated cost of the call
    '''
    id = models.BigIntegerField(primary_key=True, unique=True)
    timestamp = models.DateTimeField()
    call_id = models.ForeignKey(
        StartRecord, to_field='call_id', unique=True,
        on_delete=models.CASCADE
    )
    cost = models.FloatField()

    @property
    def type(self):
        return RecordType.END.value

    '''@property
    def source(self):
        return ''

    @property
    def destination(self):
        return '''

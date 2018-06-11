# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pdb

from django.dispatch import receiver
from django.db.models.signals import pre_save
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
    start = models.OneToOneField(
        StartRecord, to_field='call_id', on_delete=models.CASCADE,
        unique=True
    )
    cost = models.FloatField()

    @property
    def type(self):
        return RecordType.END.value

    @property
    def call_id(self):
        return self.start_id

    '''@receiver(pre_save)
    def pre_save_end_record(sender, instance, *args, **kwargs):

        pdb.set_trace()

        queryset_endrecord = EndRecord.objects.filter(id=instance.id)
        if len(queryset_endrecord) > 1:
            old_end_record = queryset_endrecord[0]
            start_record = StartRecord.objects.get(
                call_id=old_end_record.start_id
            )

            EndRecord.objects.filter(id=old_end_record.id).delete()
            StartRecord.objects.filter(id=start_record.id).delete()

            start_record.call_id = instance.start_id
            start_record.save()

        # User object updated
        return instance'''

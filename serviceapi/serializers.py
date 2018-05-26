# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime

from django.utils import timezone
from django.contrib.auth.models import User, Group
from rest_framework import serializers
from rest_framework.response import Response

from serviceapi.models import StartRecord, EndRecord, CostRecord
from serviceapi.utils import *


class StartRecordSerializer(serializers.HyperlinkedModelSerializer):

    id = serializers.IntegerField()
    timestamp = serializers.DateTimeField()
    call_id = serializers.IntegerField()
    source = serializers.CharField()
    destination = serializers.CharField()

    class Meta:
        model = StartRecord
        fields = ('id','timestamp','call_id', 'source', 'destination')

    def validate(self, data):
        if data['source'].isdigit() == False:
            raise serializers.ValidationError("Source must have only numbers")
        elif len(data['source']) != 11 and len(data['source']) != 12:
            raise serializers.ValidationError("Source must have 10 or 11 digits")

        if data['destination'].isdigit() == False:
            raise serializers.ValidationError("Destination must have only numbers")
        elif len(data['destination']) != 11 and len(data['destination']) != 12:
            raise serializers.ValidationError("Destination must have 10 or 11 digits")

        if data['source'] == data['destination']:
            raise serializers.ValidationError("Source and destination must have different values")

        return data

    def create(self, validated_data):
        start_record = StartRecord()
        start_record.id = validated_data['id']
        start_record.timestamp = validated_data['timestamp'].replace(tzinfo=timezone.utc)
        start_record.call_id = validated_data['call_id']
        start_record.source = validated_data['source']
        start_record.destination = validated_data['destination']
        start_record.save()
        return start_record


class EndRecordSerializer(serializers.HyperlinkedModelSerializer):

    id = serializers.IntegerField()
    timestamp = serializers.DateTimeField()
    call_id_id = serializers.IntegerField()

    class Meta:
        model = EndRecord
        fields = ('id','timestamp','call_id_id')

    def validate(self, data):

        record_exist_1 = EndRecord.objects.filter(id=data['id'])
        record_exist_2 = EndRecord.objects.filter(call_id_id=data['call_id_id'])
        if len(record_exist_1) > 0:
            raise serializers.ValidationError("The id already exists")
        elif len(record_exist_2) > 0:
            raise serializers.ValidationError("The call_id already exists")

        start_record = StartRecord.objects.get(call_id=data['call_id_id'])
        end_timestamp = data['timestamp'].replace(tzinfo=timezone.utc)
        if start_record is None:
            raise serializers.ValidationError("Please insert the call start before the end")
        elif start_record.timestamp >= end_timestamp:
            raise serializers.ValidationError("The call end timestamp must be greater than call start timestamp")

        return data

    def create(self, validated_data):
        id = validated_data['id']
        timestamp = validated_data['timestamp']
        call_id_id = validated_data['call_id_id']
        end_record = EndRecord()
        end_record.id = id
        end_record.timestamp = timestamp
        end_record.call_id_id = call_id_id
        end_record.save()

        start_record = StartRecord.objects.get(call_id=call_id_id)

        cost = calculate_call_cost(start_record.timestamp, end_record.timestamp)

        record_cost = CostRecord()
        record_cost.call_id = end_record
        record_cost.cost = cost
        record_cost.save()

        return end_record

class PhoneBillSerializer(serializers.Serializer):

    destination = serializers.CharField(max_length=100)
    start_date = serializers.CharField(max_length=100)
    start_time = serializers.CharField(max_length=100)
    duration = serializers.CharField(max_length=100)
    price = serializers.CharField(max_length=100)

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pdb

from django.utils import timezone
from rest_framework import serializers

from serviceapi.models import StartRecord, EndRecord, CallRecord
from serviceapi.utils import *


class CallRecordSerializer(serializers.Serializer):
    ''' Represents the serializer for the call start record '''

    id = serializers.IntegerField()
    timestamp = serializers.DateTimeField()
    call_id = serializers.IntegerField()
    type = serializers.IntegerField()
    source = serializers.CharField(required=False)
    destination = serializers.CharField(required=False)

    def get_validation_exclusions(self):
        exclusions = super(FavoriteListSerializer, self). \
            get_validation_exclusions()
        return exclusions + ['source'] + ['destination']

    def validate(self, data):
        ''' Validate if source and destination are numbers, check
        their length (must be 10 or 11 digits), and also if they are
        two different phone numbers.
        '''

        if data['type'] != RecordType.START.value and \
                data['type'] != RecordType.END.value:
            raise serializers.ValidationError('Type must be 1 or 2')

        if data['type'] == RecordType.START.value:
            if data['source'].isdigit() is False:
                raise serializers. \
                    ValidationError("Source must have only numbers")
            elif len(data['source']) != 10 and len(data['source']) != 11:
                raise serializers. \
                    ValidationError("Source must have 10 or 11 digits")

            if data['destination'].isdigit() is False:
                raise serializers. \
                    ValidationError("Destination must have only numbers")
            elif len(data['destination']) != 10 and \
                    len(data['destination']) != 11:
                raise serializers. \
                    ValidationError("Destination must have 10 or 11 digits")

            if data['source'] == data['destination']:
                raise serializers.ValidationError(
                    "Source and destination must have different values")
        else:  # end record
            start_record = StartRecord.objects.get(call_id=data['call_id'])
            end_timestamp = data['timestamp'].replace(tzinfo=timezone.utc)
            if start_record is None:
                raise serializers.ValidationError("Please insert the call"
                                                    "start before the end")
            elif start_record.timestamp >= end_timestamp:
                raise serializers.ValidationError(
                    "The call end timestamp must be"
                    "greater than call start timestamp"
                )

        return data

    def create(self, validated_data):

        if validated_data['type'] == RecordType.START.value:

            start_record = StartRecord()
            start_record.id = validated_data['id']
            start_record.timestamp = validated_data['timestamp']. \
                replace(tzinfo=timezone.utc)
            start_record.call_id = validated_data['call_id']
            start_record.source = validated_data['source']
            start_record.destination = validated_data['destination']
            start_record.save()

            return start_record

        else:  # RecordType.END

            id = validated_data['id']
            timestamp = validated_data['timestamp']
            call_id_id = validated_data['call_id']
            end_record = EndRecord()
            end_record.id = id
            end_record.timestamp = timestamp
            end_record.call_id_id = call_id_id

            start_record = StartRecord.objects.get(call_id=call_id_id)
            end_record.cost = calculate_call_cost(
                start_record.timestamp, end_record.timestamp
            )

            end_record.save()

            return end_record


class StartRecordSerializer(serializers.HyperlinkedModelSerializer):
    ''' Represents the serializer for the call start record '''

    id = serializers.IntegerField()
    timestamp = serializers.DateTimeField()
    call_id = serializers.IntegerField()
    source = serializers.CharField()
    destination = serializers.CharField()

    class Meta:
        model = StartRecord
        fields = ('id', 'timestamp', 'call_id', 'source', 'destination')

    def validate(self, data):
        ''' Validate if source and destination are numbers, check
        their length (must be 10 or 11 digits), and also if they are
        two different phone numbers.
        '''

        if data['source'].isdigit() is False:
            raise serializers.ValidationError("Source must have only numbers")
        elif len(data['source']) != 10 and len(data['source']) != 11:
            raise serializers. \
                ValidationError("Source must have 10 or 11 digits")

        if data['destination'].isdigit() is False:
            raise serializers. \
                ValidationError("Destination must have only numbers")
        elif len(data['destination']) != 10 and len(data['destination']) != 11:
            raise serializers. \
                ValidationError("Destination must have 10 or 11 digits")

        if data['source'] == data['destination']:
            raise serializers.ValidationError(
                "Source and destination must have different values")

        return data

    def create(self, validated_data):
        start_record = StartRecord()
        start_record.id = validated_data['id']
        start_record.timestamp = validated_data['timestamp']. \
            replace(tzinfo=timezone.utc)
        start_record.call_id = validated_data['call_id']
        start_record.source = validated_data['source']
        start_record.destination = validated_data['destination']
        start_record.save()
        return start_record


class EndRecordSerializer(serializers.HyperlinkedModelSerializer):
    ''' Represents the serializer for the call end record '''

    id = serializers.IntegerField()
    timestamp = serializers.DateTimeField()
    call_id_id = serializers.IntegerField()

    class Meta:
        model = EndRecord
        fields = ('id', 'timestamp', 'call_id_id')

    def validate(self, data):
        ''' Validate if the start record exist before saving the end
        record. It also checks if the end record's timestamp is later
        than the start record's timestamp
        '''

        start_record = StartRecord.objects.get(call_id=data['call_id_id'])
        end_timestamp = data['timestamp'].replace(tzinfo=timezone.utc)
        if start_record is None:
            raise serializers. \
                ValidationError("Please insert the call start before the end")
        elif start_record.timestamp >= end_timestamp:
            raise serializers.ValidationError(
                "The call end timestamp must be"
                "greater than call start timestamp"
            )

        return data

    def create(self, validated_data):
        id = validated_data['id']
        timestamp = validated_data['timestamp']
        call_id_id = validated_data['call_id_id']
        end_record = EndRecord()
        end_record.id = id
        end_record.timestamp = timestamp
        end_record.call_id_id = call_id_id

        start_record = StartRecord.objects.get(call_id=call_id_id)
        end_record.cost = calculate_call_cost(
            start_record.timestamp, end_record.timestamp
        )

        end_record.save()

        return end_record

    def update(self, end_record, validated_data):

        end_record.id = validated_data['id']
        end_record.timestamp = validated_data['timestamp']
        end_record.call_id_id = validated_data['call_id_id']

        start_record = StartRecord.objects.get(call_id=end_record.call_id_id)

        end_record.cost = calculate_call_cost(
            start_record.timestamp, end_record.timestamp
        )

        end_record.save()

        return validated_data


class PhoneBillSerializer(serializers.Serializer):
    ''' Represents the serializer that returns the detailed bill '''

    destination = serializers.CharField(max_length=100)
    start_date = serializers.CharField(max_length=100)
    start_time = serializers.CharField(max_length=100)
    duration = serializers.CharField(max_length=100)
    price = serializers.CharField(max_length=100)

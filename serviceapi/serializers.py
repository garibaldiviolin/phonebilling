# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils import timezone
from rest_framework import serializers

from serviceapi.models import StartRecord, EndRecord
from serviceapi.utils import *
from phonebilling.settings import TIMESTAMP_FORMAT


class CallRecordSerializer(serializers.Serializer):
    """ Represents the serializer for the start and end record.
    The type field value indicates if it is a start or end record.
    """

    id = serializers.IntegerField()
    timestamp = serializers.DateTimeField(
        format=TIMESTAMP_FORMAT, input_formats=(TIMESTAMP_FORMAT,)
    )
    call_id = serializers.IntegerField()
    type = serializers.IntegerField()
    source = serializers.CharField(required=False)  # start record (only)
    destination = serializers.CharField(required=False)  # start record (only)

    # removes the need for the source and destination fields
    def get_validation_exclusions(self):
        exclusions = super(FavoriteListSerializer, self). \
            get_validation_exclusions()
        return exclusions + ['source'] + ['destination']

    def validate(self, data):

        if 'id' not in data:
            raise serializers.ValidationError({
                'id': 'id field is required'
            })

        if 'type' not in data:
            raise serializers.ValidationError({
                'type': 'type field is required'
            })

        # First, check if type is START (1) or END (2)
        if data['type'] != RecordType.START.value and \
                data['type'] != RecordType.END.value:
            raise serializers.ValidationError({'type': 'Type must be 1 or 2'})

        # if the request is a partial update, then the record must exist
        if self.partial is True:
            if data['type'] == RecordType.START.value:
                queryset_start_record = StartRecord.objects. \
                    filter(id=data['id'])
                if len(queryset_start_record) < 1:
                    raise serializers.ValidationError({
                        'start_record': 'Start record does not exist'
                    })

                record = dict()

                record['id'] = data['id']
                record['timestamp'] = data.get(
                    'timestamp', queryset_start_record[0].timestamp
                )
                record['call_id'] = data.get(
                    'call_id', queryset_start_record[0].call_id
                )
                record['type'] = data['type']
                record['source'] = data.get(
                    'source', queryset_start_record[0].source
                )
                record['destination'] = data.get(
                    'destination', queryset_start_record[0].destination
                )
            else:  # end record
                queryset_end_record = EndRecord.objects. \
                    filter(id=data['id'])
                if len(queryset_end_record) < 1:
                    raise serializers.ValidationError({
                        'end_record': 'EndStart record does not exist'
                    })

                record = dict()

                record['id'] = data['id']
                record['timestamp'] = data.get(
                    'timestamp', queryset_end_record[0].timestamp
                )
                record['call_id'] = data.get(
                    'call_id', queryset_end_record[0].start_id
                )
                record['type'] = data['type']

        else:  # create (POST) or complete update (PUT)
            record = dict()

            record['id'] = data['id']
            record['timestamp'] = data['timestamp']
            record['call_id'] = data['call_id']
            record['type'] = data['type']

            if record['type'] == RecordType.START.value:
                if 'source' not in data:
                    raise serializers.ValidationError({
                        'source': 'Start record must have a source field'
                    })
                if 'destination' not in data:
                    raise serializers.ValidationError({
                        'destination':
                        'Start record must have a destination field'
                    })

                record['source'] = data['source']
                record['destination'] = data['destination']

        # check if exist a record with the same call_id and type but different
        # id
        if record['type'] == RecordType.START.value:
            queryset_start_record = StartRecord.objects \
                .exclude(id=record['id']) \
                .filter(call_id=record['call_id'])
            if len(queryset_start_record) > 0:
                raise serializers.ValidationError({
                    'call_id':
                    'There is already a start record with this call_id'
                })
        else:  # end record
            queryset_end_record = EndRecord.objects \
                .exclude(id=record['id']) \
                .filter(start_id=record['call_id'])
            if len(queryset_end_record) > 0:
                raise serializers.ValidationError({
                    'call_id':
                    'There is already a end record with this call_id'
                })

        # StartRecord fields validation
        if record['type'] == RecordType.START.value:

            # source and destination fields must exist for StartRecord
            # Both of then should have 10 or 11 digits (the first two
            # digits are the area code, and the other ones are the phone
            # number), and they must have different values
            if record['source'].isdigit() is False:
                raise serializers.ValidationError({
                    'source': 'Source must have only numbers'
                })
            elif 'source' in record and len(record['source']) != 10 \
                    and len(record['source']) != 11:
                raise serializers.ValidationError({
                    'source': 'Source must have 10 or 11 digits'
                })

            if record['destination'].isdigit() is False:
                raise serializers.ValidationError({
                    'destination': 'Destination must have only numbers'
                })
            elif len(record['destination']) != 10 \
                    and len(record['destination']) != 11:
                raise serializers.ValidationError({
                    'destination': 'Destination must have 10 or 11 digits'
                })

            if record['source'] == record['destination']:
                raise serializers.ValidationError({
                    'source':
                    'Source and destination must have different values'
                })

            queryset_end_record = EndRecord.objects.filter(
                start_id=record['call_id']
            )
            start_timestamp = record['timestamp'].replace(tzinfo=timezone.utc)
            if len(queryset_end_record) > 0 and \
                    start_timestamp >= queryset_end_record[0].timestamp:
                raise serializers.ValidationError({
                    'timestamp': 'The call start timestamp must be'
                    ' earlier than call end timestamp'
                })

        else:  # EndRecord fields validation

            # StartRecord with the call_id informed must exist
            # before saving EndRecord
            queryset = StartRecord.objects.filter(call_id=record['call_id'])

            if len(queryset) < 1:
                raise serializers.ValidationError({
                    'start': 'Please send the call record start before the end'
                })

            start_record = queryset[0]

            # replace the default timezone (it is not needed)
            end_timestamp = record['timestamp'].replace(tzinfo=timezone.utc)

            if start_record.timestamp >= end_timestamp:
                raise serializers.ValidationError({
                    'timestamp': 'The call end timestamp must be'
                    ' greater than call start timestamp'
                })

        return data

    def create(self, validated_data):

        # if the type is START, then save a start record
        # otherwise, it is a end record
        if validated_data['type'] == RecordType.START.value:

            # Validate if object already exists
            queryset_record = StartRecord.objects.filter(
                id=validated_data['id']
            )
            if len(queryset_record) > 0:
                start_record = queryset_record[0]
            else:
                start_record = StartRecord()

            start_record.id = validated_data.get('id', start_record.id)
            start_record.timestamp = validated_data. \
                get('timestamp', start_record.timestamp). \
                replace(tzinfo=timezone.utc)
            start_record.call_id = validated_data.get(
                'call_id', start_record.call_id
            )
            start_record.source = validated_data.get(
                'source', start_record.source
            )
            start_record.destination = validated_data.get(
                'destination', start_record.destination
            )
            start_record.save()

            return start_record

        else:  # RecordType.END

            # Validate if object already exists
            queryset_record = EndRecord.objects.filter(
                id=validated_data['id']
            )
            if len(queryset_record) > 0:
                end_record = queryset_record[0]
            else:
                end_record = EndRecord()

            end_record.id = validated_data.get('id', end_record.id)
            end_record.timestamp = validated_data. \
                get('timestamp', end_record.timestamp). \
                replace(tzinfo=timezone.utc)
            end_record.start_id = validated_data.get(
                'call_id', end_record.start_id
            )

            start_record = StartRecord.objects.filter(
                call_id=end_record.start_id
            )
            end_record.start = start_record[0]

            end_record.cost = calculate_call_cost(
                start_record[0].timestamp, end_record.timestamp
            )

            end_record.save()

            return end_record


class PhoneBillSerializer(serializers.Serializer):
    """ Represents the serializer that returns the detailed bill """

    destination = serializers.CharField(max_length=100)
    start_date = serializers.CharField(max_length=100)
    start_time = serializers.CharField(max_length=100)
    duration = serializers.CharField(max_length=100)
    price = serializers.CharField(max_length=100)

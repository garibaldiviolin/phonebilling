from django.contrib.auth.models import User, Group
from rest_framework import serializers
from serviceapi.models import StartRecord, EndRecord
from datetime import datetime
from django.utils import timezone
from rest_framework.response import Response
import pdb

class DateTimeTzAwareField(serializers.DateTimeField):

    def to_native(self, value):
        value = timezone.localtime(value)
        return super(DateTimeTzAwareField, self).to_native(value)

class StartRecordSerializer(serializers.HyperlinkedModelSerializer):

    #timestamp = DateTimeTzAwareField()
    #timestamp = serializers.DateTimeField(format='iso-8601')
    timestamp = serializers.DateTimeField()

    class Meta:
        model = StartRecord
        fields = ('id','timestamp','call_id', 'source', 'destination')

    def validate(self, data):
        """
        Check that the start is before the stop.
        """
        #pdb.set_trace()
        if data['source'].isdigit() == False:
            raise serializers.ValidationError("Source must have only numbers")
        elif len(data['source']) != 11 and len(data['source']) != 12:
            raise serializers.ValidationError("Source must have 10 or 11 digits")
        return data


class EndRecordSerializer(serializers.HyperlinkedModelSerializer):

    #timestamp = DateTimeTzAwareField()
    id = serializers.IntegerField()
    call_id_id = serializers.IntegerField()
    timestamp = serializers.DateTimeField()

    class Meta:
        model = EndRecord
        fields = ('id','timestamp','call_id_id')

    def validate(self, data):

        """
        Check that the start is before the stop.
        """

        record_exist_1 = EndRecord.objects.filter(id=data['id'])
        record_exist_2 = EndRecord.objects.filter(call_id_id=data['call_id_id'])
        if len(record_exist_1) > 0:
            raise serializers.ValidationError("The id already exists")
        elif len(record_exist_2) > 0:
            raise serializers.ValidationError("The call_id already exists")

        start_record = StartRecord.objects.get(call_id=data['call_id_id'])
        end_timestamp = data['timestamp'].replace(tzinfo=timezone.utc)
        pdb.set_trace()
        if start_record is None:
            raise serializers.ValidationError("Please insert the call start before the end")
        elif start_record.timestamp >= end_timestamp:
            raise serializers.ValidationError("The call end timestamp must be greater than call start timestamp")

        return data

    '''def create(self, validated_data):
        timestamp = validated_data['timestamp']
        call_id_id = validated_data['call_id_id']
        end_record = EndRecord()
        end_record.timestamp = timestamp
        end_record.call_id_id = call_id_id
        end_record.save()
        return end_record'''

class PhoneBillSerializer(serializers.Serializer):

    #call_id_id = serializers.IntegerField()

    class Meta:
        model = EndRecord
        fields = ('call_id_id',)

    def create(self, validated_data):

        #pdb.set_trace()
        #call_id_id = validated_data['call_id_id']
        #end_record = EndRecord.objects.create(call_id_id=24, **validated_data)
        end_record = EndRecord.objects.all()
        serializer = EndRecordSerializer(end_record, many=True)
        pdb.set_trace()
        return Response(serializer.data)

    def list(self):

        #pdb.set_trace()

        serializer_class = PhoneBillSerializer
        #http_method_names = ['post']

        source = self.request.query_params.get('source', None)
        pdb.set_trace()
        if source is not None:
            #queryset = Answer.objects.filter(question_id=1).select_related()
            comments = EndRecord.objects.filter(call_id=source).select_related('call_id')
        else:
            comments = EndRecord.objects.all().select_related('call_id')

        return comments

class TwoPhoneBillSerializer(serializers.Serializer):

    destination = serializers.CharField(max_length=100)
    start_date = serializers.CharField(max_length=100)
    start_time = serializers.CharField(max_length=100)
    duration = serializers.CharField(max_length=100)
    price = serializers.CharField(max_length=100)
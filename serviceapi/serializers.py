from django.contrib.auth.models import User, Group
from rest_framework import serializers
from serviceapi.models import StartRecord, EndRecord
from datetime import datetime
from django.utils import timezone
 
class DateTimeTzAwareField(serializers.DateTimeField):

    def to_native(self, value):
        value = timezone.localtime(value)
        return super(DateTimeTzAwareField, self).to_native(value)

class StartRecordSerializer(serializers.HyperlinkedModelSerializer):

    #timestamp = DateTimeTzAwareField()
    #timestamp = serializers.DateTimeField(format='iso-8601')

    class Meta:
        model = StartRecord
        fields = ('call_id', 'source', 'destination')


class EndRecordSerializer(serializers.HyperlinkedModelSerializer):

    #timestamp = DateTimeTzAwareField()

    class Meta:
        model = EndRecord
        fields = ('call_id',)

class PhoneBillSerializer(serializers.HyperlinkedModelSerializer):

    call_id = serializer.BigIntegerField(unique=True)
    timestamp_start = serializer.DateTimeField(auto_now_add=True)
    timestamp_end = serializer.DateTimeField(auto_now_add=True)
    source = serializer.CharField(max_length=11)
    destination = serializer.CharField(max_length=11)

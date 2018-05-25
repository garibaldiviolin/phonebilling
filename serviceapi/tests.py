# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.core import serializers
from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from rest_framework import status

from serviceapi.models import StartRecord, EndRecord
from serviceapi.serializers import StartRecordSerializer,EndRecordSerializer
from serviceapi.views import StartRecordViewSet

client = Client()

SOURCE_NUMBER = "99988526423"
DESTINATION_NUMBER = "9993468278"

list_start = list()
list_end = list()

class GetAllStartRecordsTest(TestCase):
    """ Test module for GET all puppies API """

    '''StartRecord.objects.create(
        id=1, timestamp=datetime.datetime(2016, 2, 29, 12, 0, 0, 0, timezone.utc), call_id=70, source=SOURCE_NUMBER, destination=DESTINATION_NUMBER)
    StartRecord.objects.create(
        id=2, timestamp=datetime.datetime(2017, 12, 12, 15, 7, 13, 0, timezone.utc), call_id=71, source=SOURCE_NUMBER, destination=DESTINATION_NUMBER)'''

    def setUp(self):

        list_start.append(StartRecord(
            id=1, timestamp=datetime.datetime(2016, 2, 29, 12, 0, 0, 0, timezone.utc), call_id=70, source=SOURCE_NUMBER, destination=DESTINATION_NUMBER))
        list_start.append(StartRecord(
            id=2, timestamp=datetime.datetime(2017, 12, 12, 15, 7, 13, 0, timezone.utc), call_id=71, source=SOURCE_NUMBER, destination=DESTINATION_NUMBER))
        list_start.append(StartRecord(
            id=3, timestamp=datetime.datetime(2017, 12, 12, 22, 57, 56, 0, timezone.utc), call_id=72, source=SOURCE_NUMBER, destination=DESTINATION_NUMBER))
        list_start.append(StartRecord(
            id=4, timestamp=datetime.datetime(2017, 12, 12, 21, 57, 13, 0, timezone.utc), call_id=73, source=SOURCE_NUMBER, destination=DESTINATION_NUMBER))
        list_start.append(StartRecord(
            id=5, timestamp=datetime.datetime(2017, 12, 12, 4, 57, 13, 0, timezone.utc), call_id=74, source=SOURCE_NUMBER, destination=DESTINATION_NUMBER))
        list_start.append(StartRecord(
            id=6, timestamp=datetime.datetime(2017, 12, 12, 21, 57, 13, 0, timezone.utc), call_id=75, source=SOURCE_NUMBER, destination=DESTINATION_NUMBER))
        list_start.append(StartRecord(
            id=7, timestamp=datetime.datetime(2017, 12, 12, 15, 7, 58, 0, timezone.utc), call_id=76, source=SOURCE_NUMBER, destination=DESTINATION_NUMBER))
        list_start.append(StartRecord(
            id=8, timestamp=datetime.datetime(2018, 2, 28, 21, 57, 13, 0, timezone.utc), call_id=77, source=SOURCE_NUMBER, destination=DESTINATION_NUMBER))

        list_end.append(EndRecord(
            id=1, timestamp=datetime.datetime(2016, 2, 29, 14, 0, 0, 0, timezone.utc), call_id_id=70))
        list_end.append(EndRecord(
            id=2, timestamp=datetime.datetime(2017, 12, 12, 15, 14, 56, 0, timezone.utc), call_id_id=71))
        list_end.append(EndRecord(
            id=3, timestamp=datetime.datetime(2017, 12, 12, 22, 50, 56, 0, timezone.utc), call_id_id=72))
        list_end.append(EndRecord(
            id=4, timestamp=datetime.datetime(2017, 12, 12, 22, 10, 56, 0, timezone.utc), call_id_id=73))
        list_end.append(EndRecord(
            id=5, timestamp=datetime.datetime(2017, 12, 12, 6, 10, 56, 0, timezone.utc), call_id_id=74))
        list_end.append(EndRecord(
            id=6, timestamp=datetime.datetime(2017, 12, 13, 22, 10, 56, 0, timezone.utc), call_id_id=75))
        list_end.append(EndRecord(
            id=7, timestamp=datetime.datetime(2017, 12, 12, 15, 12, 56, 0, timezone.utc), call_id_id=76))
        list_end.append(EndRecord(
            id=8, timestamp=datetime.datetime(2018, 3, 1, 22, 10, 56, 0, timezone.utc), call_id_id=77))

        list_start.reverse()
        list_end.reverse()

        for start_record in list_start:
            start_record.save()

        for end_record in list_end:
            end_record.save()

    def test_get_all_start_records(self):
        # get API response
        response = client.get("/startrecord/")

        # get data from db
        start_record = StartRecord.objects.all().order_by('-call_id')

        serializer_list = StartRecordSerializer(list_start, many=True)
        serializer_db = StartRecordSerializer(start_record, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data, serializer_list.data)
        self.assertEquals(response.data, serializer_db.data)

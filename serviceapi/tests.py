# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from .models import StartRecord, EndRecord
import datetime
from django.utils import timezone
from .serializers import StartRecordSerializer
from .views import StartRecordViewSet
import pdb

# initialize the APIClient app
client = Client()

SOURCE_NUMBER = 99988526423
DESTINATION_NUMBER = 9993468278

class GetAllStartRecordsTest(TestCase):
    """ Test module for GET all puppies API """

    start_record = list()

    StartRecord.objects.create(
        id=1, timestamp=datetime.datetime(2016, 2, 29, 12, 0, 0, 0, timezone.utc), call_id=70, source=SOURCE_NUMBER, destination=DESTINATION_NUMBER)
    StartRecord.objects.create(
        id=2, timestamp=datetime.datetime(2017, 12, 12, 15, 7, 13, 0, timezone.utc), call_id=71, source=SOURCE_NUMBER, destination=DESTINATION_NUMBER)

    def setUp(self):
        '''StartRecord.objects.create(
            id=1, timestamp=datetime.datetime(2016, 2, 29, 12, 0, 0, 0, timezone.utc), call_id=70, source=SOURCE_NUMBER, destination=DESTINATION_NUMBER)
        StartRecord.objects.create(
            id=2, timestamp=datetime.datetime(2017, 12, 12, 15, 7, 13, 0, timezone.utc), call_id=71, source=SOURCE_NUMBER, destination=DESTINATION_NUMBER)
        StartRecord.objects.create(
            id=3, timestamp=datetime.datetime(2017, 12, 12, 22, 57, 56, 0, timezone.utc), call_id=72, source=SOURCE_NUMBER, destination=DESTINATION_NUMBER)
        StartRecord.objects.create(
            id=4, timestamp=datetime.datetime(2017, 12, 12, 21, 57, 13, 0, timezone.utc), call_id=73, source=SOURCE_NUMBER, destination=DESTINATION_NUMBER)
        StartRecord.objects.create(
            id=5, timestamp=datetime.datetime(2017, 12, 12, 4, 57, 13, 0, timezone.utc), call_id=74, source=SOURCE_NUMBER, destination=DESTINATION_NUMBER)
        StartRecord.objects.create(
            id=6, timestamp=datetime.datetime(2017, 12, 12, 21, 57, 13, 0, timezone.utc), call_id=75, source=SOURCE_NUMBER, destination=DESTINATION_NUMBER)
        StartRecord.objects.create(
            id=7, timestamp=datetime.datetime(2017, 12, 12, 15, 7, 58, 0, timezone.utc), call_id=76, source=SOURCE_NUMBER, destination=DESTINATION_NUMBER)
        StartRecord.objects.create(
            id=8, timestamp=datetime.datetime(2018, 2, 28, 21, 57, 13, 0, timezone.utc), call_id=77, source=SOURCE_NUMBER, destination=DESTINATION_NUMBER)

        EndRecord.objects.create(
            id=1, timestamp=datetime.datetime(2016, 2, 29, 14, 0, 0, 0, timezone.utc), call_id_id=70)
        EndRecord.objects.create(
            id=2, timestamp=datetime.datetime(2017, 12, 12, 15, 14, 56, 0, timezone.utc), call_id_id=71)
        EndRecord.objects.create(
            id=3, timestamp=datetime.datetime(2017, 12, 12, 22, 50, 56, 0, timezone.utc), call_id_id=72)
        EndRecord.objects.create(
            id=4, timestamp=datetime.datetime(2017, 12, 12, 22, 10, 56, 0, timezone.utc), call_id_id=73)
        EndRecord.objects.create(
            id=5, timestamp=datetime.datetime(2017, 12, 12, 06, 10, 56, 0, timezone.utc), call_id_id=74)
        EndRecord.objects.create(
            id=6, timestamp=datetime.datetime(2017, 12, 13, 22, 10, 56, 0, timezone.utc), call_id_id=75)
        EndRecord.objects.create(
            id=7, timestamp=datetime.datetime(2017, 12, 12, 15, 12, 56, 0, timezone.utc), call_id_id=76)
        EndRecord.objects.create(
            id=8, timestamp=datetime.datetime(2018, 3, 1, 22, 10, 56, 0, timezone.utc), call_id_id=77)'''



    def test_get_all_records(self):
        # get API response
        response = client.get("/startrecord/")
        #pdb.set_trace()

        # get data from db
        start_record = StartRecord.objects.all()
        serializer = StartRecordSerializer(StartRecord, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

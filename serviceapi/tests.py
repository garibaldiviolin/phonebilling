# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
import json
import pdb

from django.core import serializers
from django.test import TestCase, Client
from django.utils import timezone
from rest_framework import status

from serviceapi.models import StartRecord, EndRecord
from serviceapi.serializers import StartRecordSerializer, \
    EndRecordSerializer, PhoneBillSerializer
from serviceapi.utils import RecordType

client = Client()

SOURCE_NUMBER = "99988526423"
DESTINATION_NUMBER = "9993468278"

START_TIME_1 = datetime.datetime(2016, 2, 29, 12, 0, 0, 0, timezone.utc)
START_TIME_2 = datetime.datetime(2017, 12, 12, 15, 7, 13, 0, timezone.utc)
START_TIME_3 = datetime.datetime(2017, 12, 12, 22, 47, 56, 0, timezone.utc)
START_TIME_4 = datetime.datetime(2017, 12, 12, 21, 57, 13, 0, timezone.utc)
START_TIME_5 = datetime.datetime(2017, 12, 12, 4, 57, 13, 0, timezone.utc)
START_TIME_6 = datetime.datetime(2017, 12, 12, 21, 57, 13, 0, timezone.utc)
START_TIME_7 = datetime.datetime(2017, 12, 12, 15, 7, 58, 0, timezone.utc)
START_TIME_8 = datetime.datetime(2018, 2, 28, 21, 57, 13, 0, timezone.utc)

END_TIME_1 = datetime.datetime(2016, 2, 29, 14, 0, 0, 0, timezone.utc)
END_TIME_2 = datetime.datetime(2017, 12, 12, 15, 14, 56, 0, timezone.utc)
END_TIME_3 = datetime.datetime(2017, 12, 12, 22, 50, 56, 0, timezone.utc)
END_TIME_4 = datetime.datetime(2017, 12, 12, 22, 10, 56, 0, timezone.utc)
END_TIME_5 = datetime.datetime(2017, 12, 12, 6, 10, 56, 0, timezone.utc)
END_TIME_6 = datetime.datetime(2017, 12, 13, 22, 10, 56, 0, timezone.utc)
END_TIME_7 = datetime.datetime(2017, 12, 12, 15, 12, 56, 0, timezone.utc)
END_TIME_8 = datetime.datetime(2018, 3, 1, 22, 10, 56, 0, timezone.utc)
END_TIME_9 = datetime.datetime(2016, 3, 1, 12, 0, 1, 0, timezone.utc)
END_TIME_10 = datetime.datetime(2016, 2, 29, 12, 0, 0, 1, timezone.utc)

list_start = list()
list_end = list()

start_single_record = StartRecord(
    id=1, timestamp=START_TIME_1,
    call_id=70, source=SOURCE_NUMBER, destination=DESTINATION_NUMBER
)

end_single_record = EndRecord(
    id=1, timestamp=END_TIME_1,
    call_id_id=70, cost=0
)

# ************************************
# ************************************
# Start Record Tests
# ************************************
# ************************************


class PhoneBill:

    def __init__(self, destination, start_date, start_time, duration, price):
        self.destination = destination
        self.start_date = start_date
        self.start_time = start_time
        self.duration = duration
        self.price = price


class GetPhoneBillTest(TestCase):
    """ Test module for GET single end record """

    def setUp(self):

        # creates the list with the call end records
        self.list_start = list()

        self.list_start.append({
            'id': 2, 'timestamp': START_TIME_2, 'call_id': 71,
            'type': RecordType.START.value, 'source': SOURCE_NUMBER,
            'destination': DESTINATION_NUMBER
        })

        self.list_start.append({
            'id': 3, 'timestamp': START_TIME_3, 'call_id': 72,
            'type': RecordType.START.value, 'source': SOURCE_NUMBER,
            'destination': DESTINATION_NUMBER
        })

        self.list_start.append({
            'id': 4, 'timestamp': START_TIME_4, 'call_id': 73,
            'type': RecordType.START.value, 'source': SOURCE_NUMBER,
            'destination': DESTINATION_NUMBER
        })

        self.list_start.append({
            'id': 5, 'timestamp': START_TIME_5, 'call_id': 74,
            'type': RecordType.START.value, 'source': SOURCE_NUMBER,
            'destination': DESTINATION_NUMBER
        })

        self.list_start.append({
            'id': 6, 'timestamp': START_TIME_6, 'call_id': 75,
            'type': RecordType.START.value, 'source': SOURCE_NUMBER,
            'destination': DESTINATION_NUMBER
        })

        self.list_start.append({
            'id': 7, 'timestamp': START_TIME_7, 'call_id': 76,
            'type': RecordType.START.value, 'source': SOURCE_NUMBER,
            'destination': DESTINATION_NUMBER
        })

        # creates the list with the call end records
        self.list_end = list()

        self.list_end.append({
            'id': 2, 'timestamp': END_TIME_2, 'call_id': 71,
            'type': RecordType.END.value, 'cost': 0.99
        })

        self.list_end.append({
            'id': 3, 'timestamp': END_TIME_3, 'call_id': 72,
            'type': RecordType.END.value, 'cost': 0.36
        })

        self.list_end.append({
            'id': 4, 'timestamp': END_TIME_4, 'call_id': 73,
            'type': RecordType.END.value, 'cost': 0.54
        })

        self.list_end.append({
            'id': 5, 'timestamp': END_TIME_5, 'call_id': 74,
            'type': RecordType.END.value, 'cost': 1.26
        })

        self.list_end.append({
            'id': 6, 'timestamp': END_TIME_6, 'call_id': 75,
            'type': RecordType.END.value, 'cost': 86.94
        })

        self.list_end.append({
            'id': 7, 'timestamp': END_TIME_7, 'call_id': 76,
            'type': RecordType.END.value, 'cost': 0.72
        })

        # creates the bill list to match with the response that will be
        # returned later
        self.bill_list = list()
        for i in range(len(self.list_end)):

            destination = self.list_start[i]['destination']

            record_start_time = self.list_start[i]['timestamp']
            record_end_time = self.list_end[i]['timestamp']
            delta = record_end_time - record_start_time
            h = delta.seconds / 3600  # hours
            m = delta.seconds / 60  # minutes
            s = delta.seconds % 60  # seconds
            duration = '%dh%02dm%02ds' % (h, m, s)

            formatted_price = ('R$ %0.2f' % self.list_end[
                               i]['cost']).replace('.', ',')

            self.bill_list.append(PhoneBill(
                destination=destination,
                start_date=record_start_time.strftime('%d/%m/%Y'),
                start_time=record_start_time.strftime('%H:%M:%S'),
                duration=duration,
                price=formatted_price,
            ))

        for item in self.list_start:
            item['timestamp'] = str(item['timestamp'])

        for item in self.list_end:
            item['timestamp'] = str(item['timestamp'])

    def test_get_phone_bill(self):
        ''' This test sends (POST) a list of start and end phone calls,
        requests the phone bill, and then matches the response with the
        expected list
        ''' 

        # Post all start records
        for start_record in self.list_start:
            response = client.post(
                '/callrecord/',
                data=json.dumps(start_record),
                content_type='application/json'
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Then post all end records
        for end_record in self.list_end:
            response = client.post(
                '/callrecord/',
                data=json.dumps(end_record),
                content_type='application/json'
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Now get the detailed phone bill and match the response
        response = client.get("/phonebill/?source=" +
                              SOURCE_NUMBER + "&period=12/2017")

        serializer_list = PhoneBillSerializer(self.bill_list, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data, serializer_list.data)

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
import json
import pdb

from django.core import serializers
from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from rest_framework import status, serializers

from serviceapi.models import StartRecord, EndRecord
from serviceapi.serializers import StartRecordSerializer,EndRecordSerializer, \
    PhoneBillSerializer
from serviceapi.views import StartRecordViewSet

client = Client()

SOURCE_NUMBER = "99988526423"
DESTINATION_NUMBER = "9993468278"

list_start = list()
list_end = list()

start_single_record = StartRecord(
    id=1, timestamp=datetime.datetime(2016, 2, 29, 12, 0, 0, 0, timezone.utc), call_id=70, source=SOURCE_NUMBER, destination=DESTINATION_NUMBER)

end_single_record = EndRecord(
    id=1, timestamp=datetime.datetime(2016, 2, 29, 14, 0, 0, 0, timezone.utc), call_id_id=70, cost=0)

# ************************************
# ************************************
# Start Record Tests
# ************************************
# ************************************

class PhoneBill:

    destination = serializers.CharField(max_length=100)
    start_date = serializers.CharField(max_length=100)
    start_time = serializers.CharField(max_length=100)
    duration = serializers.CharField(max_length=100)
    price = serializers.CharField(max_length=100)

    def __init__(self, destination, start_date, start_time, duration, price):
        self.destination = destination
        self.start_date = start_date
        self.start_time = start_time
        self.duration = duration
        self.price = price

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
            id=3, timestamp=datetime.datetime(2017, 12, 12, 22, 47, 56, 0, timezone.utc), call_id=72, source=SOURCE_NUMBER, destination=DESTINATION_NUMBER))
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

        list_start.reverse()

        for start_record in list_start:
            start_record.save()

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


class GetSingleValidStartRecordTest(TestCase):
    """ Test module for GET single start record """

    def setUp(self):

        list_start[:] = []

        start_single_record.save()

    def test_get_valid_single_start_record(self):
        # get API response

        response = client.get("/startrecord/" + str(start_single_record.id) + "/")

        # get data from db
        start_record_db = StartRecord.objects.get(call_id=start_single_record.call_id)

        serializer_list = StartRecordSerializer(start_single_record)
        serializer_db = StartRecordSerializer(start_record_db)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data, serializer_list.data)
        self.assertEquals(response.data, serializer_db.data)


class GetSingleInvalidStartRecordTest(TestCase):

    def setUp(self):

        list_start[:] = []

        start_single_record.save()

    def test_get_invalid_single_start_record(self):
        # get API response

        response = client.get("/startrecord/9999/")

        # get data from db
        start_record_db = StartRecord.objects.get(call_id=start_single_record.call_id)

        serializer_list = StartRecordSerializer(start_single_record)
        serializer_db = StartRecordSerializer(start_record_db)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CreateNewStartRecordTest(TestCase):
    """ Test module for inserting a new puppy """

    def setUp(self):
        self.valid_startrecord = {
            'id': 10,
            'timestamp': str(datetime.datetime(2016, 2, 29, 12, 0, 0, 0, timezone.utc)),
            'call_id': 5,
            'source': '11912124425',
            'destination': '11991251242'
        }

        self.start_record_list = list()

        self.start_record_list.append({
            'id': 'A',
            'timestamp': str(datetime.datetime(2016, 2, 29, 12, 0, 0, 0, timezone.utc)),
            'call_id': 5,
            'source': '11912124425',
            'destination': '11991251242'
        })

        self.start_record_list.append({
            'id': '',
            'timestamp': str(datetime.datetime(2016, 2, 29, 12, 0, 0, 0, timezone.utc)),
            'call_id': 5,
            'source': '11912124425',
            'destination': '11991251242'
        })

        self.start_record_list.append({
            'id': 2,
            'timestamp': '9999-99-99T99:99:99Z',
            'call_id': 5,
            'source': '11912124425',
            'destination': '11991251242'
        })

        self.start_record_list.append({
            'id': 2,
            'timestamp': '',
            'call_id': 5,
            'source': '11912124425',
            'destination': '11991251242'
        })

        self.start_record_list.append({
            'id': 3,
            'timestamp': str(datetime.datetime(2016, 2, 29, 12, 0, 0, 0, timezone.utc)),
            'call_id': 'B',
            'source': '11912124425',
            'destination': '11991251242'
        })

        self.start_record_list.append({
            'id': 3,
            'timestamp': str(datetime.datetime(2016, 2, 29, 12, 0, 0, 0, timezone.utc)),
            'call_id': '',
            'source': '11912124425',
            'destination': '11991251242'
        })

        self.start_record_list.append({
            'id': 4,
            'timestamp': str(datetime.datetime(2016, 2, 29, 12, 0, 0, 0, timezone.utc)),
            'call_id': 5,
            'source': '119121244',
            'destination': '11991251242'
        })

        self.start_record_list.append({
            'id': 4,
            'timestamp': str(datetime.datetime(2016, 2, 29, 12, 0, 0, 0, timezone.utc)),
            'call_id': 5,
            'source': '',
            'destination': '11991251242'
        })

        self.start_record_list.append({
            'id': 5,
            'timestamp': str(datetime.datetime(2016, 2, 29, 12, 0, 0, 0, timezone.utc)),
            'call_id': 5,
            'source': 'A1912124425',
            'destination': '11991251242'
        })

        self.start_record_list.append({
            'id': 5,
            'timestamp': str(datetime.datetime(2016, 2, 29, 12, 0, 0, 0, timezone.utc)),
            'call_id': 5,
            'source': '',
            'destination': '11991251242'
        })

        self.start_record_list.append({
            'id': 6,
            'timestamp': str(datetime.datetime(2016, 2, 29, 12, 0, 0, 0, timezone.utc)),
            'call_id': 5,
            'source': '11912124425',
            'destination': '119912512'
        })

        self.start_record_list.append({
            'id': 7,
            'timestamp': str(datetime.datetime(2016, 2, 29, 12, 0, 0, 0, timezone.utc)),
            'call_id': 5,
            'source': '11912124425',
            'destination': 'B1991251242'
        })

        self.start_record_list.append({
            'id': 7,
            'timestamp': str(datetime.datetime(2016, 2, 29, 12, 0, 0, 0, timezone.utc)),
            'call_id': 5,
            'source': '11912124425',
            'destination': ''
        })

    def test_create_valid_start_record(self):
        response = client.post(
            '/startrecord/',
            data=json.dumps(self.valid_startrecord),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_start_record(self):
        for record in self.start_record_list:
            response = client.post(
                '/startrecord/',
                data=json.dumps(record),
                content_type='application/json'
            )

            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UpdateSingleStartRecordTest(TestCase):
    """ Test module for updating an existing puppy record """

    def setUp(self):
        
        self.list_start = list()
        self.list_start.append(StartRecord(
            id=1, timestamp=datetime.datetime(2016, 2, 29, 12, 0, 0, 0, timezone.utc), call_id=70, source=SOURCE_NUMBER, destination=DESTINATION_NUMBER))
        self.list_start.append(StartRecord(
            id=2, timestamp=datetime.datetime(2017, 12, 12, 15, 7, 13, 0, timezone.utc), call_id=71, source=SOURCE_NUMBER, destination=DESTINATION_NUMBER))

        for self.start_record in self.list_start:
            self.start_record.save()

        self.valid_start_record = {
            'id': 1,
            'timestamp': str(datetime.datetime(2016, 2, 29, 12, 0, 0, 0, timezone.utc)),
            'call_id': 73,
            'source': SOURCE_NUMBER,
            'destination': DESTINATION_NUMBER
        }

        self.invalid_start_record = {
            'id': 2,
            'timestamp': str(datetime.datetime(2016, 2, 29, 12, 0, 0, 0, timezone.utc)),
            'call_id': '',
            'source': SOURCE_NUMBER,
            'destination': DESTINATION_NUMBER
        }

    def test_valid_update_start_record(self):
        response = client.put(
            '/startrecord/' + str(self.valid_start_record['id']) + '/',
            data=json.dumps(self.valid_start_record),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_update_start_record(self):
        response = client.put(
            '/startrecord/' + str(self.invalid_start_record['id']) + '/',
            data=json.dumps(self.invalid_start_record),
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DeleteSingleStartRecordTest(TestCase):
    """ Test module for deleting an existing puppy record """

    def setUp(self):
        self.list_start = list()
        self.list_start.append(StartRecord(
            id=1, timestamp=datetime.datetime(2016, 2, 29, 12, 0, 0, 0, timezone.utc), call_id=70, source=SOURCE_NUMBER, destination=DESTINATION_NUMBER))
        self.list_start.append(StartRecord(
            id=2, timestamp=datetime.datetime(2017, 12, 12, 15, 7, 13, 0, timezone.utc), call_id=71, source=SOURCE_NUMBER, destination=DESTINATION_NUMBER))

        for self.start_record in self.list_start:
            self.start_record.save()

    def test_valid_delete_start_record(self):
        response = client.delete(
            '/startrecord/' + str(self.list_start[0].id) + '/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_delete_start_record(self):
        response = client.delete(
            '/startrecord/9999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


# ************************************
# ************************************
# End Record Tests
# ************************************
# ************************************h

class GetAllEndRecordsTest(TestCase):

    def setUp(self):

        list_end.append(EndRecord(
            id=1, timestamp=datetime.datetime(2016, 2, 29, 14, 0, 0, 0, timezone.utc), call_id_id=70, cost=0))
        list_end.append(EndRecord(
            id=2, timestamp=datetime.datetime(2017, 12, 12, 15, 14, 56, 0, timezone.utc), call_id_id=71, cost=0))
        list_end.append(EndRecord(
            id=3, timestamp=datetime.datetime(2017, 12, 12, 22, 50, 56, 0, timezone.utc), call_id_id=72, cost=0))
        list_end.append(EndRecord(
            id=4, timestamp=datetime.datetime(2017, 12, 12, 22, 10, 56, 0, timezone.utc), call_id_id=73, cost=0))
        list_end.append(EndRecord(
            id=5, timestamp=datetime.datetime(2017, 12, 12, 6, 10, 56, 0, timezone.utc), call_id_id=74, cost=0))
        list_end.append(EndRecord(
            id=6, timestamp=datetime.datetime(2017, 12, 13, 22, 10, 56, 0, timezone.utc), call_id_id=75, cost=0))
        list_end.append(EndRecord(
            id=7, timestamp=datetime.datetime(2017, 12, 12, 15, 12, 56, 0, timezone.utc), call_id_id=76, cost=0))
        list_end.append(EndRecord(
            id=8, timestamp=datetime.datetime(2018, 3, 1, 22, 10, 56, 0, timezone.utc), call_id_id=77, cost=0))

        list_end.reverse()

        for end_record in list_end:
            end_record.save()

    def test_get_all_end_records(self):
        # get API response
        response = client.get("/endrecord/")

        # get data from db
        end_record = EndRecord.objects.all().order_by('-call_id')

        serializer_list = EndRecordSerializer(list_end, many=True)
        serializer_db = EndRecordSerializer(end_record, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data, serializer_list.data)
        self.assertEquals(response.data, serializer_db.data)


class GetSingleValidEndRecordTest(TestCase):
    """ Test module for GET single end record """

    def setUp(self):

        list_end[:] = []

        end_single_record.save()

    def test_get_valid_single_end_record(self):
        # get API response

        response = client.get("/endrecord/" + str(end_single_record.id) + "/")

        # get data from db
        end_record_db = EndRecord.objects.get(call_id_id=end_single_record.call_id_id)

        serializer_list = EndRecordSerializer(end_single_record)
        serializer_db = EndRecordSerializer(end_record_db)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data, serializer_list.data)
        self.assertEquals(response.data, serializer_db.data)


class GetSingleInvalidEndRecordTest(TestCase):

    def setUp(self):

        list_end[:] = []

        end_single_record.save()

    def test_get_invalid_single_end_record(self):
        # get API response

        response = client.get("/endrecord/9999/")

        # get data from db
        end_record_db = EndRecord.objects.get(call_id_id=end_single_record.call_id_id)

        serializer_list = EndRecordSerializer(end_single_record)
        serializer_db = EndRecordSerializer(end_record_db)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CreateNewEndRecordTest(TestCase):
    """ Test module for inserting a new end record """

    def setUp(self):
        StartRecord.objects.create(
            id=10, timestamp=datetime.datetime(2016, 2, 29, 12, 0, 0, 0, timezone.utc), call_id=5, source=SOURCE_NUMBER, destination=DESTINATION_NUMBER)

        self.valid_endrecord = {
            'id': 10,
            'timestamp': str(datetime.datetime(2016, 2, 29, 12, 0, 0, 1, timezone.utc)),
            'call_id_id': 5
        }

        self.end_record_list = list()

        self.end_record_list.append({
            'id': 'A',
            'timestamp': str(datetime.datetime(2016, 2, 29, 12, 0, 0, 0, timezone.utc)),
            'call_id_id': 5
        })

        self.end_record_list.append({
            'id': '',
            'timestamp': str(datetime.datetime(2016, 2, 29, 12, 0, 0, 0, timezone.utc)),
            'call_id_id': 5
        })

        self.end_record_list.append({
            'id': 2,
            'timestamp': '9999-99-99T99:99:99Z',
            'call_id_id': 5
        })

        self.end_record_list.append({
            'id': 2,
            'timestamp': '',
            'call_id_id': 5
        })

        self.end_record_list.append({
            'id': 3,
            'timestamp': str(datetime.datetime(2016, 2, 29, 12, 0, 0, 0, timezone.utc)),
            'call_id_id': 'B'
        })

        self.end_record_list.append({
            'id': 3,
            'timestamp': str(datetime.datetime(2016, 2, 29, 12, 0, 0, 0, timezone.utc)),
            'call_id_id': ''
        })

    def test_create_valid_end_record(self):
        response = client.post(
            '/endrecord/',
            data=json.dumps(self.valid_endrecord),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_end_record(self):
        for record in self.end_record_list:
            response = client.post(
                '/endrecord/',
                data=json.dumps(record),
                content_type='application/json'
            )

            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UpdateSingleEndRecordTest(TestCase):
    """ Test module for updating an existing end record record """

    def setUp(self):

        self.list_start = list()
        self.list_start.append(StartRecord(
            id=1, timestamp=datetime.datetime(2016, 2, 29, 12, 0, 0, 0, timezone.utc), call_id=70, source=SOURCE_NUMBER, destination=DESTINATION_NUMBER))
        self.list_start.append(StartRecord(
            id=2, timestamp=datetime.datetime(2017, 12, 12, 15, 7, 13, 0, timezone.utc), call_id=71, source=SOURCE_NUMBER, destination=DESTINATION_NUMBER))
        
        self.list_end = list()
        self.list_end.append(EndRecord(
            id=1, timestamp=datetime.datetime(2016, 3, 1, 12, 0, 1, 0, timezone.utc), call_id_id=70, cost=0))
        self.list_end.append(EndRecord(
            id=2, timestamp=datetime.datetime(2017, 12, 12, 15, 7, 13, 0, timezone.utc), call_id_id=71, cost=0))

        for self.start_record in self.list_start:
            self.start_record.save()

        for self.end_record in self.list_end:
            self.end_record.save()

        self.valid_end_record = {
            'id': 1,
            'timestamp': str(datetime.datetime(2016, 3, 1, 12, 0, 1, 0, timezone.utc)),
            'call_id_id': 70
        }

        self.invalid_end_record = {
            'id': 2,
            'timestamp': str(datetime.datetime(2016, 2, 29, 12, 0, 0, 0, timezone.utc)),
            'call_id_id': ''
        }

    '''def test_valid_update_end_record(self):
        response = client.put(
            '/endrecord/' + str(self.valid_end_record['id']) + '/',
            data=json.dumps(self.valid_end_record),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)'''

    def test_invalid_update_end_record(self):
        response = client.put(
            '/endrecord/' + str(self.invalid_end_record['id']) + '/',
            data=json.dumps(self.invalid_end_record),
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DeleteSingleEndRecordTest(TestCase):
    """ Test module for deleting an existing end record """

    def setUp(self):
        self.list_end = list()
        self.list_end.append(EndRecord(
            id=1, timestamp=datetime.datetime(2016, 2, 29, 12, 0, 0, 0, timezone.utc), call_id_id=70, cost=0))
        self.list_end.append(EndRecord(
            id=2, timestamp=datetime.datetime(2017, 12, 12, 15, 7, 13, 0, timezone.utc), call_id_id=71, cost=0))

        for self.end_record in self.list_end:
            self.end_record.save()

    def test_valid_delete_end_record(self):
        response = client.delete(
            '/endrecord/' + str(self.list_end[0].id) + '/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_delete_end_record(self):
        response = client.delete(
            '/endrecord/9999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class GetPhoneBillTest(TestCase):
    """ Test module for GET single end record """

    def setUp(self):

        StartRecord.objects.all().delete()
        EndRecord.objects.all().delete()

        list_start = list()
        list_start.append(StartRecord(
            id=2, timestamp=datetime.datetime(2017, 12, 12, 15, 7, 13, 0, timezone.utc), call_id=71, source=SOURCE_NUMBER, destination=DESTINATION_NUMBER))
        list_start.append(StartRecord(
            id=3, timestamp=datetime.datetime(2017, 12, 12, 22, 47, 56, 0, timezone.utc), call_id=72, source=SOURCE_NUMBER, destination=DESTINATION_NUMBER))
        list_start.append(StartRecord(
            id=4, timestamp=datetime.datetime(2017, 12, 12, 21, 57, 13, 0, timezone.utc), call_id=73, source=SOURCE_NUMBER, destination=DESTINATION_NUMBER))
        list_start.append(StartRecord(
            id=5, timestamp=datetime.datetime(2017, 12, 12, 4, 57, 13, 0, timezone.utc), call_id=74, source=SOURCE_NUMBER, destination=DESTINATION_NUMBER))
        list_start.append(StartRecord(
            id=6, timestamp=datetime.datetime(2017, 12, 12, 21, 57, 13, 0, timezone.utc), call_id=75, source=SOURCE_NUMBER, destination=DESTINATION_NUMBER))
        list_start.append(StartRecord(
            id=7, timestamp=datetime.datetime(2017, 12, 12, 15, 7, 58, 0, timezone.utc), call_id=76, source=SOURCE_NUMBER, destination=DESTINATION_NUMBER))

        list_end = list()
        list_end.append(EndRecord(
            id=2, timestamp=datetime.datetime(2017, 12, 12, 15, 14, 56, 0, timezone.utc), call_id_id=71, cost=0.99))
        list_end.append(EndRecord(
            id=3, timestamp=datetime.datetime(2017, 12, 12, 22, 50, 56, 0, timezone.utc), call_id_id=72, cost=0.36))
        list_end.append(EndRecord(
            id=4, timestamp=datetime.datetime(2017, 12, 12, 22, 10, 56, 0, timezone.utc), call_id_id=73, cost=0.54))
        list_end.append(EndRecord(
            id=5, timestamp=datetime.datetime(2017, 12, 12, 6, 10, 56, 0, timezone.utc), call_id_id=74, cost=1.26))
        list_end.append(EndRecord(
            id=6, timestamp=datetime.datetime(2017, 12, 13, 22, 10, 56, 0, timezone.utc), call_id_id=75, cost=86.94))
        list_end.append(EndRecord(
            id=7, timestamp=datetime.datetime(2017, 12, 12, 15, 12, 56, 0, timezone.utc), call_id_id=76, cost=0.72))

        self.bill_list = list()
        for i in range(len(list_end)):

            destination = list_start[i].destination

            record_start_time = list_start[i].timestamp
            record_end_time = list_end[i].timestamp
            delta = record_end_time - record_start_time
            h = delta.seconds / 3600  # hours
            m = delta.seconds / 60  # minutes
            s = delta.seconds % 60 # seconds
            duration = '%dh%02dm%02ds' % (h, m, s)

            formatted_price = ('R$ %0.2f' % list_end[i].cost).replace('.',',')

            self.bill_list.append(PhoneBill(
                destination=destination,
                start_date=record_start_time.strftime('%d/%m/%Y'),
                start_time=record_start_time.strftime('%H:%M:%S'),
                duration=duration,
                price=formatted_price, 
            ))

    def test_get_valid_single_end_record(self):
        # get API response

        for start_record in list_start:

            serializer_post = {
                'id': start_record.id,
                'timestamp': str(start_record.timestamp),
                'call_id': start_record.call_id,
                'source': start_record.source,
                'destination': start_record.destination
            }

            response = client.post(
                '/startrecord/',
                data=json.dumps(serializer_post),
                content_type='application/json'
            )
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        for end_record in list_end:
            serializer_post = {
                'id': end_record.id,
                'timestamp': str(end_record.timestamp),
                'call_id_id': end_record.call_id_id
            }

            response = client.post(
                '/endrecord/',
                data=json.dumps(serializer_post),
                content_type='application/json'
            )                

            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = client.get("/phonebill/?source=" + SOURCE_NUMBER + "&period=12/2017")

        serializer_list = PhoneBillSerializer(self.bill_list, many=True)

        pdb.set_trace()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEquals(response.data, serializer_list.data)

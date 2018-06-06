# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
import json

from django.test import TestCase, Client
from django.utils import timezone
from rest_framework import status

from serviceapi.models import StartRecord, EndRecord
from serviceapi.serializers import CallRecordSerializer, \
    PhoneBillSerializer
from serviceapi.utils import RecordType
from phonebilling.settings import TIMESTAMP_FORMAT

client = Client()

SOURCE_NUMBER = '99988526423'
DESTINATION_NUMBER = '9993468278'

ID_1 = 1
ID_2 = 2
ID_3 = 3
ID_4 = 4
ID_5 = 5
ID_6 = 6
ID_7 = 7
ID_8 = 8

CALL_ID_1 = 70
CALL_ID_2 = 71
CALL_ID_3 = 72
CALL_ID_4 = 73
CALL_ID_5 = 74
CALL_ID_6 = 75
CALL_ID_7 = 76
CALL_ID_8 = 77

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


class GetAllStartRecordsTest(TestCase):
    """ Test module for getting all start records API """

    def setUp(self):

        self.list_start = list()

        self.list_start.append(StartRecord(
            id=ID_1, timestamp=START_TIME_1, call_id=CALL_ID_1,
            source=SOURCE_NUMBER, destination=DESTINATION_NUMBER
        ))
        self.list_start.append(StartRecord(
            id=ID_2, timestamp=START_TIME_2, call_id=CALL_ID_2,
            source=SOURCE_NUMBER, destination=DESTINATION_NUMBER
        ))
        self.list_start.append(StartRecord(
            id=ID_3, timestamp=START_TIME_3, call_id=CALL_ID_3,
            source=SOURCE_NUMBER, destination=DESTINATION_NUMBER
        ))
        self.list_start.append(StartRecord(
            id=ID_4, timestamp=START_TIME_4, call_id=CALL_ID_4,
            source=SOURCE_NUMBER, destination=DESTINATION_NUMBER
        ))
        self.list_start.append(StartRecord(
            id=ID_5, timestamp=START_TIME_5, call_id=CALL_ID_5,
            source=SOURCE_NUMBER, destination=DESTINATION_NUMBER
        ))
        self.list_start.append(StartRecord(
            id=ID_6, timestamp=START_TIME_6, call_id=CALL_ID_6,
            source=SOURCE_NUMBER, destination=DESTINATION_NUMBER
        ))
        self.list_start.append(StartRecord(
            id=ID_7, timestamp=START_TIME_7, call_id=CALL_ID_7,
            source=SOURCE_NUMBER, destination=DESTINATION_NUMBER
        ))
        self.list_start.append(StartRecord(
            id=ID_8, timestamp=START_TIME_8, call_id=CALL_ID_8,
            source=SOURCE_NUMBER, destination=DESTINATION_NUMBER
        ))

        self.list_start.reverse()

        self.serialized_list = list()

        # saves the objects and creates the list to match the service response
        for start_record in self.list_start:
            self.serialized_list.append({
                'id': start_record.id,
                'timestamp': start_record.timestamp.strftime(TIMESTAMP_FORMAT),
                'call_id': start_record.call_id,
                'type': RecordType.START.value,
                'source': start_record.source,
                'destination': start_record.destination
            })
            start_record.save()

    def test_get_all_start_records(self):

        response = client.get('/callrecord/')

        serializer = CallRecordSerializer(self.serialized_list, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data, serializer.data)


class GetSingleValidStartRecordTest(TestCase):
    """ Test module for getting single start record """

    def setUp(self):

        self.list_start = list()

        self.start_record = StartRecord(
            id=ID_1, timestamp=START_TIME_1, call_id=CALL_ID_1,
            source=SOURCE_NUMBER, destination=DESTINATION_NUMBER
        )

        # saves the objects and creates the list to match the service response
        self.serialized_list = list()
        self.serialized_list.append({
            'id': self.start_record.id,
            'timestamp': self.start_record.timestamp.strftime(
                TIMESTAMP_FORMAT
            ),
            'call_id': self.start_record.call_id,
            'type': RecordType.START.value,
            'source': self.start_record.source,
            'destination': self.start_record.destination
        })
        self.start_record.save()

    def test_get_single_valid_start_record(self):

        response = client.get('/callrecord/' + str(self.start_record.id) + '/')

        serializer = CallRecordSerializer(self.serialized_list, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data, serializer.data)


class GetSingleInvalidStartRecordTest(TestCase):
    """ Test module for getting single invalid start record """

    def setUp(self):

        self.list_start = list()

        self.start_record = StartRecord(
            id=ID_1, timestamp=START_TIME_1, call_id=CALL_ID_1,
            source=SOURCE_NUMBER, destination=DESTINATION_NUMBER
        )
        self.start_record.save()

    def test_get_single_invalid_start_record(self):

        response = client.get('/callrecord/9999/')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CreateNewStartRecordTest(TestCase):
    """ Test module for inserting a new start record """

    def setUp(self):
        self.valid_startrecord = {
            'id': 10,
            'timestamp':
                START_TIME_1.strftime(TIMESTAMP_FORMAT),
            'call_id': 5,
            'type': RecordType.START.value,
            'source': '11912124425',
            'destination': '11991251242'
        }

        self.start_record_list = list()

        # test with id field (invalid)
        self.start_record_list.append({
            'id': 'A',
            'timestamp':
                START_TIME_1.strftime(TIMESTAMP_FORMAT),
            'call_id': 5,
            'type': RecordType.START.value,
            'source': '11912124425',
            'destination': '11991251242'
        })

        # test with id field (empty)
        self.start_record_list.append({
            'id': '',
            'timestamp':
                START_TIME_1.strftime(TIMESTAMP_FORMAT),
            'call_id': 5,
            'type': RecordType.START.value,
            'source': '11912124425',
            'destination': '11991251242'
        })

        # test with id field (removed)
        self.start_record_list.append({
            'timestamp':
                START_TIME_1.strftime(TIMESTAMP_FORMAT),
            'call_id': 5,
            'type': RecordType.START.value,
            'source': '11912124425',
            'destination': '11991251242'
        })

        # test with timestamp field (invalid)
        self.start_record_list.append({
            'id': 2,
            'timestamp': '9999-99-99T99:99:99Z',
            'call_id': 5,
            'type': RecordType.START.value,
            'source': '11912124425',
            'destination': '11991251242'
        })

        # test with timestamp field (empty)
        self.start_record_list.append({
            'id': 2,
            'timestamp': '',
            'call_id': 5,
            'type': RecordType.START.value,
            'source': '11912124425',
            'destination': '11991251242'
        })

        # test with timestamp field (removed)
        self.start_record_list.append({
            'id': 2,
            'call_id': 5,
            'type': RecordType.START.value,
            'source': '11912124425',
            'destination': '11991251242'
        })

        # test with call_id field (invalid)
        self.start_record_list.append({
            'id': 3,
            'timestamp':
                START_TIME_1.strftime(TIMESTAMP_FORMAT),
            'call_id': 'B',
            'type': RecordType.START.value,
            'source': '11912124425',
            'destination': '11991251242'
        })

        # test with call_id field (empty)
        self.start_record_list.append({
            'id': 3,
            'timestamp':
                START_TIME_1.strftime(TIMESTAMP_FORMAT),
            'call_id': '',
            'type': RecordType.START.value,
            'source': '11912124425',
            'destination': '11991251242'
        })

        # test with call_id field (removed)
        self.start_record_list.append({
            'id': 3,
            'timestamp':
                START_TIME_1.strftime(TIMESTAMP_FORMAT),
            'type': RecordType.START.value,
            'source': '11912124425',
            'destination': '11991251242'
        })

        # test with type field (invalid)
        self.start_record_list.append({
            'id': 3,
            'timestamp':
                START_TIME_1.strftime(TIMESTAMP_FORMAT),
            'call_id': 5,
            'type': 0,
            'source': '11912124425',
            'destination': '11991251242'
        })

        # test with type field (invalid)
        self.start_record_list.append({
            'id': 3,
            'timestamp':
                START_TIME_1.strftime(TIMESTAMP_FORMAT),
            'call_id': 5,
            'type': 'A',
            'source': '11912124425',
            'destination': '11991251242'
        })

        # test with type field (empty)
        self.start_record_list.append({
            'id': 3,
            'timestamp':
                START_TIME_1.strftime(TIMESTAMP_FORMAT),
            'call_id': 5,
            'type': '',
            'source': '11912124425',
            'destination': '11991251242'
        })

        # test with type field (removed)
        self.start_record_list.append({
            'id': 3,
            'timestamp':
                START_TIME_1.strftime(TIMESTAMP_FORMAT),
            'call_id': 5,
            'source': '11912124425',
            'destination': '11991251242'
        })

        # test with source field (length - 9)
        self.start_record_list.append({
            'id': 4,
            'timestamp':
                START_TIME_1.strftime(TIMESTAMP_FORMAT),
            'call_id': 5,
            'type': RecordType.START.value,
            'source': '119121244',
            'destination': '11991251242'
        })

        # test with source field (length - 12)
        self.start_record_list.append({
            'id': 4,
            'timestamp':
                START_TIME_1.strftime(TIMESTAMP_FORMAT),
            'call_id': 5,
            'type': RecordType.START.value,
            'source': '119121244123',
            'destination': '11991251242'
        })

        # test with source field (invalid)
        self.start_record_list.append({
            'id': 5,
            'timestamp':
                START_TIME_1.strftime(TIMESTAMP_FORMAT),
            'call_id': 5,
            'type': RecordType.START.value,
            'source': 'A1912124425',
            'destination': '11991251242'
        })

        # test with source field (empty)
        self.start_record_list.append({
            'id': 5,
            'timestamp':
                START_TIME_1.strftime(TIMESTAMP_FORMAT),
            'call_id': 5,
            'type': RecordType.START.value,
            'source': '',
            'destination': '11991251242'
        })

        # test with destination field (length - 9)
        self.start_record_list.append({
            'id': 6,
            'timestamp':
                START_TIME_1.strftime(TIMESTAMP_FORMAT),
            'call_id': 5,
            'type': RecordType.START.value,
            'source': '11912124425',
            'destination': '119912512'
        })

        # test with destination field (length - 12)
        self.start_record_list.append({
            'id': 6,
            'timestamp':
                START_TIME_1.strftime(TIMESTAMP_FORMAT),
            'call_id': 5,
            'type': RecordType.START.value,
            'source': '11912124425',
            'destination': '119912512111'
        })

        # test with destionation field (invalid)
        self.start_record_list.append({
            'id': 7,
            'timestamp':
                START_TIME_1.strftime(TIMESTAMP_FORMAT),
            'call_id': 5,
            'type': RecordType.START.value,
            'source': '11912124425',
            'destination': 'B1991251242'
        })

        # test with destination field (empty)
        self.start_record_list.append({
            'id': 7,
            'timestamp':
                START_TIME_1.strftime(TIMESTAMP_FORMAT),
            'call_id': 5,
            'type': RecordType.START.value,
            'source': '11912124425',
            'destination': ''
        })

        # test with destination field (removed)
        self.start_record_list.append({
            'id': 7,
            'timestamp':
                START_TIME_1.strftime(TIMESTAMP_FORMAT),
            'call_id': 5,
            'type': RecordType.START.value,
            'source': '11912124425'
        })

    def test_create_valid_start_record(self):
        response = client.post(
            '/callrecord/',
            data=json.dumps(self.valid_startrecord),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_start_record(self):
        for record in self.start_record_list:
            response = client.post(
                '/callrecord/',
                data=json.dumps(record),
                content_type='application/json'
            )
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UpdateSingleStartRecordTest(TestCase):
    """ Test module for updating an existing start record record """

    def setUp(self):

        self.list_start = list()
        self.list_start.append(StartRecord(
            id=ID_1, timestamp=START_TIME_1,
            call_id=CALL_ID_1, source=SOURCE_NUMBER,
            destination=DESTINATION_NUMBER
        ))
        self.list_start.append(StartRecord(
            id=ID_2, timestamp=START_TIME_2,
            call_id=CALL_ID_2, source=SOURCE_NUMBER,
            destination=DESTINATION_NUMBER
        ))

        for self.start_record in self.list_start:
            self.start_record.save()

        self.valid_start_record = {
            'id': 1,
            'timestamp': START_TIME_1.strftime(TIMESTAMP_FORMAT),
            'call_id': CALL_ID_4,
            'type': RecordType.START.value,
            'source': SOURCE_NUMBER,
            'destination': DESTINATION_NUMBER
        }

        self.invalid_start_record = {
            'id': 2,
            'timestamp': START_TIME_1.strftime(TIMESTAMP_FORMAT),
            'call_id': '',
            'type': RecordType.START.value,
            'source': SOURCE_NUMBER,
            'destination': DESTINATION_NUMBER
        }

    def test_valid_update_start_record(self):
        response = client.put(
            '/callrecord/' + str(self.valid_start_record['id']) + '/',
            data=json.dumps(self.valid_start_record),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_update_start_record(self):
        response = client.put(
            '/callrecord/' + str(self.invalid_start_record['id']) + '/',
            data=json.dumps(self.invalid_start_record),
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DeleteSingleStartRecordTest(TestCase):
    """ Test module for deleting an existing start record """

    def setUp(self):
        self.list_start = list()
        self.list_start.append(StartRecord(
            id=ID_1, timestamp=START_TIME_1, call_id=CALL_ID_1,
            source=SOURCE_NUMBER, destination=DESTINATION_NUMBER
        ))
        self.list_start.append(StartRecord(
            id=ID_2, timestamp=START_TIME_2, call_id=CALL_ID_2,
            source=SOURCE_NUMBER, destination=DESTINATION_NUMBER
        ))

        for self.start_record in self.list_start:
            self.start_record.save()

    def test_valid_delete_start_record(self):
        response = client.delete(
            '/callrecord/' + str(self.list_start[0].id) + '/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_delete_start_record(self):
        response = client.delete(
            '/callrecord/9999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


# ************************************
# ************************************
# End Record Tests
# ************************************
# ************************************


class GetAllEndRecordsTest(TestCase):
    """ Test module for getting all end records API """

    def setUp(self):

        self.list_end = list()

        self.list_end.append(EndRecord(
            id=ID_1, timestamp=END_TIME_1, start_id=CALL_ID_1, cost=0.22
        ))
        self.list_end.append(EndRecord(
            id=ID_2, timestamp=END_TIME_2, start_id=CALL_ID_2, cost=0.99
        ))
        self.list_end.append(EndRecord(
            id=ID_3, timestamp=END_TIME_3, start_id=CALL_ID_3, cost=0.26
        ))
        self.list_end.append(EndRecord(
            id=ID_4, timestamp=END_TIME_4, start_id=CALL_ID_4, cost=0.54
        ))
        self.list_end.append(EndRecord(
            id=ID_5, timestamp=END_TIME_5, start_id=CALL_ID_5, cost=1.26
        ))
        self.list_end.append(EndRecord(
            id=ID_6, timestamp=END_TIME_6, start_id=CALL_ID_6, cost=86.94
        ))
        self.list_end.append(EndRecord(
            id=ID_7, timestamp=END_TIME_7, start_id=CALL_ID_7, cost=0.72
        ))
        self.list_end.append(EndRecord(
            id=ID_8, timestamp=END_TIME_8, start_id=CALL_ID_8, cost=0.22
        ))

        self.list_end.reverse()

        self.serialized_list = list()

        # saves the objects and creates the list to match the service response
        for end_record in self.list_end:
            self.serialized_list.append({
                'id': end_record.id,
                'timestamp': end_record.timestamp.strftime(TIMESTAMP_FORMAT),
                'call_id': end_record.start_id,
                'type': RecordType.END.value
            })
            end_record.save()

    def test_get_all_end_records(self):

        response = client.get('/callrecord/')

        serializer = CallRecordSerializer(self.serialized_list, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data, serializer.data)


class GetSingleValidEndRecordTest(TestCase):
    """ Test module for getting single end record """

    def setUp(self):

        self.end_record = EndRecord(
            id=ID_1, timestamp=END_TIME_1, start_id=CALL_ID_1, cost=0.22
        )
        self.end_record.save()

        # saves the objects and creates the list to match the service response
        self.serialized_list = list()

        self.serialized_list.append({
            'id': self.end_record.id,
            'timestamp': self.end_record.timestamp.strftime(TIMESTAMP_FORMAT),
            'call_id': self.end_record.start_id,
            'type': RecordType.END.value
        })

    def test_get_single_valid_end_record(self):

        response = client.get('/callrecord/' + str(self.end_record.id) + '/')

        serializer = CallRecordSerializer(self.serialized_list, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data, serializer.data)


class GetSingleInvalidEndRecordTest(TestCase):
    """ Test module for getting single invalid end record """

    def setUp(self):

        self.list_end = list()

        self.end_record = EndRecord(
            id=ID_1, timestamp=END_TIME_1, start_id=CALL_ID_1, cost=0.22
        )

        # saves the objects and creates the list to match the service response
        self.serialized_list = list()
        self.serialized_list.append({
            'id': self.end_record.id,
            'timestamp': self.end_record.timestamp.strftime(TIMESTAMP_FORMAT),
            'call_id': self.end_record.start_id,
            'type': RecordType.END.value
        })
        self.end_record.save()

    def test_get_single_invalid_end_record(self):

        response = client.get('/callrecord/9999/')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CreateNewEndRecordTest(TestCase):
    """ Test module for inserting a new end record """

    def setUp(self):

        self.list_start = list()

        # saves all start records
        self.list_start.append(StartRecord(
            id=ID_1, timestamp=START_TIME_1, call_id=CALL_ID_1,
            source=SOURCE_NUMBER, destination=DESTINATION_NUMBER
        ))
        self.list_start.append(StartRecord(
            id=ID_2, timestamp=START_TIME_2, call_id=CALL_ID_2,
            source=SOURCE_NUMBER, destination=DESTINATION_NUMBER
        ))
        self.list_start.append(StartRecord(
            id=ID_3, timestamp=START_TIME_3, call_id=CALL_ID_3,
            source=SOURCE_NUMBER, destination=DESTINATION_NUMBER
        ))
        self.list_start.append(StartRecord(
            id=ID_4, timestamp=START_TIME_4, call_id=CALL_ID_4,
            source=SOURCE_NUMBER, destination=DESTINATION_NUMBER
        ))
        self.list_start.append(StartRecord(
            id=ID_5, timestamp=START_TIME_5, call_id=CALL_ID_5,
            source=SOURCE_NUMBER, destination=DESTINATION_NUMBER
        ))
        self.list_start.append(StartRecord(
            id=ID_6, timestamp=START_TIME_6, call_id=CALL_ID_6,
            source=SOURCE_NUMBER, destination=DESTINATION_NUMBER
        ))
        self.list_start.append(StartRecord(
            id=ID_7, timestamp=START_TIME_7, call_id=CALL_ID_7,
            source=SOURCE_NUMBER, destination=DESTINATION_NUMBER
        ))
        self.list_start.append(StartRecord(
            id=ID_8, timestamp=START_TIME_8, call_id=CALL_ID_8,
            source=SOURCE_NUMBER, destination=DESTINATION_NUMBER
        ))

        # saves all start records
        for start_record in self.list_start:
            start_record.save()

        self.valid_endrecord = {
            'id': 1,
            'timestamp':
                END_TIME_1.strftime(TIMESTAMP_FORMAT),
            'call_id': CALL_ID_1,
            'type': RecordType.END.value
        }

        self.end_record_list = list()

        # test with id field (invalid)
        self.end_record_list.append({
            'id': 'A',
            'timestamp':
                END_TIME_1.strftime(TIMESTAMP_FORMAT),
            'call_id': CALL_ID_1,
            'type': RecordType.END.value
        })

        # test with id field (empty)
        self.end_record_list.append({
            'id': '',
            'timestamp':
                END_TIME_1.strftime(TIMESTAMP_FORMAT),
            'call_id': CALL_ID_1,
            'type': RecordType.END.value
        })

        # test with id field (removed)
        self.end_record_list.append({
            'timestamp':
                END_TIME_1.strftime(TIMESTAMP_FORMAT),
            'call_id': CALL_ID_1,
            'type': RecordType.END.value
        })

        # test with timestamp field (invalid format)
        self.end_record_list.append({
            'id': 1,
            'timestamp': '9999-99-99T99:99:99Z',
            'call_id': CALL_ID_1,
            'type': RecordType.END.value
        })

        # test with timestamp field (empty)
        self.end_record_list.append({
            'id': 1,
            'timestamp': '',
            'call_id': CALL_ID_1,
            'type': RecordType.END.value
        })

        # test with timestamp field (removed)
        self.end_record_list.append({
            'id': 1,
            'call_id': CALL_ID_1,
            'type': RecordType.END.value
        })

        # test with call_id field (invalid)
        self.end_record_list.append({
            'id': 1,
            'timestamp':
                END_TIME_1.strftime(TIMESTAMP_FORMAT),
            'call_id': 'B',
            'type': RecordType.END.value
        })

        # test with call_id field (empty)
        self.end_record_list.append({
            'id': 1,
            'timestamp':
                END_TIME_1.strftime(TIMESTAMP_FORMAT),
            'call_id': '',
            'type': RecordType.END.value
        })

        # test with call_id field (removed)
        self.end_record_list.append({
            'id': 1,
            'timestamp':
                END_TIME_1.strftime(TIMESTAMP_FORMAT),
            'type': RecordType.END.value
        })

        # test with type field (empty)
        self.end_record_list.append({
            'id': 1,
            'timestamp':
                END_TIME_1.strftime(TIMESTAMP_FORMAT),
            'call_id': CALL_ID_1,
            'type': ''
        })

        # test with type field (invalid)
        self.end_record_list.append({
            'id': 1,
            'timestamp':
                END_TIME_1.strftime(TIMESTAMP_FORMAT),
            'call_id': CALL_ID_1,
            'type': 'B'
        })

        # test with type field (removed)
        self.end_record_list.append({
            'id': 1,
            'timestamp':
                END_TIME_1.strftime(TIMESTAMP_FORMAT),
            'call_id': CALL_ID_1
        })

    def test_create_valid_end_record(self):
        response = client.post(
            '/callrecord/',
            data=json.dumps(self.valid_endrecord),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_end_record(self):
        for record in self.end_record_list:
            response = client.post(
                '/callrecord/',
                data=json.dumps(record),
                content_type='application/json'
            )
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UpdateSingleEndRecordTest(TestCase):
    """ Test module for updating an existing end record """

    def setUp(self):

        self.list_start = list()

        self.list_start.append(StartRecord(
            id=ID_1, timestamp=START_TIME_1, call_id=CALL_ID_1,
            source=SOURCE_NUMBER, destination=DESTINATION_NUMBER
        ))
        self.list_start.append(StartRecord(
            id=ID_2, timestamp=START_TIME_2, call_id=CALL_ID_2,
            source=SOURCE_NUMBER, destination=DESTINATION_NUMBER
        ))

        for start_record in self.list_start:
            start_record.save()

        self.list_end = list()
        self.list_end.append(EndRecord(
            id=ID_1, timestamp=END_TIME_1, start_id=CALL_ID_1, cost=0.22
        ))
        self.list_end.append(EndRecord(
            id=ID_2, timestamp=END_TIME_2, start_id=CALL_ID_2, cost=0.22
        ))

        for self.end_record in self.list_end:
            self.end_record.save()

        self.valid_end_record = {
            'id': 1,
            'timestamp': END_TIME_1.strftime(TIMESTAMP_FORMAT),
            'call_id': CALL_ID_1,
            'type': RecordType.END.value
        }

        self.invalid_end_record = {
            'id': 2,
            'timestamp': END_TIME_1.strftime(TIMESTAMP_FORMAT),
            'call_id': '',
            'type': RecordType.END.value
        }

    def test_valid_update_end_record(self):
        response = client.put(
            '/callrecord/' + str(self.valid_end_record['id']) + '/',
            data=json.dumps(self.valid_end_record),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_update_end_record(self):
        response = client.put(
            '/callrecord/' + str(self.invalid_end_record['id']) + '/',
            data=json.dumps(self.invalid_end_record),
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DeleteSingleEndRecordTest(TestCase):
    """ Test module for deleting an existing end record """

    def setUp(self):
        self.list_end = list()
        self.list_end.append(EndRecord(
            id=ID_1, timestamp=END_TIME_1, start_id=CALL_ID_1, cost=0.33
        ))
        self.list_end.append(EndRecord(
            id=ID_2, timestamp=END_TIME_2, start_id=CALL_ID_2, cost=0.44
        ))

        for self.end_record in self.list_end:
            self.end_record.save()

    def test_valid_delete_end_record(self):
        response = client.delete(
            '/callrecord/' + str(self.list_end[0].id) + '/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_delete_end_record(self):
        response = client.delete(
            '/callrecord/9999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


# ************************************
# ************************************
# Phone Bill Tests
# ************************************
# ************************************


class GetPhoneBillTest(TestCase):
    """ Test module for getting phone bill """

    def setUp(self):

        # creates the list with call start records
        self.list_start = list()

        self.list_start.append({
            'id': 2, 'timestamp': START_TIME_2, 'call_id': CALL_ID_2,
            'type': RecordType.START.value, 'source': SOURCE_NUMBER,
            'destination': DESTINATION_NUMBER
        })

        self.list_start.append({
            'id': 3, 'timestamp': START_TIME_3, 'call_id': CALL_ID_3,
            'type': RecordType.START.value, 'source': SOURCE_NUMBER,
            'destination': DESTINATION_NUMBER
        })

        self.list_start.append({
            'id': 4, 'timestamp': START_TIME_4, 'call_id': CALL_ID_4,
            'type': RecordType.START.value, 'source': SOURCE_NUMBER,
            'destination': DESTINATION_NUMBER
        })

        self.list_start.append({
            'id': 5, 'timestamp': START_TIME_5, 'call_id': CALL_ID_5,
            'type': RecordType.START.value, 'source': SOURCE_NUMBER,
            'destination': DESTINATION_NUMBER
        })

        self.list_start.append({
            'id': 6, 'timestamp': START_TIME_6, 'call_id': CALL_ID_6,
            'type': RecordType.START.value, 'source': SOURCE_NUMBER,
            'destination': DESTINATION_NUMBER
        })

        self.list_start.append({
            'id': 7, 'timestamp': START_TIME_7, 'call_id': CALL_ID_7,
            'type': RecordType.START.value, 'source': SOURCE_NUMBER,
            'destination': DESTINATION_NUMBER
        })

        # creates the list with call end records
        self.list_end = list()

        self.list_end.append({
            'id': 2, 'timestamp': END_TIME_2, 'call_id': CALL_ID_2,
            'type': RecordType.END.value, 'cost': 0.99
        })

        self.list_end.append({
            'id': 3, 'timestamp': END_TIME_3, 'call_id': CALL_ID_3,
            'type': RecordType.END.value, 'cost': 0.36
        })

        self.list_end.append({
            'id': 4, 'timestamp': END_TIME_4, 'call_id': CALL_ID_4,
            'type': RecordType.END.value, 'cost': 0.54
        })

        self.list_end.append({
            'id': 5, 'timestamp': END_TIME_5, 'call_id': CALL_ID_5,
            'type': RecordType.END.value, 'cost': 1.26
        })

        self.list_end.append({
            'id': 6, 'timestamp': END_TIME_6, 'call_id': CALL_ID_6,
            'type': RecordType.END.value, 'cost': 86.94
        })

        self.list_end.append({
            'id': 7, 'timestamp': END_TIME_7, 'call_id': CALL_ID_7,
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

            # formatted list that will be serialized later
            self.bill_list.append(PhoneBill(
                destination=destination,
                start_date=record_start_time.strftime('%d/%m/%Y'),
                start_time=record_start_time.strftime('%H:%M:%S'),
                duration=duration,
                price=formatted_price,
            ))

        # transforms timestamp to string format (list_start)
        for item in self.list_start:
            item['timestamp'] = item['timestamp'].strftime(TIMESTAMP_FORMAT)

        # transforms timestamp to string format (list_end)
        for item in self.list_end:
            item['timestamp'] = item['timestamp'].strftime(TIMESTAMP_FORMAT)

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
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Then post all end records
        for end_record in self.list_end:
            response = client.post(
                '/callrecord/',
                data=json.dumps(end_record),
                content_type='application/json'
            )
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Now get the detailed phone bill and match the response
        response = client.get('/phonebill/?source=' +
                              SOURCE_NUMBER + '&period=12/2017')

        serializer_list = PhoneBillSerializer(self.bill_list, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data, serializer_list.data)

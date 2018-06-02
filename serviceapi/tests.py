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
    """ Test module for GET all puppies API """

    def setUp(self):

        self.list_start = list()

        self.list_start.append(StartRecord(
            id=1, timestamp=START_TIME_1, call_id=70,
            source=SOURCE_NUMBER, destination=DESTINATION_NUMBER
        ))
        self.list_start.append(StartRecord(
            id=2, timestamp=START_TIME_2, call_id=71,
            source=SOURCE_NUMBER, destination=DESTINATION_NUMBER
        ))
        self.list_start.append(StartRecord(
            id=3, timestamp=START_TIME_3, call_id=72,
            source=SOURCE_NUMBER, destination=DESTINATION_NUMBER
        ))
        self.list_start.append(StartRecord(
            id=4, timestamp=START_TIME_4, call_id=73,
            source=SOURCE_NUMBER, destination=DESTINATION_NUMBER
        ))
        self.list_start.append(StartRecord(
            id=5, timestamp=START_TIME_5, call_id=74,
            source=SOURCE_NUMBER, destination=DESTINATION_NUMBER
        ))
        self.list_start.append(StartRecord(
            id=6, timestamp=START_TIME_6, call_id=75,
            source=SOURCE_NUMBER, destination=DESTINATION_NUMBER
        ))
        self.list_start.append(StartRecord(
            id=7, timestamp=START_TIME_7, call_id=76,
            source=SOURCE_NUMBER, destination=DESTINATION_NUMBER
        ))
        self.list_start.append(StartRecord(
            id=8, timestamp=START_TIME_8, call_id=77,
            source=SOURCE_NUMBER, destination=DESTINATION_NUMBER
        ))

        self.list_start.reverse()

        self.serialized_list = list()

        # saves the objects and creates the list to match the service response
        for start_record in self.list_start:
            self.serialized_list.append({
                'id': start_record.id,
                'timestamp': str(start_record.timestamp),
                'call_id': start_record.call_id,
                'type': RecordType.START.value,
                'source': start_record.source,
                'destination': start_record.destination
            })
            start_record.save()

    def test_get_all_start_records(self):
        # get API response
        response = client.get("/callrecord/")

        serializer = CallRecordSerializer(self.serialized_list, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data, serializer.data)


class GetSingleValidStartRecordTest(TestCase):
    """ Test module for GET single start record """

    def setUp(self):

        self.list_start = list()

        self.start_record = StartRecord(
            id=1, timestamp=START_TIME_1, call_id=70,
            source=SOURCE_NUMBER, destination=DESTINATION_NUMBER
        )

        # saves the objects and creates the list to match the service response
        self.serialized_list = list()
        self.serialized_list.append({
            'id': self.start_record.id,
            'timestamp': str(self.start_record.timestamp),
            'call_id': self.start_record.call_id,
            'type': RecordType.START.value,
            'source': self.start_record.source,
            'destination': self.start_record.destination
        })
        self.start_record.save()

    def test_get_single_valid_start_record(self):
        # get API response

        response = client.get('/callrecord/' + str(self.start_record.id) + '/')

        serializer = CallRecordSerializer(self.serialized_list, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data, serializer.data)


class GetSingleInvalidStartRecordTest(TestCase):
    """ Test module for GET single start record """

    def setUp(self):

        self.list_start = list()

        self.start_record = StartRecord(
            id=1, timestamp=START_TIME_1, call_id=70,
            source=SOURCE_NUMBER, destination=DESTINATION_NUMBER
        )

        # saves the objects and creates the list to match the service response
        self.serialized_list = list()
        self.serialized_list.append({
            'id': self.start_record.id,
            'timestamp': str(self.start_record.timestamp),
            'call_id': self.start_record.call_id,
            'type': RecordType.START.value,
            'source': self.start_record.source,
            'destination': self.start_record.destination
        })
        self.start_record.save()

    def test_get_single_invalid_start_record(self):
        # get API response
        response = client.get("/callrecord/9999/")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CreateNewStartRecordTest(TestCase):
    """ Test module for inserting a new puppy """

    def setUp(self):
        self.valid_startrecord = {
            'id': 10,
            'timestamp':
                str(START_TIME_1),
            'call_id': 5,
            'type': RecordType.START.value,
            'source': '11912124425',
            'destination': '11991251242'
        }

        self.start_record_list = list()

        self.start_record_list.append({
            'id': 'A',
            'timestamp':
                str(START_TIME_1),
            'call_id': 5,
            'type': RecordType.START.value,
            'source': '11912124425',
            'destination': '11991251242'
        })

        self.start_record_list.append({
            'id': '',
            'timestamp':
                str(START_TIME_1),
            'call_id': 5,
            'type': RecordType.START.value,
            'source': '11912124425',
            'destination': '11991251242'
        })

        self.start_record_list.append({
            'id': 2,
            'timestamp': '9999-99-99T99:99:99Z',
            'call_id': 5,
            'type': RecordType.START.value,
            'source': '11912124425',
            'destination': '11991251242'
        })

        self.start_record_list.append({
            'id': 2,
            'timestamp': '',
            'call_id': 5,
            'type': RecordType.START.value,
            'source': '11912124425',
            'destination': '11991251242'
        })

        self.start_record_list.append({
            'id': 3,
            'timestamp':
                str(START_TIME_1),
            'call_id': 'B',
            'type': RecordType.START.value,
            'source': '11912124425',
            'destination': '11991251242'
        })

        self.start_record_list.append({
            'id': 3,
            'timestamp':
                str(START_TIME_1),
            'call_id': '',
            'type': RecordType.START.value,
            'source': '11912124425',
            'destination': '11991251242'
        })

        self.start_record_list.append({
            'id': 3,
            'timestamp':
                str(START_TIME_1),
            'call_id': 5,
            'type': '',
            'source': '11912124425',
            'destination': '11991251242'
        })

        self.start_record_list.append({
            'id': 3,
            'timestamp':
                str(START_TIME_1),
            'call_id': 5,
            'type': 'B',
            'source': '11912124425',
            'destination': '11991251242'
        })

        self.start_record_list.append({
            'id': 4,
            'timestamp':
                str(START_TIME_1),
            'call_id': 5,
            'type': RecordType.START.value,
            'source': '119121244',
            'destination': '11991251242'
        })

        self.start_record_list.append({
            'id': 4,
            'timestamp':
                str(START_TIME_1),
            'call_id': 5,
            'type': RecordType.START.value,
            'source': '',
            'destination': '11991251242'
        })

        self.start_record_list.append({
            'id': 5,
            'timestamp':
                str(START_TIME_1),
            'call_id': 5,
            'type': RecordType.START.value,
            'source': 'A1912124425',
            'destination': '11991251242'
        })

        self.start_record_list.append({
            'id': 5,
            'timestamp':
                str(START_TIME_1),
            'call_id': 5,
            'type': RecordType.START.value,
            'source': '',
            'destination': '11991251242'
        })

        self.start_record_list.append({
            'id': 6,
            'timestamp':
                str(START_TIME_1),
            'call_id': 5,
            'type': RecordType.START.value,
            'source': '11912124425',
            'destination': '119912512'
        })

        self.start_record_list.append({
            'id': 7,
            'timestamp':
                str(START_TIME_1),
            'call_id': 5,
            'type': RecordType.START.value,
            'source': '11912124425',
            'destination': 'B1991251242'
        })

        self.start_record_list.append({
            'id': 7,
            'timestamp':
                str(START_TIME_1),
            'call_id': 5,
            'type': RecordType.START.value,
            'source': '11912124425',
            'destination': ''
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
    """ Test module for updating an existing puppy record """

    def setUp(self):

        self.list_start = list()
        self.list_start.append(StartRecord(
            id=1, timestamp=START_TIME_1,
            call_id=70, source=SOURCE_NUMBER,
            destination=DESTINATION_NUMBER
        ))
        self.list_start.append(StartRecord(
            id=2, timestamp=START_TIME_2,
            call_id=71, source=SOURCE_NUMBER,
            destination=DESTINATION_NUMBER
        ))

        for self.start_record in self.list_start:
            self.start_record.save()

        self.valid_start_record = {
            'id': 1,
            'timestamp': str(START_TIME_1),
            'call_id': 73,
            'type': RecordType.START.value,
            'source': SOURCE_NUMBER,
            'destination': DESTINATION_NUMBER
        }

        self.invalid_start_record = {
            'id': 2,
            'timestamp': str(START_TIME_1),
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
    """ Test module for deleting an existing puppy record """

    def setUp(self):
        self.list_start = list()
        self.list_start.append(StartRecord(
            id=1, timestamp=START_TIME_1, call_id=70,
            source=SOURCE_NUMBER, destination=DESTINATION_NUMBER
        ))
        self.list_start.append(StartRecord(
            id=2, timestamp=START_TIME_2, call_id=71,
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
    """ Test module for GET all puppies API """

    def setUp(self):

        self.list_end = list()

        self.list_end.append(EndRecord(
            id=1, timestamp=END_TIME_1, start_id=70, cost=0.22
        ))
        self.list_end.append(EndRecord(
            id=2, timestamp=END_TIME_2, start_id=71, cost=0.99
        ))
        self.list_end.append(EndRecord(
            id=3, timestamp=END_TIME_3, start_id=72, cost=0.26
        ))
        self.list_end.append(EndRecord(
            id=4, timestamp=END_TIME_4, start_id=73, cost=0.54
        ))
        self.list_end.append(EndRecord(
            id=5, timestamp=END_TIME_5, start_id=74, cost=1.26
        ))
        self.list_end.append(EndRecord(
            id=6, timestamp=END_TIME_6, start_id=75, cost=86.94
        ))
        self.list_end.append(EndRecord(
            id=7, timestamp=END_TIME_7, start_id=76, cost=0.72
        ))
        self.list_end.append(EndRecord(
            id=8, timestamp=END_TIME_8, start_id=77, cost=0.22
        ))

        self.list_end.reverse()

        self.serialized_list = list()

        # saves the objects and creates the list to match the service response
        for end_record in self.list_end:
            self.serialized_list.append({
                'id': end_record.id,
                'timestamp': str(end_record.timestamp),
                'call_id': end_record.start_id,
                'type': RecordType.END.value
            })
            end_record.save()

    def test_get_all_end_records(self):
        # get API response
        response = client.get("/callrecord/")

        serializer = CallRecordSerializer(self.serialized_list, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data, serializer.data)


class GetSingleValidEndRecordTest(TestCase):
    """ Test module for GET single end record """

    def setUp(self):

        self.end_record = EndRecord(
            id=1, timestamp=END_TIME_1, start_id=70, cost=0.22
        )
        self.end_record.save()

        # saves the objects and creates the list to match the service response
        self.serialized_list = list()

        self.serialized_list.append({
            'id': self.end_record.id,
            'timestamp': str(self.end_record.timestamp),
            'call_id': self.end_record.start_id,
            'type': RecordType.END.value
        })

    def test_get_single_valid_end_record(self):
        # get API response
        response = client.get('/callrecord/' + str(self.end_record.id) + '/')

        serializer = CallRecordSerializer(self.serialized_list, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data, serializer.data)


class GetSingleInvalidEndRecordTest(TestCase):
    """ Test module for GET single end record """

    def setUp(self):

        self.list_end = list()

        self.end_record = EndRecord(
            id=1, timestamp=END_TIME_1, start_id=70, cost=0.22
        )

        # saves the objects and creates the list to match the service response
        self.serialized_list = list()
        self.serialized_list.append({
            'id': self.end_record.id,
            'timestamp': str(self.end_record.timestamp),
            'call_id': self.end_record.start_id,
            'type': RecordType.END.value
        })
        self.end_record.save()

    def test_get_single_invalid_end_record(self):
        # get API response
        response = client.get("/callrecord/9999/")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CreateNewEndRecordTest(TestCase):
    """ Test module for inserting a new puppy """

    def setUp(self):

        self.list_start = list()

        self.list_start.append(StartRecord(
            id=1, timestamp=START_TIME_1, call_id=70,
            source=SOURCE_NUMBER, destination=DESTINATION_NUMBER
        ))
        self.list_start.append(StartRecord(
            id=2, timestamp=START_TIME_2, call_id=71,
            source=SOURCE_NUMBER, destination=DESTINATION_NUMBER
        ))
        self.list_start.append(StartRecord(
            id=3, timestamp=START_TIME_3, call_id=72,
            source=SOURCE_NUMBER, destination=DESTINATION_NUMBER
        ))
        self.list_start.append(StartRecord(
            id=4, timestamp=START_TIME_4, call_id=73,
            source=SOURCE_NUMBER, destination=DESTINATION_NUMBER
        ))
        self.list_start.append(StartRecord(
            id=5, timestamp=START_TIME_5, call_id=74,
            source=SOURCE_NUMBER, destination=DESTINATION_NUMBER
        ))
        self.list_start.append(StartRecord(
            id=6, timestamp=START_TIME_6, call_id=75,
            source=SOURCE_NUMBER, destination=DESTINATION_NUMBER
        ))
        self.list_start.append(StartRecord(
            id=7, timestamp=START_TIME_7, call_id=76,
            source=SOURCE_NUMBER, destination=DESTINATION_NUMBER
        ))
        self.list_start.append(StartRecord(
            id=8, timestamp=START_TIME_8, call_id=77,
            source=SOURCE_NUMBER, destination=DESTINATION_NUMBER
        ))

        for start_record in self.list_start:
            start_record.save()

        self.valid_endrecord = {
            'id': 1,
            'timestamp':
                str(END_TIME_1),
            'call_id': 70,
            'type': RecordType.END.value
        }

        self.end_record_list = list()

        self.end_record_list.append({
            'id': 'A',
            'timestamp':
                str(END_TIME_1),
            'call_id': 70,
            'type': RecordType.END.value
        })

        self.end_record_list.append({
            'id': '',
            'timestamp':
                str(END_TIME_1),
            'call_id': 70,
            'type': RecordType.END.value
        })

        self.end_record_list.append({
            'id': 1,
            'timestamp': '9999-99-99T99:99:99Z',
            'call_id': 70,
            'type': RecordType.END.value
        })

        self.end_record_list.append({
            'id': 1,
            'timestamp': '',
            'call_id': 70,
            'type': RecordType.END.value
        })

        self.end_record_list.append({
            'id': 1,
            'timestamp':
                str(END_TIME_1),
            'call_id': 'B',
            'type': RecordType.END.value
        })

        self.end_record_list.append({
            'id': 1,
            'timestamp':
                str(END_TIME_1),
            'call_id': '',
            'type': RecordType.END.value
        })

        self.end_record_list.append({
            'id': 1,
            'timestamp':
                str(END_TIME_1),
            'call_id': 70,
            'type': ''
        })

        self.end_record_list.append({
            'id': 1,
            'timestamp':
                str(END_TIME_1),
            'call_id': 70,
            'type': 'B'
        })

    def test_create_valid_end_record(self):
        a = json.dumps(self.valid_endrecord)
        response = client.post(
            '/callrecord/',
            data=a,
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
    """ Test module for updating an existing puppy record """

    def setUp(self):

        self.list_start = list()

        self.list_start.append(StartRecord(
            id=1, timestamp=START_TIME_1, call_id=70,
            source=SOURCE_NUMBER, destination=DESTINATION_NUMBER
        ))
        self.list_start.append(StartRecord(
            id=2, timestamp=START_TIME_2, call_id=71,
            source=SOURCE_NUMBER, destination=DESTINATION_NUMBER
        ))

        for start_record in self.list_start:
            start_record.save()

        self.list_end = list()
        self.list_end.append(EndRecord(
            id=1, timestamp=END_TIME_1, start_id=70, cost=0.22
        ))
        self.list_end.append(EndRecord(
            id=2, timestamp=END_TIME_2, start_id=71, cost=0.22
        ))

        for self.end_record in self.list_end:
            self.end_record.save()

        self.valid_end_record = {
            'id': 1,
            'timestamp': str(END_TIME_1),
            'call_id': 70,
            'type': RecordType.END.value
        }

        self.invalid_end_record = {
            'id': 2,
            'timestamp': str(END_TIME_1),
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
    """ Test module for deleting an existing puppy record """

    def setUp(self):
        self.list_end = list()
        self.list_end.append(EndRecord(
            id=1, timestamp=END_TIME_1, start_id=70, cost=0.33
        ))
        self.list_end.append(EndRecord(
            id=2, timestamp=END_TIME_2, start_id=71, cost=0.44
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
    """ Test module for GET single end record """

    def setUp(self):

        # creates the list with call start records
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

        # creates the list with call end records
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
        response = client.get("/phonebill/?source=" +
                              SOURCE_NUMBER + "&period=12/2017")

        serializer_list = PhoneBillSerializer(self.bill_list, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data, serializer_list.data)

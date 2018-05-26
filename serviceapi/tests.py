# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
import json
import pdb

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

start_single_record = StartRecord(
    id=1, timestamp=datetime.datetime(2016, 2, 29, 12, 0, 0, 0, timezone.utc), call_id=70, source=SOURCE_NUMBER, destination=DESTINATION_NUMBER)

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


class GetAllEndRecordsTest(TestCase):

    def setUp(self):

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

    def test_get_valid_single_start_record(self):
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

    def test_valid_update_puppy(self):
        url = '/startrecord/' + str(self.valid_start_record['id']) + '/'
        response = client.put(
            url,
            data=json.dumps(self.valid_start_record),
            content_type='application/json'
        )
        pdb.set_trace()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_update_puppy(self):
        response = client.put(
            '/startrecord/' + str(self.invalid_start_record['id']) + '/',
            data=json.dumps(self.invalid_start_record),
            content_type='application/json')
        pdb.set_trace()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)







'''

class GetSingleStartRecordTest(TestCase):
    """ Test module for GET single start record API """

    def setUp(self):
        self.casper = Puppy.objects.create(
            name='Casper', age=3, breed='Bull Dog', color='Black')
        self.muffin = Puppy.objects.create(
            name='Muffin', age=1, breed='Gradane', color='Brown')
        self.rambo = Puppy.objects.create(
            name='Rambo', age=2, breed='Labrador', color='Black')
        self.ricky = Puppy.objects.create(
            name='Ricky', age=6, breed='Labrador', color='Brown')

    def test_get_valid_single_puppy(self):
        response = client.get(
            reverse('get_delete_update_puppy', kwargs={'pk': self.rambo.pk}))
        puppy = Puppy.objects.get(pk=self.rambo.pk)
        serializer = PuppySerializer(puppy)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_puppy(self):
        response = client.get(
            reverse('get_delete_update_puppy', kwargs={'pk': 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CreateNewPuppyTest(TestCase):
    """ Test module for inserting a new puppy """

    def setUp(self):
        self.valid_payload = {
            'name': 'Muffin',
            'age': 4,
            'breed': 'Pamerion',
            'color': 'White'
        }

        self.invalid_payload = {
            'name': '',
            'age': 4,
            'breed': 'Pamerion',
            'color': 'White'
        }

    def test_create_valid_puppy(self):
        response = client.post(
            reverse('get_post_puppies'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_puppy(self):
        response = client.post(
            reverse('get_post_puppies'),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UpdateSinglePuppyTest(TestCase):
    """ Test module for updating an existing puppy record """

    def setUp(self):
        self.casper = Puppy.objects.create(
            name='Casper', age=3, breed='Bull Dog', color='Black')
        self.muffin = Puppy.objects.create(
            name='Muffy', age=1, breed='Gradane', color='Brown')
        self.valid_payload = {
            'name': 'Muffy',
            'age': 2,
            'breed': 'Labrador',
            'color': 'Black'
        }

        self.invalid_payload = {
            'name': '',
            'age': 4,
            'breed': 'Pamerion',
            'color': 'White'
        }

    def test_valid_update_puppy(self):
        response = client.put(
            reverse('get_delete_update_puppy', kwargs={'pk': self.muffin.pk}),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_update_puppy(self):
        response = client.put(
            reverse('get_delete_update_puppy', kwargs={'pk': self.muffin.pk}),
            data=json.dumps(self.invalid_payload),
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DeleteSinglePuppyTest(TestCase):
    """ Test module for deleting an existing puppy record """

    def setUp(self):
        self.casper = Puppy.objects.create(
            name='Casper', age=3, breed='Bull Dog', color='Black')
        self.muffin = Puppy.objects.create(
            name='Muffy', age=1, breed='Gradane', color='Brown')

    def test_valid_delete_puppy(self):
        response = client.delete(
            reverse('get_delete_update_puppy', kwargs={'pk': self.muffin.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_delete_puppy(self):
        response = client.delete(
            reverse('get_delete_update_puppy', kwargs={'pk': 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)



'''
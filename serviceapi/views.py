from __future__ import unicode_literals

import json
import logging

from django.utils import timezone
from rest_framework.generics import ListAPIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status

from serviceapi.models import StartRecord, EndRecord
from serviceapi.serializers import PhoneBillSerializer, CallRecordSerializer
from serviceapi.utils import *
from phonebilling.settings import TIMESTAMP_FORMAT


class CallRecordViewSet(viewsets.ViewSet):

    serializer_class = CallRecordSerializer

    logger = logging.getLogger(__name__)

    def list(self, request):

        queryset_a = StartRecord.objects.all().order_by('-call_id')
        queryset_b = EndRecord.objects.all().order_by('-start')

        # Builds the response list
        results = list()
        for end_record in queryset_b:

            # Appends the REST fields to the result
            results.append({
                'id': end_record.id,
                'timestamp': end_record.timestamp.strftime(
                    TIMESTAMP_FORMAT
                ),
                'call_id': end_record.call_id,
                'type': RecordType.END.value
            })

        for start_record in queryset_a:

            # Appends the REST fields to the result
            results.append({
                'id': start_record.id,
                'timestamp': start_record.timestamp.strftime(
                    TIMESTAMP_FORMAT
                ),
                'call_id': start_record.call_id,
                'type': RecordType.START.value,
                'source': start_record.source,
                'destination': start_record.destination
            })

        self.logger.debug('list - results=' + json.dumps(results))

        return Response(results)

    def retrieve(self, request, pk):

        self.logger.debug('retrieve - pk=' + pk)

        queryset_a = StartRecord.objects.filter(id=pk).order_by('call_id')
        queryset_b = EndRecord.objects.filter(id=pk).order_by('start')

        # Builds the response list
        results = list()
        if (len(queryset_a) < 1 and len(queryset_b) < 1):
            return Response(results, status=status.HTTP_404_NOT_FOUND)

        for end_record in queryset_b:

            # Appends the REST fields to the result
            results.append({
                'id': end_record.id,
                'timestamp': end_record.timestamp.strftime(TIMESTAMP_FORMAT),
                'call_id': end_record.call_id,
                'type': RecordType.END.value
            })

        for start_record in queryset_a:

            results.append({
                'id': start_record.id,
                'timestamp': start_record.timestamp.strftime(
                    TIMESTAMP_FORMAT
                ),
                'call_id': start_record.call_id,
                'type': RecordType.START.value,
                'source': start_record.source,
                'destination': start_record.destination
            })

        self.logger.debug('retrieve - results=' + json.dumps(results))

        return Response(results)

    def create(self, request):

        self.logger.debug('create - request.data=' + json.dumps(request.data))

        serializer = CallRecordSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            self.logger.debug('create - response 201')
            self.logger.debug(
                'create - serializer.data %s response 201',
                serializer.data
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            self.logger.debug('create - response 400')
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

    def update(self, request, pk):

        self.logger.debug(
            'update - pk %s request.data=%s' % (pk, json.dumps(request.data))
        )

        serializer = CallRecordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            self.logger.debug(
                'update - serializer.data %s response 201',
                json.dumps(serializer.data)
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            self.logger.debug('update - response 400')
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

    def partial_update(self, request, pk):

        self.logger.debug(
            'partial_update - pk %s request.data=%s' %
            (pk, json.dumps(request.data))
        )

        serializer = CallRecordSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            self.logger.debug(
                'partial_update - serializer.data %s response 201',
                json.dumps(serializer.data)
            )
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            self.logger.debug('partial_update - response 400')
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

    def destroy(self, request, pk):

        queryset_a = StartRecord.objects.filter(id=pk)
        queryset_b = EndRecord.objects.filter(id=pk)
        if len(queryset_a) < 1 and len(queryset_b) < 1:
            self.logger.debug('partial_update - response 404')
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            # First, delete the end record because it depends on
            # the start record
            queryset_b.delete()
            queryset_a.delete()
            results = {}
            self.logger.debug(
                'partial_update - results %s response 204', json.dumps(results)
            )
            return Response(results, status=status.HTTP_204_NO_CONTENT)


class PhoneBillViewSet(viewsets.ViewSetMixin, ListAPIView):

    queryset = EndRecord.objects.all()
    serializer_class = PhoneBillSerializer

    logger = logging.getLogger(__name__)

    def list(self, request):
        ''' Returns the bill based on the parameters sent in the URL
        (source and period parameters, using HTTP GET method).
        If the period parameter (optional) is not present than the
        method uses the last month (of the request's day) as the period.
        '''

        source = self.request.query_params.get('source')
        period = self.request.query_params.get('period')

        self.logger.debug(
            'PhoneBillViewSet - source=%s, period=%s' % (source, period)
        )

        results = list()

        if source is None:
            results.append({
                'source': 'the field is necessary'
            })
            return Response(results, status=status.HTTP_400_BAD_REQUEST)

        if source.isdigit() is False:
            results.append({
                'source': 'the field must only contain digits'
            })
            return Response(results, status=status.HTTP_400_BAD_REQUEST)

        if len(source) != 10 and len(source) != 11:
            results.append({
                'source': 'the field must contain 10 or 11 digits'
            })
            return Response(results, status=status.HTTP_400_BAD_REQUEST)

        # If period was sent, validates the parameter
        # The period must have a slash between month and year
        # (format: mm/yyyy)
        if period is not None:

            if len(period) != len(BILL_PERIOD_MASK) or period[2] != '/':
                results.append({
                    'period':
                    'The period must have the following format: mm/yyyy'
                })
                return Response(results, status=status.HTTP_400_BAD_REQUEST)

            month_period = period[0:2]
            year_period = period[3:8]

            if month_period.isdigit() is False:
                results.append({
                    'month_period': "The month's period sent is not valid"
                })
                return Response(results, status=status.HTTP_400_BAD_REQUEST)

            if year_period.isdigit() is False:
                results.append({
                    'year_period':
                    "The year's period sent is not valid"
                })
                return Response(results, status=status.HTTP_400_BAD_REQUEST)

            start_period_date = datetime.datetime(
                int(year_period),
                int(month_period),
                1,  # days
                0,  # hours
                0,  # minutes
                0,  # seconds
                0,
                timezone.utc
            )
            end_period_date = add_one_month(start_period_date)

        else:
            end_period_date = datetime.datetime.now()
            end_period_date = end_period_date.replace(
                day=1,
                hour=0,
                minute=0,
                second=0
            )

            start_period_date = subtract_one_month(end_period_date)

        queryset = EndRecord.objects.select_related('start') \
            .filter(start__source=source) \
            .filter(start__timestamp__gte=start_period_date) \
            .filter(timestamp__lt=end_period_date) \
            .order_by('start__call_id')

        # Builds the response list
        results = list()
        for end_record in queryset:

            destination = end_record.start.destination

            record_start_time = end_record.start.timestamp
            record_end_time = end_record.timestamp
            delta = record_end_time - record_start_time
            h = delta.total_seconds() // 3600  # hours
            m = (delta.total_seconds() // 60) % 60  # minutes
            s = delta.total_seconds() % 60  # seconds
            duration = '%dh%02dm%02ds' % (h, m, s)

            formatted_price = ('R$ %0.2f' % end_record.cost). \
                replace('.', ',')

            # Appends the REST fields to the result
            results.append({
                'destination': destination,
                'start_date': record_start_time.strftime('%d/%m/%Y'),
                'start_time': record_start_time.strftime('%H:%M:%S'),
                'duration': duration,
                'price': formatted_price
            })

        self.logger.debug('PhoneBillViewSet - response=' + json.dumps(results))

        return Response(results, status=status.HTTP_200_OK)

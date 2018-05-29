# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils import timezone
from rest_framework.generics import ListAPIView
from rest_framework import viewsets

from serviceapi.models import StartRecord, EndRecord
from serviceapi.serializers import StartRecordSerializer, \
    EndRecordSerializer, PhoneBillSerializer
from serviceapi.utils import *


class StartRecordViewSet(viewsets.ModelViewSet):

    queryset = StartRecord.objects.all().order_by('-call_id')
    serializer_class = StartRecordSerializer


class EndRecordViewSet(viewsets.ModelViewSet):

    queryset = EndRecord.objects.all().order_by('-call_id')
    serializer_class = EndRecordSerializer


class PhoneBillViewSet(viewsets.ViewSetMixin, ListAPIView):

    queryset = EndRecord.objects.all()
    serializer_class = PhoneBillSerializer

    def get_queryset(self):
        ''' Returns the bill based on the parameters sent in the URL
        (source and period parameters, using HTTP GET method).
        If the period parameter (optional) is not present than the
        method uses the last month (of the request's day) as the period.
        '''

        source = self.request.query_params.get('source')
        period = self.request.query_params.get('period')

        results = {}

        pdb.set_trace()

        # Check if source is present, and if contains
        # 10 or 11 digits
        if source is None:
            results.append({
                'source': 'the field is necessary'
            })
            return results

        if source.is_digit() is False:
            results.append({
                'source': 'the field must only contain digits'
            })
            return results

        if len(source) != 10 and len(source) != 11:
            results.append({
                'source': 'the field must contain 10 or 11 digits'
            })
            return results

        # If period was sent, validates the parameter
        # The period must have a slash between month and year
        # (format: mm/yyyy)
        if period is not None:

            if len(period) != len(BILL_PERIOD_MASK) or period[2] != '/':
                results.append({
                    'period': PERIOD_FORMAT_ERROR
                })
                return results

            month_period = period[0:2]
            year_period = period[3:8]

            if month_period.isdigit() is False:
                results.append({
                    'month_period': MONTH_PERIOD_FORMAT_ERROR
                })
                return results

            if year_period.isdigit() is False:
                results.append({
                    'year_period': YEAR_PERIOD_FORMAT_ERROR
                })
                return results

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

        queryset = EndRecord.objects.select_related('call_id') \
            .filter(call_id__source=source) \
            .filter(call_id__timestamp__gte=start_period_date) \
            .filter(timestamp__lt=end_period_date) \
            .order_by('call_id_id')

        # Builds the response list
        results = list()
        for end_record in queryset:

            destination = end_record.call_id.destination

            record_start_time = end_record.call_id.timestamp
            record_end_time = end_record.timestamp
            delta = record_end_time - record_start_time
            h = delta.seconds / 3600  # hours
            m = delta.seconds / 60  # minutes
            s = delta.seconds % 60  # seconds
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

        return results

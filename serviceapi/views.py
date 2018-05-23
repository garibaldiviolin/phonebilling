# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from serviceapi.models import StartRecord, EndRecord
from rest_framework import viewsets
from serviceapi.serializers import *
from serviceapi.serializers import PhoneBillSerializer
from itertools import chain
from operator import attrgetter
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import detail_route
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView
from serviceapi.utils import *
import pdb


class StartRecordViewSet(viewsets.ModelViewSet):

    queryset = StartRecord.objects.all().order_by('-call_id')
    serializer_class = StartRecordSerializer

class EndRecordViewSet(viewsets.ModelViewSet):

    queryset = EndRecord.objects.all().order_by('-call_id')
    serializer_class = EndRecordSerializer

class PhoneBillViewSet(viewsets.ViewSetMixin, ListAPIView):

    serializer_class = PhoneBillSerializer
    queryset = RecordCost.objects.all()

    def get_queryset(self):

        source = self.request.query_params.get('source')
        period = self.request.query_params.get('period')

        results = {}

        if period is not None:

            if len(period) != len(BILL_PERIOD_MASK) or period[2] != '/':
                results.append({
                    'period': PERIOD_FORMAT_ERROR
                })
                return results

            month_period = period[0:2]
            year_period = period[3:8]

            if month_period.isdigit() == False:
                results.append({
                    'month_period': MONTH_PERIOD_FORMAT_ERROR
                })
                return results

            if year_period.isdigit() == False:
                results.append({
                    'year_period': YEAR_PERIOD_FORMAT_ERROR
                })
                return results

            start_period_date = datetime.datetime(
                int(year_period),
                int(month_period),
                1, # days
                0, # hours
                0, # minutes
                0, # seconds
                0,
                timezone.utc
            )
            #start_period_date = end_period_date + datetime.timedelta (month=1)
            end_period_date = start_period_date.replace(month=int(month_period)+1)

        else:
            end_period_date = datetime.now()
            end_period_date = period_date.replace(
                    day=1,
                    hour=0,
                    minute=0,
                    second=0)

            #start_period_date = end_period_date - datetime.timedelta (month=1)
            start_period_date = end_period_date.replace(month=int(month_period)-1)

        if source is not None:

            pdb.set_trace()

            queryset = RecordCost.objects.select_related('call_id__call_id') \
                .filter(call_id__call_id__source=source) \
                .filter(call_id__call_id__timestamp__gte=start_period_date) \
                .filter(call_id__timestamp__lt=end_period_date) \
                .order_by('call_id_id')

            results = list()
            for record_cost in queryset:

                destination = record_cost.call_id.call_id.destination

                record_start_time = record_cost.call_id.call_id.timestamp
                record_end_time = record_cost.call_id.timestamp
                delta = record_end_time - record_start_time
                h = delta.seconds / 3600  # hours
                m = delta.seconds / 60  # minutes
                s = delta.seconds % 60 # seconds
                duration = '%dh%02dm%02ds' % (h, m, s)

                formatted_price = ('R$ %0.2f' % record_cost.cost).replace('.',',')

                results.append({
                    'destination': destination,
                    'start_date': record_start_time.strftime('%d/%m/%Y'),
                    'start_time': record_start_time.strftime('%H:%M:%S'),
                    'duration': duration,
                    'price': formatted_price, 
                })
                return results

        return results

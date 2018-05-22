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
from serviceapi.utils import calculate_call_cost
import pdb


class StartRecordViewSet(viewsets.ModelViewSet):

    queryset = StartRecord.objects.all().order_by('-call_id')
    serializer_class = StartRecordSerializer


class EndRecordViewSet(viewsets.ModelViewSet):

    queryset = EndRecord.objects.all().order_by('-call_id')
    serializer_class = EndRecordSerializer

class PhoneBillViewSet(viewsets.ViewSetMixin, ListAPIView):

    serializer_class = PhoneBillSerializer
    paginate_by = 20
    queryset = RecordCost.objects.all()

    def get_queryset(self):

        source = self.request.query_params.get('source')
        period = self.request.query_params.get('period')

        results = {}

        if (source is not None) and (period is not None):

            #queryset_a = StartRecord.objects.filter(source=source)
            #queryset_b = EndRecord.objects.filter(call_id=queryset_a)

            pdb.set_trace()

            queryset = RecordCost.objects.select_related('call_id__call_id') \
                .filter(call_id__call_id__source=source) \
                .filter(call_id__call_id__timestamp=period)

            '''results_list = list(chain(queryset_a, queryset_b))

            sorted_list = sorted(results_list, key=lambda instance: -instance.call_id)

            results = list()
            for entry in sorted_list:
                item_type = entry.__class__.__name__.lower()
                if isinstance(entry, StartRecord):
                    serializer = StartRecordSerializer(entry)
                if isinstance(entry, EndRecord):
                    serializer = EndRecordSerializer(entry)

                results.append({'item_type': item_type, 'data': serializer.data})'''

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

                #pdb.set_trace()
                formatted_price = ('R$ %0.2f' % record_cost.cost).replace('.',',')

                #results.append({'item_type': item_type, 'data': serializer.data})
                results.append({
                    'destination': destination,
                    'start_date': record_start_time.strftime('%d/%m/%Y'),
                    'start_time': record_start_time.strftime('%H:%M:%S'),
                    'duration': duration,
                    'price': formatted_price, 
                })
                return results

        return results

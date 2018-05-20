# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from serviceapi.models import StartRecord, EndRecord
from rest_framework import viewsets
from serviceapi.serializers import *
from serviceapi.serializers import TwoPhoneBillSerializer
from itertools import chain
from operator import attrgetter
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import detail_route
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView
import pdb


class StartRecordViewSet(viewsets.ModelViewSet):

    queryset = StartRecord.objects.all().order_by('-call_id')
    serializer_class = StartRecordSerializer


class EndRecordViewSet(viewsets.ModelViewSet):

    queryset = EndRecord.objects.all().order_by('-call_id')
    serializer_class = EndRecordSerializer

class PhoneBillViewSetList(viewsets.ModelViewSet):
 
    #result_lst = list(chain(queryset1, queryset2))
    #queryset = EndRecord.objects.all().select_related('call_id')
    queryset = EndRecord.objects.all()
    serializer_class = PhoneBillSerializer

    def get(self, request, *args, **kwargs):
        pdb.set_trace()
        print "teste"
        return self.retrieve(request, *args, **kwargs)

class PhoneBillViewSet(viewsets.ModelViewSet):
 
    #result_lst = list(chain(queryset1, queryset2))
    #queryset = EndRecord.objects.all().select_related('call_id')
    queryset = EndRecord.objects.all()
    serializer_class = PhoneBillSerializer

    def get(self, request, *args, **kwargs):
        pdb.set_trace()
        print "teste"
        return self.retrieve(request, *args, **kwargs)


        serializer_class = EntrySerializer

    def get_queryset(self):
        pdb.set_trace()
        period = self.request.query_params.get('period')

        if period is not None:
            if period == 'last': # for last entry
               queryset = Entry.objects.last()
            elif period == 'week':
                print '2' 
                # queryset for week
            elif period == 'month':
                print '2'
                # queryset for month
        return queryset

class PhoneBillViewSet3(ListAPIView):

    serializer_class = TwoPhoneBillSerializer
    paginate_by = 20
    queryset = EndRecord.objects.all()

    def get_queryset(self):

        source = self.request.query_params.get('source')
        period = self.request.query_params.get('period')

        results = EndRecord.objects.all()

        if source is not None and period is not None:

            #queryset_a = StartRecord.objects.filter(source=source)
            #queryset_b = EndRecord.objects.filter(call_id=queryset_a)

            queryset = EndRecord.objects.select_related('call_id').filter(call_id__source=source)

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
            for end_record in queryset:

                destination = end_record.call_id.destination

                record_start_time = end_record.call_id.timestamp
                record_end_time = end_record.timestamp
                delta = record_end_time - record_start_time
                h = delta.seconds / 3600  # hours
                m = delta.seconds / 60  # minutes
                duration = '%dh%dm%ds' % (h, m, delta.seconds)

                #results.append({'item_type': item_type, 'data': serializer.data})
                results.append({
                    'destination': destination,
                    'start_date': record_start_time.strftime('%d/%m/%Y'),
                    'start_time': record_start_time.strftime('%H:%M:%S'),
                    'duration': duration,
                    'price': 'R$ 2,90'
                })

        return results


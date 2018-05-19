# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from serviceapi.models import StartRecord, EndRecord
from rest_framework import viewsets
from serviceapi.serializers import *
from itertools import chain
from operator import attrgetter


class StartRecordViewSet(viewsets.ModelViewSet):

    queryset = StartRecord.objects.all().order_by('-call_id')
    serializer_class = StartRecordSerializer


class EndRecordViewSet(viewsets.ModelViewSet):

    queryset = EndRecord.objects.all().order_by('-call_id')
    serializer_class = EndRecordSerializer

class PhoneBillViewSet(viewsets.ModelViewSet):
 
    #result_lst = list(chain(queryset1, queryset2))

    startrecord = StartRecordViewSet(read_only=True)
    #queryset = StartRecord.objects.all()
    serializer_class = PhoneBillSerializer
    http_method_names = ['get', 'head']

    """def get_queryset(self):
        queryset_a = StartRecord.objects.all()
        queryset_b = StartRecord.objects.all()
        source = self.request.query_params.get('startrecord.source', None)
        if source is not None:
            queryset = queryset.filter(source=source)

        return queryset"""



    def get_queryset(self):

        queryset_a = StartRecord.objects.all()
        queryset_b = StartRecord.objects.all()

        # Create an iterator for the querysets and turn it into a list.
        results_list = list(chain(queryset_a, queryset_b))

        source = self.request.query_params.get('startrecord.source', None)
        if source is not None:
            #queryset = queryset.filter(source=source)
            # Optionally filter based on date, score, etc.
            sorted_list = sorted(results_list, key=lambda instance: -instance.source)
            return sorted_list

        return results_list

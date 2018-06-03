# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
from enum import Enum

from phonebilling.settings import TIMESTAMP_FORMAT

PERIOD_FORMAT_ERROR = "The period must have the following format: mm/yyyy"
MONTH_PERIOD_FORMAT_ERROR = "The month's period sent is not valid"
YEAR_PERIOD_FORMAT_ERROR = "The year's period sent is not valid"

BILL_PERIOD_MASK = '99/9999'

STANDING_CALL_CHARGE = 0.36
STANDARD_MINUTE_CALL_CHARGE = 0.09

FREE_PERIOD_START_HOUR = 22
FREE_PERIOD_START_MINUTE = 0
FREE_PERIOD_START_SECOND = 0

FREE_PERIOD_END_HOUR = 6
FREE_PERIOD_END_MINUTE = 0
FREE_PERIOD_END_SECOND = 0

BASE_PERIOD = 60  # currently, the base period is 1 minute (60 seconds)
PERIOD_COST = 0.09  # currently, the base period cost is R$ 0,09


class RecordType(Enum):
    START = 1
    END = 2


def subtract_one_month(date):
    dt1 = date.replace(day=1)
    dt2 = dt1 - datetime.timedelta(days=1)
    dt3 = dt2.replace(day=1)
    return dt3


def add_one_month(date):
    dt1 = date + datetime.timedelta(days=31)
    dt2 = dt1.replace(day=1)
    return dt2


def calculate_call_cost(start_time, end_time):
    ''' This function calculates the phone call's cost, based on the
    start_time end_time parameters (both are datetime.datetime types)
    The idea is to use a auxiliar variable (aux_time) to go from start_time
    to end_time, and sum each period's cost (using the current value of
    BASE_PERIOD and PERIOD_COST)
    '''

    aux_time = start_time

    # initial charge
    call_cost = STANDING_CALL_CHARGE

    while aux_time < end_time:

        delta_left_time = end_time - aux_time
        delta_seconds = delta_left_time.seconds

        free_period_start = aux_time.replace(
            hour=FREE_PERIOD_START_HOUR,
            minute=FREE_PERIOD_START_MINUTE,
            second=FREE_PERIOD_START_SECOND
        )
        free_period_end = aux_time.replace(
            hour=FREE_PERIOD_END_HOUR,
            minute=FREE_PERIOD_END_MINUTE,
            second=FREE_PERIOD_END_SECOND
        )

        if aux_time > free_period_end:
            free_period_end = free_period_end \
                + datetime.timedelta(days=1)

        # if the left period has less than BASE_PERIOD, than the function can
        # return because these period isn't charged
        if (delta_seconds / BASE_PERIOD) < 1:
            return call_cost

        condition_a = aux_time.hour >= FREE_PERIOD_END_HOUR
        condition_b = aux_time.hour < FREE_PERIOD_START_HOUR

        # if aux_time is in the period that charges per minute, then
        # calculate the cost using BASE_PERIOD and PERIOD_COST
        if condition_a and condition_b:
            delta_charge_time = free_period_start - aux_time
            if (delta_charge_time >= delta_left_time):
                aux_seconds = delta_seconds
            else:
                aux_seconds = delta_charge_time.seconds
            call_cost += (aux_seconds // BASE_PERIOD) * PERIOD_COST
        else:  # don't charge
            delta_free_time = free_period_end - aux_time
            if (delta_free_time >= delta_left_time):
                aux_seconds = delta_seconds
            else:
                aux_seconds = delta_free_time.seconds

        aux_time = aux_time + datetime.timedelta(seconds=aux_seconds)

    return call_cost


def validate_datetime(date_text):
    try:
        datetime.datetime.strptime(date_text, TIMESTAMP_FORMAT)
        value = True
    except ValueError:
        value = False

    return value

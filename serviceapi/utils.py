# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
from django.utils import timezone
import pdb

PERIOD_FORMAT_ERROR = "The period must have the following format: mm/yyyy"
MONTH_PERIOD_FORMAT_ERROR = "The month's period sent is not valid"
YEAR_PERIOD_FORMAT_ERROR = "The year's period sent is not valid"

BILL_PERIOD_MASK = '99/9999'

STANDING_CALL_CHARGE = 0.36
STANDARD_MINUTE_CALL_CHARGE = 0.09

NO_COST_PERIOD_START_HOUR = 22
NO_COST_PERIOD_START_MINUTE = 0
NO_COST_PERIOD_START_SECOND = 0

NO_COST_PERIOD_END_HOUR = 5
NO_COST_PERIOD_END_MINUTE = 59
NO_COST_PERIOD_END_SECOND = 59

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

    aux_time = start_time

    # initial charge
    call_cost = STANDING_CALL_CHARGE

    while aux_time < end_time:

        delta_left_time = end_time - aux_time

        no_cost_period_start = aux_time.replace(hour=NO_COST_PERIOD_START_HOUR,
                minute=NO_COST_PERIOD_START_MINUTE,
                second=NO_COST_PERIOD_START_SECOND)
        no_cost_period_end = aux_time.replace(hour=NO_COST_PERIOD_END_HOUR,
                minute=NO_COST_PERIOD_END_MINUTE,
                second=NO_COST_PERIOD_END_SECOND) \
                + datetime.timedelta(days=1)

        if (delta_left_time.seconds / 60) < 1:
            return call_cost

        condition_a = aux_time.hour >= 6
        condition_b = aux_time.hour < 22

        # charge for the time
        if condition_a and condition_b:
            delta_charge_time = no_cost_period_start - aux_time
            if (delta_charge_time >= delta_left_time):
                charge_seconds = delta_left_time.seconds
            else:
                charge_seconds = delta_charge_time.seconds
            call_cost += (charge_seconds / 60) * 0.09
        # don't charge
        else:
            delta_charge_time = no_cost_period_end - aux_time
            if (delta_charge_time >= delta_left_time):
                charge_seconds = delta_left_time.seconds
            else:
                delta_charge_time
        aux_time = aux_time + datetime.timedelta(seconds=charge_seconds)

    return call_cost

def old_calculate_call_cost(start_time, end_time):

    aux_time = start_time

    # initial charge
    call_cost = STANDING_CALL_CHARGE

    while aux_time < end_time:

        delta_time = end_time - aux_time

        no_cost_period_start = aux_time.replace(hour=NO_COST_PERIOD_START_HOUR,
                minute=NO_COST_PERIOD_START_MINUTE,
                second=NO_COST_PERIOD_START_SECOND)
        no_cost_period_end = aux_time.replace(hour=NO_COST_PERIOD_END_HOUR,
                minute=NO_COST_PERIOD_END_MINUTE,
                second=NO_COST_PERIOD_END_SECOND)

        # check if duration is greater or equan than 1 minute
        if (delta_time.seconds / 60) >= 1:

            condition_a = aux_time + datetime.timedelta(seconds=60) < \
                no_cost_period_start
            condition_b = aux_time + datetime.timedelta(seconds=60) > \
                no_cost_period_end
            if condition_a and condition_b:
                call_cost += STANDARD_MINUTE_CALL_CHARGE
                if start_time == datetime.datetime(2017, 12, 12, 4, 57, 13, 0, timezone.utc):
                    print('aux_time' + aux_time.strftime("%Y-%m-%d %H:%M:%S"))
                    print('call_cost=%0.2f' % (call_cost,))
                    pdb.set_trace()

        aux_time = aux_time + datetime.timedelta(seconds=60)

    return call_cost

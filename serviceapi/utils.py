# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

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

def calculate_call_cost(start_time, end_time):

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

        # check if duration is greater than 1 hour
        if (delta_time.seconds / 60) >= 1:

            condition_a = aux_time + datetime.timedelta(seconds=60) < \
                no_cost_period_start
            condition_b = aux_time + datetime.timedelta(seconds=60) > \
                no_cost_period_end
            if condition_a and condition_b:
                call_cost += STANDARD_MINUTE_CALL_CHARGE

        aux_time = aux_time + datetime.timedelta(seconds=60)

    return call_cost

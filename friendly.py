#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
human friendly functions
'''

import re
import datetime

from .fmt import *

WEEKS = '(?P<weeks>[0-9]+w)?'
DAYS = '(?P<days>[0-9]+d)?'
HOURS = '(?P<hours>[0-9]+h)?'
MINUTES = '(?P<minutes>[0-9]+m)?'
SECONDS = '(?P<seconds>[0-9]+s)?'
REGEX = re.compile(WEEKS+DAYS+HOURS+MINUTES+SECONDS)

class FriendlyTimedeltaParseError(Exception):
    def __init__(self, string):
        msg = 'friendly.timedelta parse error for string: ' + string

def timedelta(string):
    try:
        match = REGEX.match(string)
        if not match:
            raise FriendlyTimedeltaParseError(string)
        kwargs = {k:int(v[:-1]) for k,v in match.groupdict().items() if v != None}
        return datetime.timedelta(**kwargs)
    except:
        import traceback
        traceback.print_exc()


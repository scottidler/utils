#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

from .git import describe
from .shell import cd
from .fmt import fmt, pfmt, dbg

def get_version(path='.'):
    try:
        try:
            with cd(path):
                value = open('VERSION').read().strip()
        except:
            value = describe()
    except:
        value ='UNKNOWN'
    parts = value.split('-')
    return parts[0].replace('v', '') + '.dev{0}+{1}'.format(*parts[1:]) if parts[1:] else ''

class Version(str):
    __instance = None
    def __new__(cls):
        if Version.__instance is None:
            value = get_version()
            Version.__instance = super(Version, cls).__new__(cls, value)
        return Version.__instance

version = Version()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

from .git import reporoot, describe

def get_version():
    try:
        try:
            value = open(os.path.join(reporoot(), 'VERSION')).read().strip()
            return value
        except:
            value = describe()
    except:
        value ='UNKNOWN'
    version, *suffix = value.split('-')
    return version.replace('v', '') + '.dev{0}+{1}'.format(*suffix) if suffix else ''

class Version(str):
    __instance = None
    def __new__(cls):
        if Version.__instance is None:
            value = get_version()
            Version.__instance = super(Version, cls).__new__(cls, value)
        return Version.__instance

version = Version()

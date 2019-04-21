#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from enum import Enum
from fnmatch import fnmatch

from utils.dbg import dbg

class MatchType(Enum):
    GLOB = 0
    PREFIX = 1
    SUFFIX = 2
    REGEX = 3

class InvalidFuzzyTypeError(Exception):
    def __init__(obj):
        message = f'type(obj)={type(obj)} is not dict or list'
        super(InvalidFuzzyTypeError, self).__init__(message)

MATCH_FUNCS = {
    MatchType.PREFIX: lambda item, pattern: fnmatch(item, pattern+'*'),
    MatchType.SUFFIX: lambda item, pattern: fnmatch(item, '*'+pattern),
    MatchType.GLOB: lambda item, pattern: fnmatch(item, pattern),
    MatchType.REGEX: lambda item, pattern: re.search(item, pattern),
}

def match_item(item, patterns, match_type, include):
    match_func = MATCH_FUNCS[match_type]
    if include:
        return any([match_func(item, pattern) for pattern in patterns])
    return all([not match_func(item, pattern) for pattern in patterns])

def match_items(items, patterns, match_type=MatchType.GLOB, include=True):
    return [item for item in items if match_item(item, patterns, match_type, include)]


class FuzzyList(list):
    def __init__(self, *args, **kwargs):
        self._match_type = kwargs.pop('match_type', MatchType.GLOB)
        super(FuzzyList, self).__init__(*args, **kwargs)
    def include(self, *patterns, match_type=None):
        items = match_items([item for item in self.__iter__()], patterns, match_type or self._match_type, include=True)
        return FuzzyList(items)
    def exclude(self, *patterns, match_type=None):
        items = match_items([item for item in self.__iter__()], patterns, match_type or self._match_type, include=False)
        return FuzzyList(items)

class FuzzyDict(dict):
    def __init__(self, *args, **kwargs):
        self._match_type = kwargs.pop('match_type', MatchType.GLOB)
        super(FuzzyDict, self).__init__(*args, **kwargs)
    def include(self, *patterns, match_type=None):
        items = match_items(self.keys(), patterns, match_type or self._match_type, include=True)
        return FuzzyDict({item: self.get(item) for item in items})
    def exclude(self, *patterns, match_type=None):
        items = match_items(self.keys(), patterns, match_type or self._match_type, include=False)
        return FuzzyDict({item: self.get(item) for item in items})

def fuzzy(obj):
    if isinstance(obj, dict):
        return FuzzyDict(obj)
    elif isinstance(obj, list):
        return FuzzyList(obj)
    raise InvalidFuzzyTypeError(obj)


if __name__ == '__main__':
    f = fuzzy(['a', 'b'])
    print(f'f={f.items}')

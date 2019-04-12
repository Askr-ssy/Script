# -*-coding:utf-8-*-
from __future__ import division,unicode_literals

import re
import sys
import hashlib
import collections
import numbers

from itertools import groupby

if sys.version_info[0]>=3:
    basestring=str
    unicode=str
    long=int
else:
    basestring=bytes
    unicode=unicode
    long=long
    range=xrange

class VSM(object):
    def __init__(self,value=None):
        self.weight={}
        self.vector=[]

        if isinstance(value,VSM):
            self.value=value.value
        elif isinstance(value,basestring):
            self.build_vector_by_content(unicode(value))
        elif isinstance(value,collections.Iterable):
            self.build_hash_by_features(value)
        elif isinstance(value,numbers.Integral):
            self.value=value
        else:
            raise Exception('Bad parameter with type {}'.format(type(value)))        
    def build_vector_by_content(self,lcontent):
        self.weight={k:sum(1 for _ in g) for k,g in groupby(sorted(lcontent))}
        self.
    def lcut(self,content):
        self.vector=jieba.lcut(content)

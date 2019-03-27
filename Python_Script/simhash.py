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

def _hashfunc(x):
    return int(hashlib.md5(x).hexdigest(),16)

class Simhash(object):
    __slots__=['value','f','reg','hashfunc']

    def __init__(self,value,f=64,reg=r'[\w\u4e00-\u9fcc]+',hashfunc=None):
        self.f=f
        self.reg=reg
        self.value=None

        if hashfunc:
            self.hashfunc=hashfunc
        else:
            self.hashfunc=_hashfunc 
        
        if isinstance(value,Simhash):
            self.value=value.value
        elif isinstance(value,basestring):
            self.build_weight_by_text(unicode(value))
        elif isinstance(value,collections.Iterable):
            self.build_hash_by_features(value)
        elif isinstance(value,numbers.Integral):
            self.value=value
        else:
            raise Exception('Bad parameter with type {}'.format(type(value)))
        
    def __eq__(self,other):
        return self.value==other.value
    
    def _side(self,content,width=2):
        return [content[i:i+width] for i in range(max(len(content)-width+1,1))]

    def _tokenize(self,content):
        content=content.lower()
        content=''.join(re.findall(self.reg,content))
        ans=self._side(content)
        return ans
    
    def build_weight_by_text(self,content):
        features=self._tokenize(content)
        features={k:sum(1 for _ in g) for k,g in groupby(sorted(features))}
        return self.build_hash_by_features(features)
    
    def build_hash_by_features(self,features):
        v=[0]*self.f
        maskes=[1<<i for i in range(self.f)]

        if isinstance(features,dict):
            features=features.items()
        for f in features:
            assert isinstance(f,collections.Iterable)
            h=self.hashfunc(f[0].encode('utf-8'))
            w=f[1]
        for i in range(self.f):
            v[i]+= w if h & maskes[i] else -w
        ans =0
        for i in range(self.f):
            if v[i]>0:
                ans |=maskes[i]
        self.value =ans

    def distance(self,another):
        assert self.f==another.f 
        x=(self.value^another.value) &((1<<self.f)-1)
        ans =0 
        while x:
            ans +=1
            x &=x-1
        return ans


        
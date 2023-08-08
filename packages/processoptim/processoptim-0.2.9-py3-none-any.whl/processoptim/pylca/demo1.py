# -*- coding: utf-8 -*-
"""
Created on Wed Aug  2 10:03:53 2023

@author: Hedi
"""

from numpy import load
from tabulate import tabulate

class __lci__(object):
    def __init__(self, dict_):
        self.__dict__.update(dict_)

class __method__(object):
    def __init__(self, dict_):
        self.__dict__.update(dict_)
    def __repr__(self):
        table = []
        for c in self.categories:
            table.append([c.name,c.unit])
        return tabulate(table,headers=[self.name,""],showindex="always")
    
class __category__(object):
    def __init__(self,dict_):
        self.__dict__.update(dict_)
    def __repr__(self):
        table = []
        for f in self.impactFactors.values():
            table.append([f.name,f.value,f.unit])
        return tabulate(table,headers=[self.name,"",""],showindex="always")
    
class __impact_factor__(object):
    def __init__(self,dict_):
        self.__dict__.update(dict_)

mix = load("lci\\electricity, high voltage.npy",allow_pickle=True)
cml = load("methods\\cml.npy",allow_pickle=True)


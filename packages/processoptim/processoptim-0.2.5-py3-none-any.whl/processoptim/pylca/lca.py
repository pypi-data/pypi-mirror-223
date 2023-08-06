# -*- coding: utf-8 -*-
"""
Created on Wed Aug  2 12:29:53 2023

@author: Hedi
"""
import json
import glob
import os
from tabulate import tabulate
import warnings
import inspect

script_directory = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))


class __exchange__(object):
    def __init__(self,dict_):
        self.__dict__.update(dict_)
class __lci__(object):
     def __init__(self, dict_):
         self.exchanges={}
         for k,v in dict_.items():
             if k=="exchanges":
                 for k1,v1 in dict_["exchanges"].items():
                     self.exchanges[k1]= __exchange__(v1)
             else:
                 setattr(self, k, v)
     def __repr__(self):
         return tabulate([[self.name, self.amount, self.unit]],headers=["Inventory","Amount","Unit"])
         

class inventories(dict):
    def __init__(self):
        self.load()
        
    def load(self):
        self.clear()
        inv_=[]
        for fname in glob.glob(script_directory+"\\lci\\*.json"):
            inv_.append(json.load(open(fname)))
        for inv in sorted(inv_,key=lambda x:x["name"]):
            self[inv["id"]]=__lci__(inv)
    def __repr__(self):
        from .uiinv import InvApp
        app = InvApp(self)
        app.MainLoop()
        return ""
        # table = []
        # for inv in self.values():
        #     table.append([inv.name, inv.amount, inv.unit])
        # return tabulate(table,showindex="always", headers=["","Inventory","Amount","Unit"],colalign=("right",))
    def __getitem__(self, k):
            if isinstance(k, int):
                k=list(self.keys())[k]
            return self.get(k)

class impactFactor:
    def __init__(self,dict_):
        self.__dict__.update(dict_)
class category:
    def __init__(self,dict_):
        self.impactFactors={}
        for k,v in dict_.items():
            if k=="impactFactors":
                for k1,v1 in v.items():
                    self.impactFactors[k1]=impactFactor(v1)
            else:
                setattr(self, k, v)
    def __repr__(self):
        return tabulate(map(lambda x: [x.name,x.value, x.unit],self.impactFactors.values()),headers=[self.name,"",""])
                
class categories(dict):
    def __init__(self, dict_):
        for c in dict_:
            cat = category(c)
            self[cat.name] = cat
    def __getitem__(self, k):
            if isinstance(k, int):
                k=list(self.keys())[k]
            return self.get(k)
class method:
    def __init__(self,dict_):
        for k,v in dict_.items():
            if k == "categories":
                self.categories = categories(v)
            else:
                setattr(self, k, v)
    def __repr__(self):
        return tabulate(map(lambda x:[x.name,x.unit],self.categories.values()),headers=[self.name,""],showindex="always")
    def __getitem__(self, k):
            if k in self.__dict__:
                return self.get(k)
            else:
                return self.categories[k]

        
class methods(dict):
    def __init__(self):
        for fname in glob.glob(script_directory+"\\methods\\*.json"):
            m = method(json.load(open(fname)))
            self[m.name] = m
    def __repr__(self):
        return tabulate(map(lambda x: [x.name],self.values()),showindex="always")
    def __getitem__(self, k):
            if isinstance(k, int):
                k=list(self.keys())[k]
            return self.get(k)
    
class res(dict):
    def __init__(self, lca):
        self.lca=lca
        self.__cumul__ = {}
    
    def cumul(self, cat):
        cat = self.lca.methods[self.lca.method][cat]
        if cat:
            return self.__cumul__[cat.name]
    def __repr__(self):
        table =[]
        for inv, v in self.items():
            table.append([self.lca.inventories[inv].name,"",v["amount"],self.lca.inventories[inv].unit])
            for k1,v1 in v["impacts"].items():
                table.append(["",k1,"{:.3e}".format(v1),self.lca.methods[self.lca.method][k1].unit])
        table.append(["Cumul","",""])
        for k,v in self.__cumul__.items():
            table.append(["",k,"{:.3e}".format(v)])
        return tabulate(table,colalign=("right",))
class lca:
    def __init__(self):
        self.inventories = inventories()
        self.methods=methods()
        self.__inv__ = {}
        self.method = 0
        self.categories=[]
        self.res=res(self)
    def loadLCI(self):
        from .uiinv import InLoadInv
        InLoadInv(self)
    def clear(self):
        self.__inv__ = {}
        self.res=res(self)
    def add(self, amount, inv):
        #if isinstance(inv, int) and inv <len(self.inventories):
        inv_ = next((x for x in self.inventories.items() if x[1].name == inv),None)
        if inv_:
            self.__inv__[inv_[0]]=amount
            pass
        else:
            warnings.warn("inventory {} does not exist".format(inv))
    def __repr__(self):
        table = []
        for k,v in self.__inv__.items():
            table.append([k,v,self.inventories[k].unit])
        return tabulate(table)
    def __calcul__(self,amount, inv,cat):
        impact=0
        for k,v in self.methods[self.method].categories[cat].impactFactors.items():
            if k in self.inventories[inv].exchanges.keys():
                impact+=self.inventories[inv].exchanges[k].amount*v.value
        return impact*amount/self.inventories[inv].amount
    def calcul(self):
        self.res=res(self)
        m = self.methods[self.method]
        cat_ = self.categories
        if not cat_:
            cat_ = range(len(m.categories))
        for inv,amount in self.__inv__.items():
            self.res[inv]={"amount":amount,"impacts":{}}
            for cat in cat_:
                cat = m[cat].name
                self.res[inv]["impacts"][cat]=self.__calcul__(amount, inv, cat)
                if not cat in self.res.__cumul__.keys():
                    self.res.__cumul__[cat]=0
                self.res.__cumul__[cat]+=self.res[inv]["impacts"][cat]


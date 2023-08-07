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
from ..__colors__ import __colors__
from ..__disp__ import _set_color, _set_decimals

script_directory = os.path.dirname(
    os.path.abspath(inspect.getfile(inspect.currentframe())))



class __exchange__(object):
    def __init__(self, dict_):
        self.__dict__.update(dict_)


class __lci__(object):
    def __init__(self, dict_):
        self.exchanges = {}
        for k, v in dict_.items():
            if k == "exchanges":
                for k1, v1 in dict_["exchanges"].items():
                    self.exchanges[k1] = __exchange__(v1)
            else:
                setattr(self, k, v)

    def __repr__(self):
        return tabulate([[self.name, self.amount, self.unit]], headers=["Inventory", "Amount", "Unit"])


class inventories(dict):
    def __init__(self,lca):
        self.lca = lca
        self.load()

    def load(self):
        self.clear()
        inv_ = []
        for fname in glob.glob(script_directory+"\\lci\\*.json"):
            inv_.append(json.load(open(fname)))
        for inv in sorted(inv_, key=lambda x: x["name"]):
            self[inv["id"]] = __lci__(inv)

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
        if isinstance(k, int) and k < len(self):
            return self.get(list(self.keys())[k])
        else:
            return self.get(next((x for x in self.items() if x[1].name == k or x[0] == k), (None,))[0])
        return None

    def search(self, *args):
        list_ = []
        table =[]
        for k,v in self.items():
            if all([x in v.name for x in args]):
                list_.append(k)
                table.append([self.lca.getInventoryLabel(k), v.amount, v.unit])
        if list_:
            print(tabulate(table))
        return list_;


class impactFactor:
    def __init__(self, dict_):
        self.__dict__.update(dict_)


class category:
    def __init__(self, dict_):
        self.impactFactors = {}
        for k, v in dict_.items():
            if k == "impactFactors":
                for k1, v1 in v.items():
                    self.impactFactors[k1] = impactFactor(v1)
            else:
                setattr(self, k, v)

    def __repr__(self):
        return tabulate(map(lambda x: [x.name, x.value, x.unit], self.impactFactors.values()), headers=[self.name, "", ""])


class categories(dict):
    def __init__(self, dict_):
        for c in dict_:
            cat = category(c)
            self[cat.name] = cat

    def __getitem__(self, k):
        if isinstance(k, int):
            k = list(self.keys())[k]
        return self.get(k)


class method:
    def __init__(self, dict_):
        for k, v in dict_.items():
            if k == "categories":
                self.categories = categories(v)
            else:
                setattr(self, k, v)

    def __repr__(self):
        return tabulate(map(lambda x: [x.name, x.unit], self.categories.values()), headers=[self.name, ""], showindex="always")

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
        return tabulate(map(lambda x: [x.name], self.values()), showindex="always")

    def __getitem__(self, k):
        if isinstance(k, int):
            k = list(self.keys())[k]
        return self.get(k)


class res(dict):
    def __init__(self, lca):
        self.lca = lca
        self.__cumul__ = {}

    def cumul(self, cat=None):
        cat = self.lca.methods[self.lca.method][cat]
        if cat:
            return self.__cumul__[cat.name]
        else:
            table=[]
            for k, v in self.__cumul__.items():
                table.append([k, "{:.3e}".format(v),self.lca.methods[self.lca.method][k].unit])
            return print(tabulate(table))

    def __repr__(self):
        table = []
        for inv, v in self.items():
            table.append([self.lca.getInventoryLabel(inv), "",
                         v["amount"], self.lca.inventories[inv].unit])
            for k1, v1 in v["impacts"].items():
                table.append(["", k1, "{:.3e}".format(
                    v1), self.lca.methods[self.lca.method][k1].unit])
        return tabulate(table, colalign=("right",))


class productSystem(dict):
    def __init__(self, lca, name):
        self.lca = lca
        self.res=res(self.lca)
        self.name=name

    def add(self, amount, inventory):
        inv = self.lca.inventories[inventory]
        if inv:
            self[inv.id]=amount
        else:
            warnings.warn("inventory {} does not exist".format(inventory))
            
    def remove(self, inventory):
        self.pop(inventory,None)
    def __repr__(self):
        table = []
        for k, v in self.items():
            table.append([self.lca.getInventoryLabel(k), v, self.lca.inventories[k].unit])
        return tabulate(table)
    
    def calcul(self):
        self.res = res(self.lca)
        m = self.lca.methods[self.lca.method]
        cat_ = self.lca.categories
        if not cat_:
            cat_ = range(len(m.categories))
        for inv, amount in self.items():
            self.res[inv] = {"amount": amount, "impacts": {}}
            for cat in cat_:
                cat = m[cat].name
                self.res[inv]["impacts"][cat] = self.lca.__calcul__(amount, inv, cat)
                if not cat in self.res.__cumul__.keys():
                    self.res.__cumul__[cat] = 0
                self.res.__cumul__[cat] += self.res[inv]["impacts"][cat]

    
class lca():
    def __init__(self):
        self.inventories = inventories(self)
        self.methods = methods()
        self.method = 0
        self.categories = []
        self.__product_systems = {}

    def loadLCI(self):
        from .uiinv import InLoadInv
        InLoadInv(self)

    def clear(self,reload=False):
        self.__product_systems.clear()
    
    def get(self, productSystemName):
        return self.__product_systems.get(productSystemName)

    def add(self, productSystemName):
        self.__product_systems[productSystemName]=productSystem(self,productSystemName)
        return self.__product_systems[productSystemName]

    def __repr__(self):
        table = []
        for k, v in self.__product_systems.items():
            table.append([k])
        return tabulate(table)

    def __calcul__(self, amount, inv, cat):
        impact = 0
        for k, v in self.methods[self.method].categories[cat].impactFactors.items():
            if k in self.inventories[inv].exchanges.keys():
                impact += self.inventories[inv].exchanges[k].amount*v.value
        return impact*amount/self.inventories[inv].amount
    
    def calcul(self,*args):
        if len(args)==0:
            args = self.__product_systems.keys()
        for arg in args:
            self.__product_systems[arg].calcul()
    
    def getImpact(self,cat):
        table=[]
        for k,v in self.__product_systems.items():
            table.append([k,v.res.cumul(cat)])
        print(tabulate(table,headers=[self.methods[self.method][cat].name,self.methods[self.method][cat].unit]))
        
            
    def getInventoryLabel(self,inventoryID):
                idx = _set_color(str([idx for idx, key in enumerate(self.inventories.items()) if key[0] == inventoryID]),__colors__.on_yellow)
                name = self.inventories[inventoryID].name
                if len(name)>60:
                    name = name[0:60]+_set_color("...",__colors__.bgreen)
                return (" ").join((idx,name))




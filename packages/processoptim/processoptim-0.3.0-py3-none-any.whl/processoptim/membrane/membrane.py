# -*- coding: utf-8 -*-
"""
Created on Wed Oct 26 19:25:38 2022

@author: Hedi
"""

import CoolProp.CoolProp as CP
from numpy import zeros, array, ones, pi,concatenate,cumsum,inf
import json
import os
from scipy.optimize import fsolve, fminbound,least_squares,broyden1
from scipy.integrate import cumtrapz

from numpy import pi,log,exp,linspace,log10
from ..__disp__ import _set_color, _set_decimals
from ..__colors__ import __colors__
from tabulate import tabulate
import warnings
import time

def getfield(obj,field,default):
    if hasattr(obj,field):
        return getattr(obj,field)
    else:
        return default
def getvalue(val,schema=None):
    if is_number(val):
        scientific_notation = getfield(schema, "scientific_notation", False)
        decimals = getfield(schema, "decimals", 0)
        val = _set_decimals(val, str(decimals),scientific_notation)
    return val
def is_number(s):
    try:
        float(s) # for int, long and float
    except ValueError:
            return False
    return True

class _schema_obj:
    def __init__(self, dict_):
            self.__dict__.update(dict_)
def load_json(fname):
    return json.loads(json.dumps(json.
                                 loads(open (os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                 fname+".json"), "r").read()),), object_hook=_schema_obj,)
_schema = load_json("membrane")

class obj:
    def __init__(self):
        for k,v in self.schema.__dict__.items():
                setattr(self,k,v.default)    
    @property
    def type(self):
        return type(self).__name__
    @property
    def schema(self):
        return getattr(_schema,self.type)
    def formatted_val(self,key):
        val = getattr(self,key)
        schema = getattr(self.schema,key)
        if hasattr(schema,"list"):
            val = list(map(lambda x: getvalue(getattr(eval(schema.list.eval)[x],schema.list.key),schema),val))
        elif hasattr(val, '__iter__') and not isinstance(val,str):
            val=list(map(lambda x: getvalue(x,schema),val))
            if val and is_number(val[0]):
                def num(s):
                    try:
                        return int(s)
                    except ValueError:
                        return float(s)
                val = list(map(lambda x:num(x),val))
        else:
            val = getvalue(val, schema)
        if hasattr(schema,"color"):
             val = _set_color(str(val), getattr(__colors__,schema.color))
        return val
    def repr_lign(self,key):
        schema = getattr(self.schema,key)
        if schema.repr:
            lign =[getfield(schema, "label", key)]
            lign.append (self.formatted_val(key))
            if hasattr(schema,"unit"):
                lign.append(schema.unit)
            if hasattr(schema, "desc"):
                lign.append(schema.desc)
            return lign
        return None
    def __repr__(self):
        data=[]
        for k in self.schema.__dict__.keys():
                lign = self.repr_lign(k)
                if not lign is None:
                    data.append(lign)
        return tabulate(data,numalign="left", stralign="left",tablefmt="pretty")
        
class solute(obj):
    def __init__(self,s=None):
        super().__init__()
        if s:
            for k,v in s.__dict__.items():
                setattr(self,k,v)
    def compare_to(self,key):
        return key==self.label or key in self.synonyms
    def update(self,save=True,**args):
        for k,v in args.items():
            if hasattr(self,k):
                setattr(self,k,v)
        if save:
            solutes.save()
        print(self)

class solutes(list):
    def __init__(self):
        for s in load_json("solutes"):
            self.append(solute(s))
    @property
    def type(self):
        return type(self).__name__
    def __repr__(self):
         data=[]
         for s in self:
             d=[]
             for k in _schema.headers.solutes.__dict__.keys():
                 d.append(s.formatted_val(k))
             data.append(d)
         return tabulate(data,numalign="left", stralign="left", showindex="always",headers=_schema.headers.solutes.__dict__.values())
    def find(self,key):
        return next((s for s in self if s.compare_to(key)), False)
    def save(self):
        with open (os.path.join(os.path.dirname(os.path.abspath(__file__)),"solutes.json"), "w") as f:
                json.dump(list(map(lambda x: x.__dict__,self)), f)
    def add(self,solute_,**args):
        s=self.find(solute_)
        if not s:
            s=solute()
            s.label=solute_
            for k,v in args.items():
                if hasattr(s,k):
                    setattr(s,k,v)
            for k,v in args.items():
                if hasattr(s,k):
                    setattr(s,k,v)
            self.append(s)
            self.save()
            print("solute {} successfully inserted".format(_set_color(solute_,__colors__.byellow)))
        else:
            print("solute {} already exists".format(_set_color(solute_,__colors__.byellow)))
        print(self)
    def rm(self,solute_label):
        s=self.find(solute_label)
        if s:
            self.remove(s)
            self.save()
            print("solute {} successfully removed".format(_set_color(s.label,__colors__.byellow)))
        else:
            print("undefined solute {}".format(_set_color(solute_label,__colors__.byellow)))
        print(self)
    def update(self,solute_label,**args):
        s=self.find(solute_label)
        if s:
            for k,v in args.items():
                if hasattr(s,k):
                    setattr(s,k,v)
            self.save()
            print("solute {} successfully updated".format(_set_color(s.label,__colors__.byellow)))
            print(s)
        else:
            print("undefined solute {}".format(_set_color(solute_label,__colors__.byellow)))
            
solutes_database = solutes()

class spiral_membrane_res(obj):
    def __init__(self):
        super().__init__()


class spiral_membrane(obj):
    def __init__(self,**args):
        self.auto_calcul=False
        super().__init__()
        for k,v in args.items():
            if hasattr(self,k):
                setattr(self,k,v)
        self.ns = len(self.solutes)
        if self.ns:
            for x in ["k","B","Cin"]:
                if len(getattr(self,x))!=self.ns:
                    if x in ["Cin"]:
                        setattr(self,x,zeros(self.ns))
                    else:
                        setattr(self,x,list(map(lambda i: getattr(solutes_database[i],x),self.solutes)))
                
        self.res = spiral_membrane_res()
        self.calcul()
        self.auto_calcul=True
        
    def cell(self,i):
        R=8.314 # J/K/mol
        T=self.T+273.15
        Aw=self.Aw
        NLE = self.NLE
        ns = self.ns
        
        self.res.x[i]=self.res.x[i-1]+self.L/NLE
        
        PIp=R*T*self.res.Cp[i-1,:]*1e-5 # bar
        
        self.res.Pr[i]=self.res.Pr[i-1]-self.DP/NLE
        def sys_eq(Cm):
            PIm=R*T*Cm*1e-5 # bar
            PI=(PIm-PIp).sum() # bar
            Jw=(self.res.Pr[i]-self.Patm-PI)*Aw # m/h
            Cm_=self.res.Cp[i-1,:]+(self.res.Cr[i-1,:]-self.res.Cp[i-1,:])*exp(Jw/self.k) # mol/m3, exp(m/h / m/h)
            return abs(Cm_-Cm)
        self.res.Cm[i,:]=least_squares(sys_eq,self.res.Cm[i-1,:],method="trf",bounds=([0]*ns,[inf]*ns),).x
        #self.res.Cm[i,:]=fsolve(sys_eq,self.res.Cm[i-1,:])
        PIm=R*T*self.res.Cm[i,:]*1e-5 # bar
        #print(self.res.Cm[i,:])
       
        self.res.PI[i]=(PIm-PIp).sum() # bar
        self.res.Jw[i]=(self.res.Pr[i]-self.Patm-self.res.PI[i])*Aw # m/h
        self.res.PIm[i,:] = PIm
        
        self.res.J[i,:]=self.B*(self.res.Cm[i,:]-self.res.Cp[i-1,:]) # mol/m3 * m/h =>mol/m2/h
        self.res.Cp[i,:]=self.res.J[i,:]/self.res.Jw[i] # mol/m2/h / m/h => mol/m3
        self.res.Vp[i]=self.res.Jw[i]*self.S/NLE # m/h *m2 => m3/h
        self.res.Vr[i]=self.res.Vr[i-1]-self.res.Vp[i]
        self.res.Cr[i,:]=(self.res.Vr[i-1]*self.res.Cr[i-1,:]-self.res.Cp[i-1,:]*self.res.Vp[i-1])/self.res.Vr[i]
    
      
        
    def balance(self):
        Vr=self.res.Vr_out
        Vp=self.res.Vp_out
        Vin=self.Vin
        Cin=self.Cin
        Cr=self.res.Cr_out
        Cp=self.res.Cp_out

        mol_in = Cin*Vin
        mol_r = Cr*Vr
        mol_p = Cp*Vp
        
        def set_mol_h(val):
            return _set_color(_set_decimals(val,"3",scientific_notation=1),__colors__.byellow)
        
        data=[["total",getvalue(Vin,schema= self.schema.Vin),
               getvalue(Vr,schema= self.res.schema.Vr),
               getvalue(Vp,schema= self.res.schema.Vp),
               _set_color(_set_decimals(Vin-Vp-Vr,"3",scientific_notation=1),__colors__.bblue),self.schema.Vin.unit],
             ]
        for i in range(self.ns):
            data.append([solutes_database[self.solutes[i]].label,getvalue(Cin[i],schema= self.schema.Cin),
                         getvalue(Cr[i],schema= self.res.schema.Cr),
                         getvalue(Cp[i],schema= self.res.schema.Cp),
                         "",
                         self.schema.Cin.unit
                        ])
            data.append(["",
                         set_mol_h(mol_in[i]),
                         set_mol_h(mol_r[i]),
                         set_mol_h(mol_p[i]),
                         _set_color(_set_decimals(mol_in[i]-mol_r[i]-mol_p[i],"3",scientific_notation=1),__colors__.bblue),"mol/h"
                         ])
        print(tabulate(data,headers =["","feed","retentate","permeate","balance",""],numalign="left", stralign="left",tablefmt="pretty"))

    def plot(self,Cr=False, Cp=False,Vp=False,Vr=False,PI=False,Jw=False):
        import matplotlib.pyplot as plt
        if Cr:
            plt.figure("Retentate concentrations")
            for i in range(self.ns):
                plt.plot(self.res.x*1000,self.res.Cr[:,i],label=solutes[self.solutes[i]].label)
                plt.xlabel("Position in mm")
                plt.ylabel("concentration in mol/m3")
                plt.legend()
        if Cp:
            plt.figure("Permeate concentrations")
            for i in range(self.ns):
                plt.plot(self.res.x[1:]*1000,self.res.Cp[1:,i],label=solutes[self.solutes[i]].label)
                plt.xlabel("Position in mm")
                plt.ylabel("concentration in mol/m3")
                plt.legend()
        if Vp:
            plt.figure("Permeate volumes")
            plt.plot(self.res.x[1:]*1000,cumsum(self.res.Vp[1:]))
            plt.xlabel("Position in mm")
            plt.ylabel("volume flowrate in m3/h")
        if Vr:
            plt.figure("Retentate volumes")
            plt.plot(self.res.x*1000,self.res.Vr)
            plt.xlabel("Position in mm")
            plt.ylabel("volume flowrate in m3/h")
        if PI:
            plt.figure("osmotic pressure difference")
            plt.plot(self.res.x*1000,self.res.PI)
            plt.xlabel("Position in mm")
            plt.ylabel("bar")
    def plt(self,solutes=None,res=[]):
        import matplotlib.pyplot as plt
        if isinstance(res,str):
            res=[res]
        for r_ in res:
            if not hasattr(r_,"__iter__") or isinstance(r_,str):
                r_=[r_]
            plt.figure(", ".join(r_))
            ylabel=set()
            for r in r_:
                if hasattr(self.res,r):
                    y = getattr(self.res,r)
                    schema = getattr(self.res_schema,r)
                    x=self.res.x*1000
                    if y.shape == (self.NLE+1,self.ns):
                        if hasattr(schema,"plot"):
                            x,y=eval(schema.plot)
                        if solutes is None:
                            solutes=self.solutes
                        for i in solutes:
                            s = solutes_database[i]
                            ylabel.add(schema.latex)
                            plt.plot(x,y[:,i],label=', '.join((schema.label,s.label)))
                            
                    else:
                        if hasattr(schema,"plot"):
                            x,y=eval(schema.plot)
                        ylabel.add(schema.latex)
                        plt.plot(x,y,label=', '.join((schema.label,schema.latex)))
                        
            plt.legend()
            plt.xlabel(getattr(self.res_schema,"x").latex)
            plt.ylabel(", ".join(ylabel))
            plt.grid()
                        
    def pltc(self,solutes=None):
        self.plt(solutes=solutes,res=[["Cr","Cp"]])
    def calcul(self):
        #self.auto_calcul=False
        from tqdm import tqdm
        st = time.process_time()
        NLE = self.NLE
        ns = self.ns
        
        self.res.LE = self.L/NLE # m
        self.k=array(self.k) # m/h
        self.B=array(self.B) # m/h
        self.Cin=array(self.Cin)
        
        self.res.Vr=zeros(NLE+1)
        self.res.Vp=zeros(NLE+1)
        self.res.Cr=zeros((NLE+1,ns))
        self.res.Cm=zeros((NLE+1,ns))
        self.res.Cp=zeros((NLE+1,ns))
        self.res.PIm=zeros((NLE+1,ns))
        self.res.J=zeros((NLE+1,ns))
        self.res.Pr=zeros(NLE+1)
        self.res.Cr[0,:]=self.Cin
        self.res.Vr[0]=self.Vin
        self.res.Pr[0]=self.Pin
        
        self.res.x=zeros(NLE+1)
        self.res.Jw=zeros(NLE+1)
        self.res.PI=zeros(NLE+1)

        for i in tqdm(range(1,NLE+1),desc="membrane calculation"):
            self.cell(i)
            
        self.res.Vr_out=self.res.Vr[-1]
        self.res.Vp_out=self.res.Vp.sum()
        self.res.Cr_out = self.res.Cr[-1]
        self.res.Cp_out=zeros(self.ns)
        for i in range(self.ns):
            self.res.Cp_out[i]=(self.res.Cp[:,i]*self.res.Vp).sum()/self.res.Vp_out
        
        self.res.calculation_time = time.process_time()-st
        print(self.res)


    def __setattr__(self, key, value):
        if key in ["ns","res","auto_calcul"]:
            super(spiral_membrane , self).__setattr__(key, value)
        else:
            auto_calcul = self.auto_calcul
            self.auto_calcul=False
            super(spiral_membrane , self).__setattr__(key, value)
            if auto_calcul:
                self.calcul()
            self.auto_calcul=auto_calcul
    @property
    def res_schema(self):
        return getattr(_schema,self.type+"_res")
    @property
    def get_schema(self):
        data = []
        for k,v in self.schema.__dict__.items():
                data.append([k,getfield(v,"desc",""),getfield(v,"unit",""),"argument"])
        if hasattr(self,"res"):
            for k,v in getattr(_schema,self.type+"_res").__dict__.items():
                data.append([k,getfield(v,"desc",""),getfield(v,"unit",""),"result"])
        print(tabulate(data,numalign="left", stralign="left",headers=["Property","Label","Unit","type"]))
        # set result schema
    def unzip(self,*args):
        return map(lambda k: getattr(self,k),args)
    def zipres(self,keys,vals):
        for i,k in enumerate(keys):
            setattr(self.res,k,vals[i])
        
        

    def __repr__(self):
        str_=_set_color("Process specification",__colors__.bblue)
        str_+="\n"
        str_+=super().__repr__()
        return str_
                    
    
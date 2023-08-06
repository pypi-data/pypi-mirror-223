# -*- coding: utf-8 -*-
"""
Created on Wed Jun  7 02:18:50 2023

@author: Hedi
"""
from tabulate import tabulate
import json
import glob
def f_v(v,dec):
    return ('{:.'+str(dec)+'f}').format(v)
from processoptim.thermo_properties import __tomato_paste__, __water__
from processoptim.processes import shell_tube_heat_exchanger, falling_film_evaporator
tomato = __tomato_paste__()
water = __water__()
from numpy import zeros, linspace,array,arange, exp, diff

from processoptim.pylca.lca import lca

lca= lca()


#==============================================================================
class process:
    def __init__(self,name,**args):
        self.name = name
        self.chemicals = {}
        self.capa=0
        self.x_ratio=1 # out/in
        self.UF = [0,0] # unité fonc masse cumulée kg sur la durée de traitement
        for x in ["elec","hot_water","steam","cold_water","freshwater","wastewater","processing_time","loss"]:
            setattr(self,x,0)
        for k,v in args.items():
            setattr(self,k,v)
    @property
    def UF_in(self):
            return [self.UF[0]*self.x_ratio/(1-self.loss),self.UF[1]/self.x_ratio]
    @property
    def capa_out(self):
        return self.capa*(1-self.loss)/self.x_ratio
#==============================================================================
class flux:
    def copy(self,name):
        f = flux(name)
        for x in ["dm","m","T"]:
            setattr(f,x,getattr(self,x))
        return f
    def __init__(self,name,**args):
        self.name=name
        self.dm = 0
        self.m=0
        self.T=0
        for k,v in args.items():
            setattr(self,k,v)
    @property
    def H(self):
            return tomato.H(self.dm,self.T)
    @property
    def energy(self):
        return self.m*self.H

    def mass(self,prop=''):
        if prop in ['w','water']:
            return self.m-self.flowrate('dm')
        elif not prop:
            return self.m
        return getattr(self,prop)*self.m
    def frac(self,prop='',basis='wb'):
        if basis=='db':
            return self.flowrate(prop)/self.flowrate('dm')
        else:
            return self.flowrate(prop)/self.m
    @property
    def slabel(self):
        return self.name+'\n'+'{:.0f}'.format(self.m)
#==============================================================================
class __flows__(dict):
    def add(self,f):
        self[f.name]=f
        return f
    def __repr__(self):
        table =[["","","kg","°C","DM %","DM kg","kJ"]]
        i=0
        for k,v in self.items():
            table.append([i,k,f_v(v.m,3),f_v(v.T,0),f_v(v.dm*100,0),f_v(v.mass("dm"),3),
                          f_v(v.energy,3)])
            i+=1
        return tabulate(table)
#==============================================================================
class __processes__(dict):
    def add(self,f):
        self[f.name]=f
        return f
    def __repr__(self):
        table =[['',"process","UF","Capa kg/h","processing time s","loss %","Elec. kJ","hot water kJ","cold water kJ","steam kJ","freshwater m3","wastewater m3"]]
        i=0
        for k,v in self.items():
            table.append([i,k,f_v(v.UF[0],2),f_v(v.capa*3600,2),f_v(v.processing_time,0),
                          
                          f_v(v.loss*100,0),
                          f_v(v.elec,3),f_v(v.hot_water,3),f_v(v.cold_water,3),
                          f_v(v.steam,3),f_v(v.freshwater,3),f_v(v.wastewater,3)])
        return tabulate(table)
#==============================================================================

class quality_indicator:
    def __init__(self,Tref, Ea, kref):
        self.Tref=Tref+273.15 # °C to K
        self.Ea=Ea # J/mol
        self.kref=kref/60 # min-1 to s-1
        self.Q=[] # quality
    def calcul(self,t,T,Q0=1):
        # R=8.31 #J.mol-1.K-1
        self.Q=[Q0]
        for i in range(1,len(t)):
            self.Q.append(self.Q[-1]*exp(-self.kref*exp(-self.Ea*(1/self.Tref-1/(T[i]+273.15))/8.31)*(t[i]-t[i-1])))

class __quality__:
    def __init__(self, usine):
        self.T=[]
        self.t=[]
        self.usine=usine
        
        # vitamine C
        # k_ref=0.4 #min-1
        # Ea=40e3 #J.mol-1
        # T_ref=90
        
        # color
        # k_ref=0.00142 #min-1
        # Ea=28e3 #J.mol-1
        # T_ref=90
        
        self.indicators={}
        self.indicators["vitamine_C"]=quality_indicator(90, 40e3, .4)
        self.indicators["color"]=quality_indicator(90, 28e3, .00142)
    def calcul(self,indicator=None, n=10):
        self.T=[]
        self.t=[]
        # préchauffage HB
        self.T.extend(linspace(self.usine.HB.feed_temperature,self.usine.HB.target_temperature,n))
        self.t.extend(linspace(0,self.usine.HB.res.ts,n))
        
        # hold
        self.T.extend([self.usine.HB.target_temperature]*(2-1))
        self.t.extend(linspace(0, 3*60,2)[1:]+self.usine.HB.res.ts) # 3 min
        
        #pre-effects times => required time before entering each effects
        pre_t = [0]*self.usine.n_effects
        pre_t[0]=60 # entre HB et evapo 1min
        # evapo
        for i in range(self.usine.n_effects):
            self.T.extend([self.usine.evapo.res.T[i+1]]*n)
            self.t.extend((linspace(0,self.usine.evapo.res.ts[i],n)+self.t[-1]+pre_t[i]))
        # # pasteu
        self.T.extend(linspace(self.T[-1],self.usine.pasteu.target_temperature,n)[1:])
        self.t.extend(linspace(0,self.usine.pasteu.res.ts,n)[1:]+self.t[-1])
        # # hold
        self.T.extend(linspace(self.T[-1],self.usine.pasteu.target_temperature,2)[1:])
        self.t.extend(linspace(0,12*60,2)[1:]+self.t[-1])
        # # refroidissement
        self.T.extend(linspace(self.T[-1],self.usine.P_cool.target_temperature,n)[1:])
        self.t.extend(linspace(0,self.usine.P_cool.res.ts,n)[1:]+self.t[-1])
        
        # for quality_indicator in self.indicators.values():
        #     quality_indicator.calcul(self.t,self.T)
        if indicator:
            self.indicators[indicator].calcul(self.t,self.T)
            return self.indicators[indicator].Q
            
    def tT_plt(self):
        self.calcul()
        import matplotlib.pyplot as plt
        plt.plot(self.t,self.T)
    def Q_plt(self,indicator):
        if indicator in self.indicators.keys():
            self.calcul(indicator=indicator)
            import matplotlib.pyplot as plt
            plt.plot(self.t,self.indicators[indicator].Q)

class __usine__:
    def __init__(self,n_effects=3,Tsteam=80,x_ratio_evapo=2.4,Q_tri=2):
        self.flows = __flows__()
        self.processes = __processes__()
        self.n_effects = n_effects
        self.Tsteam = Tsteam
        self.x_ratio_evapo=x_ratio_evapo
        self.Q_tri = Q_tri # Kw
        self.quality = __quality__(self)
        
    def calcul(self):
        x_ratio_evapo = self.x_ratio_evapo
        capa_lavage = 20*1000  #kg/h
        # Calcul UF
        UF = [1227400,12/100]  # unité fonctionnelle en kg de purée de tomate produite, MS bh
        # step = (label, loss, x_ratio)
        steps = [("lavage",0.1,1), ("tri",.05,1), ("broy",0,1), ("HB_heat",0,1), ("HB_hold",0,1),
                  ("Raff",.05,1),("Conc",0,x_ratio_evapo), ("P_heat",0,1), ("P_hold",0,1), ("P_cool",0,1), ("Remp",.05,1)]
        for step in steps:
            self.processes.add(process(step[0],loss=step[1],x_ratio=step[2]),)
        self.processes["Remp"].UF=UF
        for i in range(len(steps)-2,-1,-1):
           self.processes[steps[i][0]].UF=self.processes[steps[i+1][0]].UF_in
        #==============================================================================
        # tomate brute
        lavage=self.processes["lavage"]
        lavage.capa = capa_lavage/3600

        feed = self.flows.add(flux("feed",T=20,m=lavage.UF_in[0],dm=lavage.UF_in[1],))
        # """
        # Lavage
        # Feed :
        #     -> washed
        #     -> washing waste
        # """
        Q_lavage = 100 #kW 
        lavage.processing_time = lavage.UF_in[0]/capa_lavage # en s
        lavage.elec=lavage.processing_time*Q_lavage
        lavage.freshwater = 6*lavage.processing_time/3600 # (6 m3/h eau propre) # Bosona : 0.4 kg/kg tomate ; Zacharias : 0.2 kg/kg tomate
        lavage.wastewater=lavage.freshwater
        # # wastes
        washing_waste = self.flows.add(feed.copy("washing waste"))
        washing_waste.m*=lavage.loss
        # washed
        washed = self.flows.add(feed.copy("washed"))
        washed.m-=washing_waste.m
        #==============================================================================
        # Tri
        tri = self.processes["tri"]
        #Q_tri = 2 #kW
        Q_tri = self.Q_tri
        tri.capa = lavage.capa_out
        tri.processing_time = tri.UF_in[0]/tri.capa # en s
        tri.elec=tri.processing_time*Q_tri
        # # wastes
        sorting_waste = self.flows.add(washed.copy("sorting waste"))
        sorting_waste.m*=tri.loss
        # tomate triée
        triee = self.flows.add(washed.copy("sorted"))
        triee.m-=sorting_waste.m
        #==============================================================================
        # broyage
        broy = self.processes["broy"]
        Q_broy = 20.9   #kW 
        broy.capa = tri.capa_out
        broy.processing_time = broy.UF_in[0]/broy.capa # en s
        broy.elec=broy.processing_time*Q_broy
        # # wastes
        broy_waste = self.flows.add(triee.copy("broy waste"))
        broy_waste.m*=broy.loss
        # tomate broyée
        broyee = self.flows.add(triee.copy("broyee"))
        broyee.m-=broy_waste.m
        #==============================================================================
        # HB_heat
        # Ech tub chauff 2

        HB_shell_tube_heat_exchanger = shell_tube_heat_exchanger(feed_concentration=broyee.dm,
                                                                 feed_flowrate=broy.capa_out,
                                                                 feed_temperature=broyee.T,
                                                                 target_temperature=95,
                                                                 tube_diameter=2e-2,
                                                                 tube_length=4,
                                                                 n_tubes=200,
                                                                 n_passes=1)
        HB_heat=self.processes["HB_heat"]
        HB_heat.capa=broy.capa_out
        HB_heat.processing_time=HB_heat.UF_in[0]/HB_heat.capa
        HB_heat.elec=HB_shell_tube_heat_exchanger.res.E*HB_heat.processing_time
        HB_heat.steam = HB_shell_tube_heat_exchanger.res.Q*HB_heat.processing_time
        
        # tomate après HB heat
        HB_heated = self.flows.add(broyee.copy("HB heated"))
        HB_heated.T=HB_shell_tube_heat_exchanger.target_temperature
        
        # HB_hold
        HB_hold=self.processes["HB_hold"]
        HB_hold.capa = HB_heat.capa_out
        HB_hold.processing_time=HB_hold.UF_in[0]/HB_hold.capa
        HB_holded = self.flows.add(HB_heated.copy("HB holded"))
        
        setattr(self,"HB",HB_shell_tube_heat_exchanger)
        
        #==============================================================================
        # Raff
        Q_raffineur = 3   #kW
        Raff = self.processes["Raff"]
        Raff.capa= HB_hold.capa_out
        Raff.processing_time=Raff.UF_in[0]/Raff.capa
        Raff.elec=Q_raffineur*Raff.processing_time
        # # wastes
        raff_waste = self.flows.add(HB_holded.copy("raff waste"))
        raff_waste.m*=Raff.loss
        # tomate apres Raff
        raffinee = self.flows.add(HB_holded.copy("raffinee"))
        raffinee.m-=raff_waste.m
        #==============================================================================
        # Conc
        Conc = self.processes["Conc"]
        Conc.capa = Raff.capa_out
        evapo = falling_film_evaporator(n_effects=self.n_effects,
                                        steam_temperature=self.Tsteam,
                                        feed_concentration=Conc.UF_in[1],
                                        target_concentration=Conc.UF[1],
                                        feed_flowrate=Conc.capa,
                                        n_tubes=200,
                                        tube_diameter=.02,
                                        tube_length=8)
        
        Conc.processing_time=Conc.UF_in[0]/Conc.capa
        Conc.elec=evapo.res.E.sum()*HB_heat.processing_time
        Conc.steam = evapo.res.V[0]*water.Lv_T(evapo.steam_temperature)*Conc.processing_time
        
        # concentrats
        concentrats=[]
        for i in range(evapo.n_effects):
            concentrats.append(
                self.flows.add(flux("concentrat {}".format(i+1),
                                    T=evapo.res.T[i],
                                    m=evapo.res.L[i+1]*Conc.processing_time,
                                    dm=evapo.res.x[i+1]))
                )
        # concentrat = self.flows.add(raffinee.copy("concentrat"))
        # concentrat.T=evapo.res.T[-1]
        # concentrat.dm = Conc.UF[1]
        # concentrat.m = Conc.UF[0]

        # condensats
        condensats= []
        for i in range(evapo.n_effects+1):
            condensats.append(
                self.flows.add(flux("condensat {}".format(i+1),T=evapo.res.T[i],m=evapo.res.V[i]*Conc.processing_time))
                )
            # concentrati.append(
            #     self.flows.add(flux("concentrat_i {}".format(i+1),T=evapo.res.T[i],m=evapo.res.L[i]*Conc.processing_time))
            #     )
        setattr(self,"evapo",evapo)
        #==============================================================================
        # P_heat
        capa_P_heat = evapo.res.L[-1] # kg/s
        P_shell_tube_heat_exchanger = shell_tube_heat_exchanger(feed_concentration=concentrats[-1].dm,
                                                                 feed_flowrate=capa_P_heat,
                                                                 feed_temperature=concentrats[-1].T,
                                                                 target_temperature=90,
                                                                 tube_diameter=2e-2,
                                                                 tube_length=4,
                                                                 n_tubes=50,
                                                                 n_passes=1)
        P_heat=self.processes["P_heat"]
        P_heat.capa=capa_P_heat
        P_heat.processing_time=P_heat.UF_in[0]/capa_P_heat
        P_heat.elec=P_shell_tube_heat_exchanger.res.E*P_heat.processing_time
        P_heat.steam = P_shell_tube_heat_exchanger.res.Q*P_heat.processing_time
        
        # tomate après P heat
        P_heated = self.flows.add(concentrats[-1].copy("P heated"))
        P_heated.T=P_shell_tube_heat_exchanger.target_temperature
        
        # P_hold
        P_hold=self.processes["P_hold"]
        P_hold.capa = P_heat.capa_out
        P_hold.processing_time=P_hold.UF_in[0]/P_hold.capa
        P_holded =self.flows.add(P_heated.copy("P holded"))
        
        setattr(self,"pasteu",P_shell_tube_heat_exchanger)
        #==============================================================================
        # P_cool
        P_cool_shell_tube_heat_exchanger = shell_tube_heat_exchanger(feed_concentration=P_holded.dm,
                                                                 feed_flowrate=P_hold.capa_out,
                                                                 feed_temperature=P_holded.T,
                                                                 target_temperature=25,
                                                                 tube_diameter=2e-2,
                                                                 tube_length=4,
                                                                 n_tubes=50,
                                                                 n_passes=1)
        P_cool=self.processes["P_cool"]
        P_cool.capa=P_hold.capa_out
        P_cool.processing_time=P_cool.UF_in[0]/P_cool.capa
        P_cool.elec=P_cool_shell_tube_heat_exchanger.res.E*P_cool.processing_time
        P_cool.cold_water = P_cool_shell_tube_heat_exchanger.res.Q*P_cool.processing_time
        
        # tomate après P cool
        P_cooled = self.flows.add(P_holded.copy("P cooled"))
        P_cooled.T=P_cool_shell_tube_heat_exchanger.target_temperature
        
        setattr(self,"P_cool",P_cool_shell_tube_heat_exchanger)
        
        

        evap_cool=self.processes.add(process("evap_cool"))
        evap_cool.processing_time=Conc.processing_time
        evap_cool.elec=P_cool.elec
        evap_cool.cold_water=evapo.res.V[-1]*Conc.processing_time*water.Lv_T(evapo.res.T[-1])
        #==============================================================================
        # Remp
        Q_remplissage = 1.5 # kW
        
        Remp = self.processes["Remp"]
        Remp.capa = P_cool.capa_out
        Remp.processing_time=Remp.UF_in[0]/Remp.capa
        Remp.elec=Q_remplissage*Remp.processing_time
        # # wastes
        remp_waste = self.flows.add(P_cooled.copy("remp waste"))
        remp_waste.m*=Remp.loss
        # tomate apres Remp
        puree = self.flows.add(P_cooled.copy("puree"))
        puree.m-=remp_waste.m


    @property
    def GW(self):
        return lca(self.elec,"cml","mix_elec_fr",6)+ lca(self.water,"cml","water_fr",6)
        
        
    @property
    def color(self):
        return self.quality.calcul("color")[-1]
    
    @property
    def elecBis(self):
        table = list(map(lambda p:[p.name,p.elec],self.processes.values()))
        print(tabulate(table))
    @property
    def elec(self):
            return sum(map(lambda p:p.elec,self.processes.values()))
    @property
    def steam(self):
            return sum(map(lambda p:abs(p.steam),self.processes.values()))
    @property
    def cool_water(self):
            return sum(map(lambda p:abs(getattr(p,"cold_water")),self.processes.values()))
        
    def sensitivity_analysis(self,evaluate_model,variables,bounds,N_samples=1024):
        from SALib.sample import saltelli
        from SALib.analyze import sobol
        from tqdm import tqdm
        problem = {'num_vars': len(variables),'names': variables,
            'bounds': bounds}
        # Generate Samples
        param_values = saltelli.sample(problem, N_samples);
        Y = zeros([param_values.shape[0]])
        # run model
        X_tmp = list(map(lambda x: getattr(self,x),variables))
        Y = zeros([param_values.shape[0]])
        for i, X in enumerate(tqdm(param_values,desc="tomato sensitivity",colour='#00ff00',smoothing=1)):
            for j in range(len(variables)):
                if variables[j] in ["n_effects"]:
                    setattr(self,variables[j],round(X[j]))
                else:
                    setattr(self,variables[j],X[j])
                self.calcul()
                Y[i] = getattr(self,evaluate_model)
                # perform analysis
        Si = sobol.analyze(problem, Y)
        # re-establish tmp values
        for i,v in enumerate(variables):
            setattr(self,v,X_tmp[i])
        return Si
    
    def drawmass(self):
        s=list(self.flows.values())
        import matplotlib.pyplot as plt
        from matplotlib.sankey import Sankey
        
        from matplotlib import rcParams
    
        #plt.rc('font', family = 'serif')
        plt.rcParams['font.size']  = 16
        #plt.rcParams['font.serif'] = "Linux Libertine"
        plt.rcParams["legend.loc"] = 'upper right'
        fig = plt.figure()
        ax = fig.add_subplot(1,1,1, xticks=[], yticks=[])#
        sankey = Sankey(ax=ax,unit=None,gap=.1,scale=1/400, head_angle=160)
        a=0 # rotation
        
        sankey.add(flows=[s[0].m/3600,-s[1].m/3600,-s[2].m/3600],
                   orientations=[0,-1,0],
                   labels=["","",""],
                   rotation=a,  label='Lavage',fc='tomato',
                   alpha=0.8,hatch="oo") 

        sankey.add(flows=[s[2].m/3600,-s[4].m/3600,-s[3].m/3600],orientations=[0,0,1],
                    labels=["","",""],
                    rotation=a,  label='tri',prior=0,connect=(2,0),fc='tomato', alpha=0.8,hatch="o")
        
        
        # sankey.add(flows=[s[4].m/3600,-s[5].m/3600,-s[6].m/3600],orientations=[0,1,0],
        #             labels=["","",""],
        #             rotation=a,  label='broy',prior=1,connect=(1,0),fc='tomato', alpha=0.8,hatch="..")
        
        # sankey.add(flows=[s[6].m/3600,-s[8].m/3600],orientations=[0,0],
        #             labels=["",""],
        #             rotation=a,  label='HB',prior=2,connect=(2,0),fc='tomato', alpha=0.5,hatch=".")
        
        # sankey.add(flows=[s[8].m/3600,-s[9].m/3600,-s[10].m/3600],orientations=[0,1,0],
        #             labels=["","",""],
        #             rotation=a,  label='Raff',prior=3,connect=(1,0),fc='tomato', alpha=0.5,)
        
        # conc_=list(filter(lambda x: "concentrat" in x.name, self.flows.values()))
        # cond_=list(filter(lambda x: "condensat" in x.name, self.flows.values()))
        # # effet 1
        # sankey.add(flows=[s[10].m/3600,-cond_[0].m/3600,-conc_[0].m/3600],orientations=[0,1,0],
        #             labels=["","",""],
        #             rotation=a,  label='Effet 1',prior=4,connect=(2,0),fc='tomato', alpha=0.6,)
        
        # for i in range(1,self.n_effects):
        #     sankey.add(flows=[conc_[i-1].m/3600,-cond_[i].m/3600,-conc_[i].m/3600],orientations=[0,1,0],
        #                 labels=["","",""],
        #                 rotation=a,  label='Effet '+str(i+1),prior=4+i,connect=(2,0),fc='tomato', alpha=0.6*(1+(i+1)*20/100),)
        
        # sankey.add(flows=[conc_[-1].m/3600,-self.flows["remp waste"].m/3600,-self.flows["puree"].m/3600],orientations=[0,1,0],
        #                 labels=["","",""],
        #                 rotation=a,  label='Raff',prior=4+self.n_effects,connect=(2,0),fc='tomato',)
       # plt.legend()
        d=sankey.finish()
      #  plt.legend()
    
usine = __usine__(n_effects=2,Tsteam=80,x_ratio_evapo=2.4,Q_tri=3)
usine.calcul()

"""
#profil T
T=[20,95,95,71,71,62,62,52,52,90,90,20]
t=array([0,13,3*60,60,10,0,12,0,17,5,704,5])
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 16})
plt.plot(t.cumsum()/60,T,"-o",markerfacecolor="white",markeredgecolor="green")
plt.xticks(t.cumsum()/60,[ "0",  "",  "3",  "4",  "5",  "",  "",  "",  "",  "", "17", ""],rotation=0)
plt.yticks(T)
plt.grid()
"""
"""
def elec_sort(item):
    return item.elec

p_ = sorted(usine.processes.values(),key=elec_sort)
elec_labels =  array(list(map(lambda x : x.name,p_)))
elec = array(list(map(lambda x : x.elec,p_)))
elec_p = elec/elec.sum()*100

import matplotlib.pyplot as plt
fig, ax = plt.subplots()
width = 0.75
ind = arange(len(elec))

ax.barh(elec_labels, elec_p, width, color = "tomato",edgecolor='black')
# plt.rcParams.update({'font.size': 12})
# plt.bar(elec_labels,elec_p)
# plt.legend()
plt.xlabel("% Elec. / Tot.")


for i, v in enumerate(elec_p):
     ax.text(v + 1, i + .1, "{:.0f}".format(v)+"%",
            color = 'blue', fontweight = 'bold')

"""
"""
def elec_sort(item):
    return abs(item.cold_water)

p_ = sorted(usine.processes.values(),key=elec_sort)
elec_labels =  array(list(map(lambda x : x.name,p_)))
elec = abs(array(list(map(lambda x : x.cold_water,p_))))
elec_p = elec/elec.sum()*100

import matplotlib.pyplot as plt
fig, ax = plt.subplots()
width = 0.75
ind = arange(len(elec))

ax.barh(elec_labels, elec_p, width, color = "tomato",edgecolor='black')
# plt.rcParams.update({'font.size': 12})
# plt.bar(elec_labels,elec_p)
# plt.legend()
plt.xlabel("% steam. / Tot.")


for i, v in enumerate(elec_p):
     ax.text(v + 1, i + .1, "{:.0f}".format(v)+"%",
            color = 'blue', fontweight = 'bold')
     """
     
# import matplotlib.pyplot as plt
# plt.rcParams.update({'font.size': 16})
# hatches = ['.', 'o', '..',"//","\\\\",""]
# patches=plt.pie([57,16,8,6,12,1],
#         labels=["broy\n57%","conc\n16%","raff\n8%","tri\n6","< 4%","< 1%"],)
# for i in range(len(patches[0])):
#     patches[0][i].set(hatch = hatches[i], fill=False)

# import matplotlib.pyplot as plt
# plt.rcParams.update({'font.size': 16})
# hatches = ['o', '++', 'x',".","//",".."]
# patches=plt.pie([56,39,5],
#         labels=["conc 56%","HB heat 39%","P heat 5%",],)
# for i in range(len(patches[0])):
#     patches[0][i].set(hatch = hatches[i], fill=False)

#usine.drawmass()
#Si = usine.sensitivity_analysis("cool_water", ["n_effects","Tsteam"], [[1,3],[60,120]],N_samples=1024)
#Si = usine.sensitivity_analysis("elec", ["Q_tri"], [[1.5,2.5]],N_samples=1024)

#Si = usine.sensitivity_analysis("color", ["n_effects"], [[1,3]],N_samples=1024)





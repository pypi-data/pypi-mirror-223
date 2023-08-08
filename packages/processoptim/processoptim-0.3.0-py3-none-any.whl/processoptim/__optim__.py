# -*- coding: utf-8 -*-
"""
Created on Mon Aug  7 09:26:04 2023

@author: Hedi
"""

from pymoo.core.problem import ElementwiseProblem
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.operators.crossover.sbx import SBX
from pymoo.operators.mutation.pm import PM
from pymoo.operators.sampling.rnd import FloatRandomSampling
from pymoo.termination import get_termination
from pymoo.optimize import minimize
from pymoo.decomposition.asf import ASF
from numpy import array

class __optim__:
    def __init__(self,pop_size=40,n_offsprings=10,n_gen=40):
        self.res=None
        self.algorithm = NSGA2(
            pop_size=pop_size,
            n_offsprings=n_offsprings,
            sampling=FloatRandomSampling(),
            crossover=SBX(prob=0.9, eta=15),
            mutation=PM(eta=20),
            eliminate_duplicates=True
        )
        self.termination = get_termination("n_gen", n_gen)
    def calcul(self, parent, decision_parameters, targets):
        decision_parameters__ = [
            x for d_ in decision_parameters for x in d_.keys()]
        parent.integers.update([x for x_ in decision_parameters for x in x_.keys(
        ) if len(list(x_.values())[0]) > 2 and list(x_.values())[0][2] == int])
        class __optimprob__(ElementwiseProblem):
            def __init__(self):
                super().__init__(n_var=len(decision_parameters),
                                 n_obj=len(targets),
                                 n_ieq_constr=0,
                                 xl=array(
                                     [x[0] for x_ in decision_parameters for x in x_.values()]),
                                 xu=array([x[1] for x_ in decision_parameters for x in x_.values()]))

            def _evaluate(self, x, out, *args, **kwargs):
                for i, k in enumerate(decision_parameters__):
                    setattr(parent, k, x[i])
                parent.calcul()
                out["F"] = [getattr(parent, x) for x in targets]
        return minimize(__optimprob__(),
                       self.algorithm,
                       self.termination,
                       seed=1,
                       save_history=True,
                       verbose=True)
    def getPareto(self,res,normalizing=False):
        if normalizing:
            approx_ideal = res.F.min(axis=0)
            approx_nadir = res.F.max(axis=0)
            return  (res.F - approx_ideal) / (approx_nadir - approx_ideal)
        else:
            return res.F
    def compromis(self,res, importances):
        return ASF().do(self.getPareto(res,normalizing=True), 1/array(importances)).argmin()
        
        
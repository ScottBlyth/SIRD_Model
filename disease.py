# -*- coding: utf-8 -*-
"""
Created on Tue May 21 15:40:32 2024

@author: scott
"""

from GI import Genome
from random import random, randint
import numpy as np
from sklearn.cluster import KMeans 

def random_vec(n, vec):
    return np.array([2*vec[i]*random()-vec[i] for i in range(n)])

class disease(Genome): 
    
    def __init__(self, l1,l2,l3,l4, mutation_rate = (0.00001, 0.00001, 0.00001, 0.00001), lock_l1=False):
        # l1 : infection rate
        # l2 : recovery rate
        # l3 : immunity 
        # l4 : mortality rate
        self.l1,self.l2,self.l3,self.l4 = l1,l2,l3,l4 
        self.lock_l1 = lock_l1
        self.mutation_rate = mutation_rate
        
    def to_phenotype(self):
        return np.array([self.l1,self.l2,self.l3,self.l4])
        
    def get_params(self):
        return self.l1,self.l2,self.l3,self.l4

    def copy(self):
        return disease(self.l1,self.l2,self.l3,self.l4)
    
    def mutate(self): 
        k = random_vec(4, self.mutation_rate)
        new_vec = self.to_phenotype()+k
        l1,l2,l3,l4 = new_vec
        if self.lock_l1:
            l1 = self.l1
        return disease(abs(l1),abs(l2),abs(l3),abs(l4))
        
    def crossover(self, other):
        if randint(1,2) == 1:
            return self
        diseases = [self.to_phenotype(), other.to_phenotype()]
        l1,l2,l3,l4 = [diseases[randint(0,1)][i] for i in range(4)]
        return disease(l1,l2,l3,l4)




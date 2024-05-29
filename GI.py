# -*- coding: utf-8 -*-
"""
Created on Thu May 23 14:18:11 2024

@author: scott
"""

from abc import ABC,abstractmethod 

class Genome(ABC):
    def __init__(self):
        pass 
    
    @abstractmethod 
    def to_phenotype(self):
        pass
    
    @abstractmethod 
    def mutate(self):
        pass 
    
    @abstractmethod 
    def crossover(self, other):
        pass

# -*- coding: utf-8 -*-
"""
Created on Thu May 23 14:18:11 2024

@author: scott
"""

from abc import ABC,abstractmethod 
import random
import numpy as np

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

class Environment(ABC): 
    def __init__(self):
        pass 
    
    @abstractmethod 
    def fitness(self, sol)->float:
        pass 
    

def evolve(env : Environment, population, iterations):
    for _ in range(iterations):
        print("#########################################")
        # compute probability distribution 
        fitnesses = [env.fitness(sol) for sol in population]
        probabilties = [1/(f+1) for f in fitnesses]
        probabilties = np.array(fitnesses)/sum(fitnesses)
        sol1i = np.random.choice(range(len(fitnesses)), p=probabilties)
        sol2i = np.random.choice(range(len(fitnesses)), p=probabilties)
        sol1 = population[sol1i] 
        sol2 = population[sol2i] 
        new_sol = sol1.crossover(sol2) 
        mutated_sol = new_sol.mutate()
        
        # add mutated solution
        population.append(mutated_sol)
        fitnesses.append(env.fitness(mutated_sol))
        probabilties = np.array(fitnesses)/sum(fitnesses)
        
        # pick random one to remove 
        # excluding elite solution
        probabilties_ = [(i, p) for i,p in enumerate(probabilties)]
        probabilties_ = sorted(probabilties_, key=lambda x : x[1])
        
        
        probabilities2 = [x[1] for x in probabilties_[1:]]
        p2 = np.array(probabilities2)/sum(probabilities2)
        index = np.random.choice(range(1,len(fitnesses)), p=p2)
        index_pop = probabilties_[index][0]
        population.pop(index_pop)
        print("iteration 1 done")
    return population
        
    

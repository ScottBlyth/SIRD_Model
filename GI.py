# -*- coding: utf-8 -*-
"""
Created on Thu May 23 14:18:11 2024

@author: scott
"""

from abc import ABC,abstractmethod 
import random
import numpy as np
import statistics as stats

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
    fitness_curve = []
    best_each_iter = []
    for _ in range(iterations):
        # compute probability distribution 
        fitnesses = [env.fitness(sol) for i,sol in enumerate(population)]
        # add to curve
        fitness_curve.append(stats.mean(fitnesses)) 
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
        
        # pick random one to remove 
        # excluding elite solution
        # probabilties are inversely 
        # proportional to fitness
        fitnesses = [(i,f) for i,f in enumerate(fitnesses)]
        fitnesses = sorted(fitnesses, key=lambda x : -x[1])
    
        best_each_iter += population
        
        probabilties = [1/(f+1) for i,f in fitnesses[1:]]
        probabilties = np.array(probabilties)/sum(probabilties)
        
        p = len(probabilties)
        idx = np.random.choice(range(p), p=probabilties)
        index = fitnesses[idx+1][0]
        population.pop(index)
    
        
        print("Iteration done...")

    return population,fitness_curve,best_each_iter
        
    

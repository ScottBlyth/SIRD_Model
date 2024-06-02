#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun  1 17:34:47 2024

@author: ningnong
"""

from GI import Environment 
from random import random
from math import exp

def accept(T, env, prev, candidate): 
    fitness = env.fitness(candidate)
    prev_fitness = env.fitness(prev)
    if fitness > prev_fitness:
        return True 
    probability = exp((fitness-prev_fitness)/T)
    print(fitness-prev_fitness)
    print("prob: ",probability)
    return random() <= probability

def simulated_annealing(env, initial, T_0, max_iterations=10): 
    T = T_0 
    current = initial
    i = max_iterations
    fitness_curve = []
    while T > 1 and i >= 0:
        mutated = current.mutate()
        if accept(T, env, current, mutated): 
            current = mutated 
        fitness_curve.append(env.fitness(current))
        T -= 1
        i -= 1
        
    return current,fitness_curve


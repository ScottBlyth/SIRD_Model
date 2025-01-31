# -*- coding: utf-8 -*-
"""
Created on Wed Jan 29 18:29:42 2025

@author: scott
"""

import  json 
import numpy as np
from monte_carlo_markov import stochastic_iteration
from country import GraphWorld, gillespie
from disease import disease
import socket


def load_city_graph(jsonString):
    obj = json.loads(jsonString)
    n = len(obj)
    Q = np.zeros((n,n))
    populations = np.zeros(n)
    for key in obj:
        u = int(key)
        populations[u] = obj[key]["population"]
        for v,weight in obj[key]["neighbours"]:
            Q[u][v] = weight  
        Q[u,u] = 1-np.sum(Q[u, np.arange(n)!=u])
    return Q,populations

def load_model(jsonString, disease):
    Q,u = load_city_graph(jsonString)
    model = GraphWorld(Q, u, np.zeros(len(u)), disease, 1)
    return model
    
if __name__ == "__main__":
    with open("SIR/map.json") as file:
        string = file.read()
    d = disease(1, 200, 0.1, 0.01)
    model = load_model(string, d)

    model.nodes[0].current[1] = 10
    gillespie(model, 0, t_max=365, max_iter=10**8)
    

# -*- coding: utf-8 -*-
"""
Created on Wed Jan 29 18:29:42 2025

@author: scott
"""

import  json 
import numpy as np
from country import GraphWorld, gillespie
from disease import disease
from matplotlib import pyplot as plt
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

def get_time(history):
    return [t for t,points in history]

def get_ith(history, i):
    return [points[i] for t,points in history]

def plot(history, indices=None):
    if history is None:
        return
    if indices is None:
        indices = range(4)
    t = get_time(history)
    for i in indices:
        plt.plot(t, get_ith(history, i))
    
    
        
if __name__ == "__main__":
    with open("map.json") as file:
        string = file.read()
    l1,l2 = 0.5,0.1
    d = disease(l1,l2, 0.1, 0)
    model = load_model(string, d)
    model.nodes[0].current[1] = 2
    gillespie(model, 0, t_max=365, max_iter=10**8)
    
    for node in model.nodes:
        plot(node.history,[0,1])
    plt.show()
    

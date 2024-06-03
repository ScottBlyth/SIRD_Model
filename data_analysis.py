#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  3 17:17:56 2024

@author: ningnong
"""
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from matplotlib import pyplot as plt 
from disease import disease 

def projection(diseases,dim):
    pca = PCA(n_components = dim) 
    x = [d.get_params() for d in diseases]
    x = StandardScaler().fit_transform(x)
    pc = pca.fit_transform(x)
    return pc

def plot_diseases(env, disease_lst, dim, colour): 
    
    diseases = []
    indices = []
    for l in disease_lst:
        diseases += l
        indices.append(len(diseases)-1)
    
    max_fitness = max(env.fitness(d) for d in diseases)
    min_fitness = min(env.fitness(d) for d in diseases)
    difference = max_fitness-min_fitness
    sizes = [200*(max_fitness-env.fitness(d))/difference for d in diseases]
    pc = projection(diseases, dim).T
    #https://www.geeksforgeeks.org/3d-scatter-plotting-in-python-using-matplotlib/
    
    for i in indices:
        if dim == 2:
            plt.scatter(pc[0],pc[1], sizes=sizes)
        if dim == 3:
            fig = plt.figure(figsize = (10, 7))
            ax = plt.axes(projection ="3d")
            ax.scatter3D(pc[0],pc[1], pc[2], 
                         color=colour,sizes=sizes)
        
    
    

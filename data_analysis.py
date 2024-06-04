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
import numpy as np

def projection(diseases,dim):
    pca = PCA(n_components = dim) 
    x = [d.get_params() for d in diseases]
    x = StandardScaler().fit_transform(x)
    pc = pca.fit_transform(x)
    return pc

def plot_diseases(env, disease_lst, dim, colours): 
    
    diseases = []
    indices = []
    for lst in disease_lst:
        indices.append(len(diseases))
        diseases += lst
    
    max_fitness = max(env.fitness(d) for d in diseases)
    min_fitness = min(env.fitness(d) for d in diseases)
    difference = max_fitness-min_fitness
    sizes = [200*(env.fitness(d)-min_fitness)/difference for d in diseases]
    proj = projection(diseases, dim)
    fig = plt.figure(figsize = (10, 7))
    ax = plt.axes(projection ="3d")
    #https://www.geeksforgeeks.org/3d-scatter-plotting-in-python-using-matplotlib/
    for i,index in enumerate(indices):
        next_ = indices[i+1] if i+1<len(indices) else len(diseases) 
        pc = proj[index:next_]
        if dim == 2:
            plt.scatter(pc[0],pc[1], sizes=sizes[index:next_])
        if dim == 3:
            ax.scatter3D(pc.T[0],pc.T[1], pc.T[2], 
                         color=colours[i],sizes=sizes[index:next_])
        
    
    

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
    pc = pca.fit_transform(x)
    return pc

def plot_diseases(diseases, dim): 
    pc = projection(diseases, dim)
    #https://www.geeksforgeeks.org/3d-scatter-plotting-in-python-using-matplotlib/
    if dim == 2:
        plt.scatter(pc[0],pc[1])
    if dim == 3:
        fig = plt.figure(figsize = (10, 7))
        ax = plt.axes(projection ="3d")
        ax.scatter3D(pc[0],pc[1], pc[2], 
                     color="red")
        
    
    

# -*- coding: utf-8 -*-
"""
Created on Wed Jan 29 13:15:38 2025

@author: scott
"""

import numpy as np 

def traverse(Q, initial): 
    next_ =  np.random.choice(np.arange(Q.shape[0]), p=Q[initial])
    return next_

def stochastic_iteration(Q, u, k=2): 
    n = Q.shape[0]
    # construct the expected next distribution 
    u_next = np.copy(u)
    proportion = np.zeros(n)
    for i in range(n): 
        proportion[i] = 1-Q[i,i] 
    to_travel = k*proportion*u_next 
    Q_new = np.copy(Q)
    for i in range(n):
        s = np.sum(Q[i,np.arange(n)!=i])
        # normalise
        Q_new[i] = Q[i]/(s*k)
        Q_new[i,i] = 1 - np.sum(Q_new[i,np.arange(n)!=i])
    update = np.zeros(n)
    for i in range(n): 
        num = int(to_travel[i])+1
        for _ in range(num):
            next_ = traverse(Q_new, i)
            if next_ != i:
                update[next_] += 1
                update[i] -= 1
    u_next += update.astype('int32') 
    return abs(u_next)
    

# -*- coding: utf-8 -*-
"""
Created on Fri May 17 11:47:01 2024

@author: scott
"""
import numpy as np
from matplotlib import pyplot as plt

# utils 

def fmap_vec(functions): 
    def wrapped_function(**args):
        lst = [] 
        for func in functions: 
            lst.append(func(args))
        return np.array(lst) 
    return wrapped_function

# from workshop/lectures
def gillespie(events, event_consequences, Y0, t0, t_max=100):
    y, t = Y0, t0
    Y, T = np.array(Y0), [t]
    while t<t_max:
        p = propensities(t, y, events=events)
        p_rel = p/sum(p)
        tte = [time_to_event(p[i]) for i in range(len(p))]
        idx = np.random.choice(range(len(p)), p=p_rel)
        event, dt = event_consequences[idx], tte[idx]
        y = event(t, y)
        t += dt    
        T += [t]
        Y = np.vstack([Y, y])
    return T, Y

time_to_event = lambda p: (-1/p)*np.log(np.random.random())

def propensities(t, y, events):
    e_ = []
    for event in events:
        e = event(t=t, y=y)
        e_.append(e)
    return e_

class Country:
    def __init__(self, birth_rate, y_0, disease): 
        self.current = y_0 
        self.disease = disease 
        self.birth_rate = birth_rate
        self.neighbours = []
        
    def add_neighbour(self, l_i_j, l_j_i, country):
        self.neighbours.append((l_i_j, l_j_i, country))
        
    def get_SIRD_events(self): 
        S,I,R,D = self.current
        l1,l2,l3,l4 = self.disease.get_params()
        S_to_I = lambda t, y : l1*S*I 
        I_to_R = lambda t, y : l2*I
        R_to_S = lambda t, y : l4*R 
        I_to_D = lambda t, y : l3*I  
        
        props = lambda t, y : fmap_vec([S_to_I(t,y), I_to_R(t,y), R_to_S(t,y), I_to_D(t,y)])
        
        return np.array([S_to_I, I_to_R])
        
        
    def events(self): 
        S,I,R,D = self.current
        l1,l2,l3,l4 = self.disease.get_params()
        beta = self.birth_rate 
        
        dSdt = lambda t,y : -l1*S*I + l4 * R + beta 
        dIdt = lambda t,y : l1*S*I - l2*I - l3*I 
        dRdt = lambda t,y : l2*R - l4 * R 
        dDdt = lambda t,y : l3*I
        dYdt = lambda t,y : np.array([dSdt(t,y), dIdt(t, y), dRdt(t,y), dDdt(t,y)])
        return dYdt
    
    def event_consequences(self): 
        S,I,R,D = self.current
        
        
        
    


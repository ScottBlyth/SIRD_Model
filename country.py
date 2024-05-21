# -*- coding: utf-8 -*-
"""
Created on Fri May 17 11:47:01 2024

@author: scott
"""
import numpy as np
from matplotlib import pyplot as plt
from disease import disease

# utils 

def fmap_vec(functions): 
    def wrapped_function(**args):
        lst = [] 
        for func in functions: 
            lst.append(func(args))
        return np.array(lst) 
    return wrapped_function

# from workshop/lectures
def gillespie(Y0, t0, t_max=100, max_iter=10**4):
    y, t = Y0, t0
    Y, T = np.array(Y0.get_info()), [t]
    i = 0
    while t<t_max and i <= max_iter:
        events,event_consequences = y.get_SIRD_events()
        p = propensities(t, y, events=events)
        p_rel = p/sum(p)
        tte = [time_to_event(p[i]) for i in range(len(p))]
        idx = np.random.choice(range(len(p)), p=p_rel)
        event, dt = event_consequences[idx], tte[idx]
        event(t)
        t += dt    
        T += [t]
        Y = np.vstack([Y, y.get_info()])
        i += 1
    return T, Y

time_to_event = lambda p: (-1/p)*np.log(np.random.random())

def propensities(t, y, events):
    e_ = []
    for event in events:
        e = event(t=t)
        e_.append(e)
    return e_

class Country:
    def __init__(self, birth_rate, y_0, infection : disease): 
        # self.current = [S,I,R,D]
        self.current = y_0 
        self.disease = infection 
        self.birth_rate = birth_rate
        self.neighbours = []
        
    def copy(self):
        c = Country(self.birth_rate, self.current, self.disease)
        # in the future, copy neighbours to
        return c 
    
    def get_info(self): 
        return np.copy(self.current)
        
    def add_neighbour(self, l_i_j, l_j_i, country):
        self.neighbours.append((l_i_j, l_j_i, country))
        
    def move_i_to_j(self, i, j):
        if self.current[i] == 0:
            return
        self.current[i] -= 1 # S
        self.current[j] += 1 # I 
        
    def get_SIRD_events(self): 
        S,I,R,D = self.current
        l1,l2,l3,l4 = self.disease.get_params()
        S_to_I = lambda t : l1*S*I 
        I_to_R = lambda t : l2*I
        R_to_S = lambda t : l4*R 
        I_to_D = lambda t : l3*I  
        props = np.array([S_to_I, I_to_R, R_to_S, I_to_D])
        # consequences
        event_S_I = lambda t : self.move_i_to_j(0, 1)
        event_I_R = lambda t : self.move_i_to_j(1, 2)
        event_R_S = lambda t : self.move_i_to_j(2, 0)
        event_I_D = lambda t : self.move_i_to_j(1, 3)
        
        events = np.array([event_S_I, event_I_R, event_R_S, event_I_D])
        
        return props,events
        
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
        
    
if __name__ == "__main__":
    d = disease(0.00005, 1, 0.002, 0.00001)
    c = Country(1, np.array([10**5, 100, 0, 0]), d)
    T,Y = gillespie(c, 0,  t_max=100, max_iter=10**7)
    plt.plot(T,Y)
    plt.legend(["S", "I", "R", "D"])
    
    
    


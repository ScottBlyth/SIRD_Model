# -*- coding: utf-8 -*-
"""
Created on Fri May 17 11:47:01 2024

@author: scott
"""
import numpy as np
from matplotlib import pyplot as plt
from disease import disease
from bisect import bisect_left 

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
    #Y, T = np.array(Y0.get_info()), [t]
    T = [t]
    i = 0
    while t<t_max and i <= max_iter:
        events,event_consequences = y.get_events()
        p = propensities(t, y, events=events)
        p_rel = p/sum(p)
        tte = [time_to_event(p[i]) for i in range(len(p))]
        idx = np.random.choice(range(len(p)), p=p_rel)
        event, dt = event_consequences[idx], tte[idx]
        event(t)
        t += dt    
        T += [t]
        #Y = np.vstack([Y, y.get_info()])
        i += 1
    return None

time_to_event = lambda p: (-1/p)*np.log(np.random.random())

def propensities(t, y, events):
    e_ = []
    for event in events:
        e = event(t=t)
        e_.append(e)
    return e_

class Country:
    mu = 10
    def __init__(self, id: int, birth_rate, y_0, infection : disease): 
        # self.current = [S,I,R,D]
        self.current = y_0 
        self.disease = infection 
        self.birth_rate = birth_rate
        self.neighbours = []
        self.id = id
        self.history = np.array([y_0])
        self.times = [0]
        
    def copy(self):
        c = Country(self.birth_rate, self.current, self.disease)
        # in the future, copy neighbours to
        return c 
    
    def get_info(self): 
        return np.copy(self.current)
        
    def add_neighbour(self, l_i_j, l_j_i, country):
        self.neighbours.append((l_i_j, l_j_i, country))
        
    def move_i_to_j(self, i, j, t):
        if self.current[i] == 0:
            return
        self.current[i] -= 1 # S
        self.current[j] += 1 # I 
        self.times.append(t)
        self.history = np.vstack([self.history, self.get_info()])
        
    def move_to_country(self, SIRD_index, neighbour): 
        # locate neighbour 
        l1,l2,country = self.neighbours[neighbour]
        country.current[SIRD_index] += 1
        self.current[SIRD_index] -= 1
        
    
    def get_SIRD_events(self): 
        S,I,R,D = self.current
        l1,l2,l3,l4 = self.disease.get_params()
        S_to_I = lambda t : l1*S*I 
        I_to_R = lambda t : l2*I
        R_to_S = lambda t : l4*R 
        I_to_D = lambda t : l3*I  
        props = np.array([S_to_I, I_to_R, R_to_S, I_to_D])
        # consequences
        event_S_I = lambda t : self.move_i_to_j(0, 1, t)
        event_I_R = lambda t : self.move_i_to_j(1, 2, t)
        event_R_S = lambda t : self.move_i_to_j(2, 0, t)
        event_I_D = lambda t : self.move_i_to_j(1, 3, t)
        
        events = np.array([event_S_I, event_I_R, event_R_S, event_I_D])
        
        return props,events
    
    def country_to_country(self): 
        # propensties
        lst = []
        for l1,l2,c in self.neighbours: 
            lst.append(lambda t : l1*self.current[0]) # S 
            lst.append(lambda t : l1*self.current[1]/Country.mu) # I 
            lst.append(lambda t : l1*self.current[2]) # R 
        props = np.array(lst)
        events = []
        for i,val in enumerate(self.neighbours):
            l1,l2,c = val
            events.append(lambda t : self.move_to_country(0, i))
            events.append(lambda t : self.move_to_country(1, i))
            events.append(lambda t : self.move_to_country(2, i))
        events = np.array(events)
        return props,events
        
    def get_events(self): 
        p1,e1 = self.get_SIRD_events()
        p2,e2 = self.country_to_country()
        p = np.concatenate([p1,p2])
        e = np.concatenate([e1,e2])
        return p,e
    
    def event_consequences(self): 
        S,I,R,D = self.current
        
    
class World:
    def __init__(self, countries):
        self.countries  = countries
        
    def get_events(self):
        props = []
        events = []
        for c in self.countries: 
            p,e = c.get_events() 
            props += list(p) 
            events += list(e)
        props = np.array(props)
        events = np.array(events)
        return props,events
    
if __name__ == "__main__":
    d = disease(0.000005, 0.1, 0.0002, 0.0001)
    c = Country(0,1, np.array([10**5, 100, 0, 0]), d)
    c2 = Country(0,1, np.array([10**5, 0, 0, 0]), d)
    c.add_neighbour(0.05, 0.05, c2)
    c2.add_neighbour(0.05, 0.05, c)
    gillespie(World([c,c2]), 0,  t_max=365, max_iter=10**6)
    w = World([c,c2])
    
    
    


# -*- coding: utf-8 -*-
"""
Created on Fri May 17 11:47:01 2024

@author: scott
"""
import numpy as np
from matplotlib import pyplot as plt
from disease import disease
from bisect import bisect_left 
import time 

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
        #Y = np.vstack([Y, y.get_info()])
        i += 1

time_to_event = lambda p: (-1/p)*np.log(np.random.random())

def propensities(t, y, events):
    e_ = []
    for event in events:
        e = event(t=t)
        e_.append(e)
    return e_

class Country:
    mu = 5
    def __init__(self, id: int, birth_rate, y_0, infection : disease, plot=False): 
        # self.current = [S,I,R,D]
        self.current = y_0 
        self.disease = infection 
        self.birth_rate = birth_rate
        self.neighbours = []
        self.id = id
        self.history = np.array([y_0])
        self.times = [0]
        self.plot = plot
        
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
        if self.plot:
            self.times.append(t)
            self.history = np.vstack([self.history, self.get_info()])
        
    def move_to_country(self, SIRD_index, neighbour, t):
        # locate neighbour 
        if self.current[SIRD_index] == 0:
            return
        l1,l2,country = self.neighbours[neighbour]
        country.current[SIRD_index] += 1
        self.current[SIRD_index] -= 1
        if self.plot:
            self.times.append(t)
            self.history = np.vstack([self.history, self.get_info()])
    
    def get_SIRD_events(self): 
        S,I,R,D = self.current
        l1,l2,l3,l4 = self.disease.get_params()
        S_to_I = lambda t : l1*self.get_info()[0]*self.get_info()[1] 
        I_to_R = lambda t : l2*self.get_info()[1] 
        R_to_S = lambda t : l4*self.get_info()[2] 
        I_to_D = lambda t : l3*self.get_info()[1] 
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
        def func(s, i): 
            def func2(t): 
                vaL = l1*self.get_info()[s]
                return self.move_to_country(s, i, t)
            return func2
        lst = []
        for l1,l2,c in self.neighbours: 
            lst.append(lambda t : l1*self.get_info()[0]) # S 
            lst.append(lambda t : l1*self.get_info()[1]/Country.mu) # I 
            lst.append(lambda t : l1*self.get_info()[2]) # R 
        props = np.array(lst)
        events = []
        for i,val in enumerate(self.neighbours):
            l1,l2,c = val
            events.append(func(0, i))
            events.append(func(1,i))
            events.append(func(2,i))
        events = np.array(events)
        return props,events
        
    def get_events(self): 
        p1,e1 = self.get_SIRD_events()
        p2,e2 = self.country_to_country()
        p = np.concatenate([p1,p2])
        e = np.concatenate([e1,e2])
        return p,e
    
    
class World:
    def __init__(self, countries):
        self.countries  = countries
        self.props = None
        self.events = None
        
    def get_events(self):
        if self.props is not None:
            return self.props,self.events
        props = []
        events = []
        for c in self.countries: 
            p,e = c.get_events() 
            props += list(p) 
            events += list(e)
        props = np.array(props)
        events = np.array(events)
        self.props = props 
        self.events = events
        return props,events
    
# create grid of countries 

def create_grid(disease, country_l, dimensions, plot_output=False):
    n,m = dimensions 
    country_grid = [[None for _ in range(m)] for _ in range(n)]
    for i in range(n):
        for j in range(m):
            c = Country(i*m+j, 0, np.array([10**4, 0,0,0]), disease, plot=plot_output)
            country_grid[i][j] = c
    def get_neighbours(i, j): 
        neighbours = [(i, j-1), (i, j+1),
                      (i-1, j), (i+1,j)]
        return [(i,j) for i,j in neighbours if 0 <= i < n and 0 <= j < m]
    countries = []
    for i in range(n):
        for j in range(m):
            countries.append(country_grid[i][j])
            for i_n,j_n in get_neighbours(i,j):
                country_grid[i][j].add_neighbour(country_l, country_l, country_grid[i_n][j_n])
    return countries, country_grid
    
if __name__ == "__main__":
    d = disease(0.0003, 1, 0.2,  0.01)
    countries,grid = create_grid(d, 0.05, (2,2), True) 
    grid[0][0].current[1] = 3
    w = World(countries)
    start = time.time()
    gillespie(w, 0,  t_max=365*2, max_iter=3*10**5)
    end = time.time() 
    print(end-start)
    
    
    


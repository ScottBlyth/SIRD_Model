# -*- coding: utf-8 -*-
"""
Created on Fri May 17 11:47:01 2024

@author: scott
"""
import numpy as np
from matplotlib import pyplot as plt
from disease import disease
from GI import Environment, evolve
from simulated_annealing import simulated_annealing
from bisect import bisect_left 
import time 
from random import random



# utils 

def fmap_vec(functions): 
    def wrapped_function(**args):
        lst = [] 
        for func in functions: 
            lst.append(func(args))
        return np.array(lst) 
    return wrapped_function

def all_zeros(lst):
    for val in lst:
        if val != 0:
            return False
    return True

# from workshop/lectures
def gillespie(Y0, t0, t_max=100, max_iter=10**4):
    y, t = Y0, t0
    #Y, T = np.array(Y0.get_info()), [t]
    i = 0
    events,event_consequences = y.get_events() 
    while t<t_max and i <= max_iter:
        events,event_consequences = y.get_events()
        p = propensities(t, y, events=events)
        if all_zeros(p):
            return
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
        if len(p2) == 0:
            return p1,e1
        p = np.concatenate([p1,p2])
        e = np.concatenate([e1,e2])
        return p,e
    
def random_interval(i, j):
    return (j-i)*random()+i 
    
def random_vec(n, i,j):
    return [(j-i)*random()+i for _ in range(n)]
    
class GridEnvironemnt(Environment): 
    def __init__(self, country_l, dimensions):
        self.country_l = country_l
        self.n = dimensions 
        self.l1_bounds = (0.0002, 0.0005)
        self.l2_l3_bounds = (0, 3) 
=======
        self.l1_bounds = (0.0002, 0.001)
        self.l2_l3_bounds = (0.5, 3) 
        self.l4_bounds = (0.001, 0.2) 
        self.cache_fitness = {}
        
    def in_bounds(self, l1,l2,l3,l4):
        cond1 = self.l1_bounds[0] <= l1 <= self.l1_bounds[1]
        cond2 = self.l2_l3_bounds[0] <= l2+l3 <= self.l2_l3_bounds[1]
        cond3 = self.l4_bounds[0] <= l4 <= self.l4_bounds[1]
        return cond1 and cond2 and cond3
    
    def random_population(self): 
        l1 = random_interval(self.l1_bounds[0], self.l1_bounds[1])
        l2 = random_interval(self.l2_l3_bounds[0], self.l2_l3_bounds[1]) 
        l3 = random_interval(self.l2_l3_bounds[0], self.l2_l3_bounds[1]) 
        l4 = random_interval(self.l4_bounds[0], self.l4_bounds[1])
        return disease(l1, l2, l3, l4)
    
    
    def fitness_aux(self ,l1,l2,l3,l4): 
        if not self.in_bounds(l1,l2,l3,l4):
            return 1
        d = disease(l1,l2,l3,l4)
        countries,grid = create_grid(d, self.country_l, (self.n,self.n)) 
        grid[0][0].current[1] = 5
        w = World(countries)
        gillespie(w, 0,  t_max=365, max_iter=2*10**5)
        num_deaths = 0 
        for c in countries:
            num_deaths += c.get_info()[3]
        self.cache_fitness[(l1,l2,l3,l4)] = 0 if num_deaths < 0 else num_deaths
        return 0 if num_deaths < 0 else num_deaths
    
    def fitness(self, sol): 
        if sol in self.cache_fitness:
            return self.cache_fitness[sol]
        l1,l2,l3,l4 = sol.to_phenotype()
        self.cache_fitness[sol] = self.fitness_aux(l1, l2, l3, l4)
        return self.cache_fitness[sol]
    
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


def add_curves(curves):
    time_steps = [] 
    for curve in curves:
        time_steps += [t for t,y in curve]
    time_steps = sorted(time_steps)
    resulting_curve = []
    current_indices = [0 for _ in range(len(curves))]
    for t in time_steps:
        # find t value of 
        sum_ = 0
        for i,curve in enumerate(curves):
            index = current_indices[i]
            if index >= len(curve):
                sum_ += curve[index-1][1]
                break
            sum_ += curve[index][1]
            if curve[index][0] <= t:
                current_indices[i] += 1
        resulting_curve.append((t, sum_))
    return [t for t,y in resulting_curve], [y for t,y in resulting_curve]
    

def plot_grid_curves(grid, max_population): 
    n = len(grid) 
    names = []
    deaths = []
    infection_curves = []
    for i in range(n):
        for j in range(n):
            names.append((i,j))
            c = grid[i][j]
            infections = [I for S,I,R,D in c.history]
            inf_curve = [(t, s[1]) for t,s in zip(c.times, c.history)]
            infection_curves.append(inf_curve)
            deaths.append([(t, s[3]) for t,s in zip(c.times, c.history)])
            plt.plot(c.times, infections) 
    cumulative_deaths = add_curves(deaths)
    total_infections = add_curves(infection_curves)
    plt.plot(cumulative_deaths[0], cumulative_deaths[1])
    plt.plot(total_infections[0], total_infections[1])
    plt.legend(names+["Cumulative Deaths", "Total Infections"]) 
    plt.xlim(0, total_infections[0][-1])
    plt.ylim(0, max_population)
    plt.show()
    
def get_x(lst):
    return [i for i in range(len(lst))]
    
if __name__ == "__main__":
    if input("do u want to run things?: ") == 'y':
        population = []
        env = GridEnvironemnt(0.05, 1)
        for _ in range(10):
            initial = env.random_population()
            population.append(initial)
        #evolve(env : Environment, population, iterations)
        #best,plot = simulated_annealing(env, initial, 1000, 1000)
        population,curve = evolve(env, population, 25)
=======
        population,curve = evolve(env, population, 100)
        population = sorted(population, key=lambda x : -env.fitness(x))
    
        d = disease(0.0003, 1, 0.2,  0.01)
        best = population[0]
        countries,grid = create_grid(best, 0.05, (2,2), True) 
        grid[0][0].current[1] = 5
        grid[1][1].current[0] = 20000
        w = World(countries)
        start = time.time()
        gillespie(w, 0,  t_max=365, max_iter=3*10**5)
        end = time.time() 
        print(end-start)
        plot_grid_curves(grid, 50*1000)
        
    
    
    


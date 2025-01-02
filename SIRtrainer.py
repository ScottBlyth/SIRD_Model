#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 16 20:59:07 2024

@author: scott
"""

from scipy.integrate import odeint 
import numpy as np
from matplotlib import pyplot as plt
from sklearn.metrics import mean_squared_error
from sklearn.base import BaseEstimator
from sklearn.model_selection import cross_val_score, KFold

# dS/dt = -l1*S*I 
# dI/dt = l1*S*I - l2*I 
# dR/dt = l2*I 

def SIRModel(l1,l2):
    def dydt(y,t):
        N = sum(y)
        S,I,R = y
        dsdt = -l1*S*I/N 
        dIdt = l1*S*I/N - l2*I
        dRdt = l2*I
        return np.array([dsdt, dIdt, dRdt])
    return dydt   

# uses simulated annealing to fit
class SIR_Estimator(BaseEstimator): 
    def __init__(self, y0=np.array([10**4, 1, 0]), sd=1, max_iterations=1000, temp_factor=1.01):
        self.sd = sd
        self.max_iterations = max_iterations
        self.temp_factor = temp_factor
        self.y0 = y0
        
    def test_bounds(self, X, bounds, points=10, errors=[], ls=[]): 
        # bounds[0][0] < x < bounds[1][0]
        # bounds[0][1] < y < bounds[1][1]
        y0 = self.y0
        for _ in range(points):
            l1 = abs(np.random.rand()*(bounds[1][0] - bounds[0][0]) + bounds[0][0])
            l2 = abs(np.random.rand()*(bounds[1][1] - bounds[0][1]) + bounds[0][1])
            
            model = SIRModel(l1, l2) 
            y_pred = odeint(model, y0=y0, t=X)
            error = mean_squared_error(y, y_pred) 
            errors.append(error)
            ls.append(np.array([l1,l2]))
        min_ = np.argmin(errors)
        return errors, np.array(ls), ls[min_]
        
    def fit(self, X, y): 
        # X = S,I,R
        # np.random.normal()
        bounds = np.array([[0,0], [1,1]])
        best_bounds = bounds
        y0 = y[0]
        T = 1000
        l1,l2 = np.mean(bounds, axis=0)
        model = SIRModel(l1, l2) 
        y_pred = odeint(model, y0=y0, t=X)
        best_error = float('inf')
        
        best_l = None
        
        for _ in range(self.max_iterations):
            
            errors, ls,min_ = self.test_bounds(X, best_bounds,points=500)
            sort_indices = sorted(np.arange(0, len(errors)), key=lambda i : errors[i])
            sort_indices = np.array(sort_indices,dtype=int)
            n = 25
            top_half = ls[sort_indices[:n]]
            
            # left point 
            x1 = np.min(top_half.T[0])+np.random.normal(scale=self.sd)
            y1 = np.min(top_half.T[1])+np.random.normal(scale=self.sd)
            x2 = np.max(top_half.T[0])+np.random.normal(scale=self.sd)
            y2 = np.max(top_half.T[1])+np.random.normal(scale=self.sd)
            bounds = np.array([[x1,y1], 
                               [x2,y2]])
            
            
            # compute fitness 
            errors, ls,best_l = self.test_bounds(X, bounds,points=100)
            mean_error = np.mean(errors)
            if mean_error < best_error: 
                best_error = mean_error
                best_bounds = bounds
            else:
                # accept with probability e^-((best-error)/T)
                if np.exp(-(mean_error-best_error)/T) > np.random.rand():
                    # accept! 
                    best_bounds = bounds
                    best_error = mean_error
            T *= self.temp_factor
        
        
        errors, ls,best_l = self.test_bounds(X, best_bounds,points=100) 
        self.l1,self.l2 = best_l
        
        model = SIRModel(self.l1,self.l2)
        y_pred = odeint(model, y0=self.y0, t=X)
        error_ = mean_squared_error(y, y_pred)
        
        print(f"SQR MSE: {np.sqrt(error_)}")
        print(T)
        print(best_bounds)
        print(np.mean(best_bounds, axis=0))
        return self
    
    def predict(self, X): 
        # sort X and y by X 
        y0 = self.y0
        y = odeint(SIRModel(self.l1,self.l2), y0=y0, t=X) 
        return y
    
    
def sigmoid(x):
  return 1 / (1 + np.exp(-x))

def logit(x):
    return np.log(x/(1-x))

def transform(k):
    def f(p):
        points = []
        for x,y in p:
            scaling = k*x+1
            points.append(np.array([scaling*y, y]))
        return np.array(points)
    return f

def inverse_transform(k):
    def f(p):
        points = []
        for x,y in p:
            result = np.array([(x-y)/(k*y), y]) 
            points.append(result)
        return np.array(points)
    return f
    

class SIR_CrossEntropy(BaseEstimator):
    def __init__(self, max_iterations=50, n_samples=100, elite_size=10):
        self.max_iterations = max_iterations
        self.n_samples = n_samples 
        self.elite_size = elite_size
        
    def score(self, point, y0, X, y):
        try:
            l1,l2 = point 
            model = SIRModel(l1,l2)
            y_pred = odeint(model, y0=y0, t=X)
            return mean_squared_error(y, y_pred) 
        except:
            return 10**6
        
    
    def predict(self, X, y0=np.array([10**4, 1, 0])):
        model = SIRModel(self.l1,self.l2)
        y_pred = odeint(model, y0=y0, t=X)
        return y_pred
        
    def fit(self, X, y): 
        x_p = np.random.uniform(low=-2, high=0, size=self.n_samples)
        y_p = np.random.uniform(low=-2, high=0, size=self.n_samples)
        p = np.array([x_p,  y_p]).T
        mu = np.mean(p, axis=0)
        cov = np.cov(p, rowvar=0)
        y0 = y[0]
        # 
        best_found = None
        best = 10**7
        for _ in range(self.max_iterations):
            # sample self.n_sample points
            points = transform(5)(sigmoid(np.random.multivariate_normal(mean=mu, cov=cov, size=self.n_samples)))
            scores = [self.score(point, y0, X, y) for point in points]
            sort_points_idx = sorted(np.arange(0, self.n_samples), key=lambda i : scores[i])
            elites = points[sort_points_idx[:self.elite_size]]
            
            if best_found is None or self.score(elites[0], y0, X, y) < best:
                best_found = elites[0]
            
            # fit multi variate gaussian distribution around the elite samples 
            elite_logits = inverse_transform(5)(elites)
            elite_logits = logit(elite_logits)
            mu = np.mean(elite_logits, axis=0)
            cov = np.cov(elite_logits, rowvar=0)
        print(best_found)
        self.l1,self.l2 = best_found # get the best elite
        self.y0 = y0
        self.mu = mu
        self.cov = cov
        return self
    
if __name__ == "__main__":
    # create synthetic data 
    plt.show()
    l1,l2 = 0.3, 0.1
    y0 = np.array([10**5, 1, 0])
    model = SIRModel(l1,l2)
    X = np.arange(0, 125, 0.5)
    y = odeint(model, y0, X)
    noise = np.array([np.random.normal(scale=3000, size=3) for _ in range(len(y))])
    noise2 = np.array([np.random.normal(scale=1) for _ in range(len(X))])
    y += noise 
    #X += noise2
    
    for i in range(len(y[0])):
        plt.scatter(X, y.T[i], s=1)
    plt.legend(["S", "I", "R"])
    
    temps = np.arange(0.98, 1, 0.005)
 
    estimator = SIR_CrossEntropy(max_iterations=5, n_samples=100, elite_size=10)
    model = estimator.fit(X, y)
    y_pred = model.predict(X, y0=np.array([10**5, 1, 0]))
    plt.plot(X, y_pred)
    plt.show()
      
    
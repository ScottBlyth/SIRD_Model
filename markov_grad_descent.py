# -*- coding: utf-8 -*-
"""
Created on Tue Jan  7 15:32:17 2025

@author: scott
"""
import numpy as np
from matplotlib import pyplot as plt

def sigmoid(x):
    return 1/(1+np.exp(x))

def logit(x):
    return -np.log(x/(1-x))

def predict_(x):
    l1,l2,l3 = logit(x) 
    return predict(l1,l2,l3)

def predict(l1,l2,l3):
    p1,p2,p3 = sigmoid(np.array([l1,l2,l3]))
    d = p1*p2
    r = 1-p1 + p1*(1-p2-p3)
    ep = p1*p3 
    return d,r,ep 

def gradient(l1,l2,l3, y): 
    y_pred = predict(l1,l2,l3)
    error = y-y_pred 
    J = np.zeros((3,3)) 
    p1,p2,p3 = sigmoid(np.array([l1,l2,l3]))
    J[0] = np.array([ p1*(1-p1)*p2, p2*(1-p2)*p1, 0 ])
    J[1] = np.array([ -p1*(1-p1)+p1*(1-p1)*(1-p2-p3), -p2*(1-p2)*p1, -p3*(1-p3)*p1])
    J[2] = np.array([ p1*(1-p1)*p3, 0, p3*(1-p3)*p1 ])
    return J.T @ error 
    
def grad_descent(y=np.array([0.1, 0.5, 0.4]), max_iterations=10**5, epsilon=0.001, learning_rate=0.01):
    l1,l2,l3 = np.ones(3)
    points = []
    errors = []
    for _ in range(max_iterations): 
        next_l = np.array([l1,l2,l3]) - learning_rate*gradient(l1, l2, l3, y)
        l1,l2,l3 = next_l 
        y_pred = predict(l1,l2,l3)
        points.append(sigmoid(next_l))
        error =  np.linalg.norm(y_pred - y)
        errors.append(error**2)
        if error <= epsilon:
            print(f"error: {np.linalg.norm(y_pred - y) }")
            print(predict(l1,l2,l3))
            return sigmoid(np.array([l1,l2,l3]))
    print(f"error: {np.linalg.norm(y_pred - y) }")
    print(predict(l1,l2,l3))
    points = np.array(points)
    errors = np.array(errors)
    plt.plot(errors)
    plt.ylim([0, errors[0]+0.1])
    plt.show() 
    return sigmoid(np.array([l1,l2,l3]))
    
if __name__ == "__main__":
    p1,p2,p3 = grad_descent(y=np.array([0.1, 0.7, 0.2]))

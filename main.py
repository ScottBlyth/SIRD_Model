# -*- coding: utf-8 -*-
"""
Created on Wed Jan 29 18:29:42 2025

@author: scott
"""

import  json 
import numpy as np
from country import GraphWorld, gillespie
from disease import disease
from matplotlib import pyplot as plt
import socket
import regex
import json

def load_city_graph(jsonString):
    obj = json.loads(jsonString)
    n = len(obj)
    Q = np.zeros((n,n))
    populations = np.zeros((n,4))
    for key in obj:
        u = int(key)
        populations[u] = obj[key]["population"]
        for v,weight in obj[key]["neighbours"]:
            Q[u][v] = weight  
        Q[u,u] = 1-np.sum(Q[u, np.arange(n)!=u])
    return Q,populations

def load_model(jsonString, disease):
    Q,u = load_city_graph(jsonString)
    model = GraphWorld(Q, u, disease, 1)
    return model

def listen(port, disease):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    s.connect(('localhost', port))
    print("connected...")
    data = s.recv(1024).decode(errors='ignore')
    s.close()
    print("Received data...")
    # read from first "{" 
    idx = regex.search(r"{.*}$", data)
    data = data[idx.start():idx.end()+1]
    return load_model(data, disease)

def server(port, d):
    s = socket.socket()  
    s.bind(('localhost', port))    
    print("server started...")
    s.listen(5)
    
    while True:
        c, addr = s.accept()
        print("Client Accepted!")
        data = c.recv(1024).decode(errors='ignore')
        print("Received model state...")
        idx = regex.search(r"num\d+", data)
        time = int(data[idx.start()+3:idx.end()])
        
        idx = regex.search("{.*}$", data)
        obj = data[idx.start():idx.end()+1]
        model = load_model(obj, d)
        
        model.nodes[0].current[1] = 2
        
        gillespie(model, 0, t_max=time, max_iter=10**8)
        print("Model finished exceution...")
        points = {}
        for node in model.nodes:
            points[str(node.id)] = {"population" : list(node.current), "points" : []}
            if node.history is None:
                continue
            for p in node.history:
                p_ = list(p)
                p_[1] = list(p[1])
                points[str(node.id)]["points"].append(p_)
        string = json.dumps(points)

        c.send(string.encode("utf-8"))
        print("Sent!")
        c.close()
    s.close()
        
    

def get_time(history):
    return [t for t,points in history]

def get_ith(history, i):
    return [points[i] for t,points in history]

def plot(history, indices=None):
    if history is None:
        return
    if indices is None:
        indices = range(4)
    t = get_time(history)
    for i in indices:
        plt.plot(t, get_ith(history, i))
    

        
if __name__ == "__main__":
    l1,l2 = 0.5,0.1
    d = disease(l1,l2, 0.1, 0.01)
    server(6666, d)


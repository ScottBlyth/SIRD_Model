# -*- coding: utf-8 -*-
"""
Created on Tue May 21 15:40:32 2024

@author: scott
"""



class disease: 
    def __init__(self, l1,l2,l3,l4):
        # l1 : infection rate
        # l2 : recovery rate
        # l3 : immunity 
        # l4 : mortality rate
        self.l1,self.l2,self.l3,self.l4 = l1,l2,l3,l4 
        
    def get_params(self):
        return self.l1,self.l2,self.l3,self.l4

    def copy(self):
        return disease(self.l1,self.l2,self.l3,self.l4)
    

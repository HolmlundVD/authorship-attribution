#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 23 15:01:15 2021

@author: fshiranichaharsooghi
 """
import numpy as np
import math

def KLD(P,Q,eps):    
    D=0    
    
    for i in range(len(P)):
        for j in range(len(P[i])):  
            if Q[i][j]:  
                #if(P[i][j]*math.log(P[i][j]/Q[i][j],2)<0):
                    
                    #print(P[i][j])
                    #print(Q[i][j])
                    #print(math.log(P[i][j]/Q[i][j],2))
                    #print(P[i][j]*math.log(P[i][j]/Q[i][j],2))
                add=P[i][j]*math.log(P[i][j]/Q[i][j],2)
                if add>0:
                    D+=add
            else:   
                #if(P[i][j]*math.log(P[i][j]/eps,2)<0):
                    #print(P[i][j])
                    #print(eps)
                    #print(math.log(P[i][j]/eps,2))
                    #print(P[i][j]*math.log(P[i][j]/eps,2))
                add=P[i][j]*math.log(P[i][j]/eps,2)  
                if add>0:
                    D+=add
    return D
def bhattacharyya_distance(P,Q,eps):
    D=0
    for token in P.keys():
        if token in Q.keys():
            D+=Math.sqrt(P[token])*Math.sqrt(Q[token])

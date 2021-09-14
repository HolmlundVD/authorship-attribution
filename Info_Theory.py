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
    
    for token in P.keys():
        if token in Q.keys():                   
            D=D+P[token]*math.log(P[token]/Q[token],2)
        else:
            D=D+P[token]*math.log(P[token]/eps,2)   
    return D

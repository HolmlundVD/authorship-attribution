import nltk
from binarytree import Node
import string
from compression import compression as comp
import functools
from dahuffman import HuffmanCodec as codec
import numpy as np
import traceback
from treelib import Tree as tr,Node as nd
import re
import math
#
#A ppm_compressor is initialized by providing a text list, order number, and escape value
#you can then provide the object a second text and it will return the cost of compressing it using the ppm_compression
#of the first text
#
class ppm_compressor(object):
    #
    #creates a frequency tree from the specific text that tells the frequency of each character in context
    #the context gets as long as the int order provided
    #the escape value in each context will equal the provided parameter
    #
    @staticmethod
    def __initialize_tree(order:int,esc_value:int)->dict:       
        tree=tr() 
        root=tree.create_node(identifier="/root_node",data=0)       
        tree.create_node(identifier="/esc",data=1,parent=root)
        root.data=0                 
        return tree
          
    #
    #creates a ppm compressor of the given text using the given context order and 
    #   escape value. constructs a word graph based off of it 
    #The weights parameter is a dictionary that assigns a weight to the character in the total cost calculations
    #based on a regex that is contained in the context
    #
    def __init__(self,text:list,order:int,esc_value:int,weights:dict=None): 
        self.weights=weights
        self.tree=ppm_compressor.__initialize_tree(order,esc_value)                        
        self.order=order+1
        self.esc_value=esc_value
        self.cost=0
        self.analyze_and_append(text)
   
    #
    #takes the text and calculates the cost to compress it given the compression tree of this object
    #without adding it to the original text
    #
    def analyze_without_appending(self,text:list)->int:
        
        temp_tree=tr(self.tree,deep=True)
        total_cost=0      
        current_context=""
        for char in range(len(text)):
            temp_tree.get_node("/root_node").data+=1
            current_context+=text[char]
            found=False     
            temp_context=current_context
            if self.weights is not None:
                self.weight=1
                for regex in self.weights:
                    matches=re.findall(regex.key,temp_context)
                    if len(matches)>0:
                        self.weight*=math.pow(len(matches),regex.value)
            while temp_context is not "":               
                node=temp_tree.get_node(temp_context)
                parent_node=temp_tree.get_node(temp_context[:-1]) or temp_tree.get_node("/root_node")                
                parent_esc=temp_tree[temp_context[:-2]+"/esc"]
                if node is None:                     
                    new_node=temp_tree.create_node(identifier=temp_context,parent=parent_node,data=1)                    
                    if len(temp_context)<self.order:
                        temp_tree.create_node(parent=new_node,data=self.esc_value,identifier=temp_context+"/esc") 
                    
                    total_cost+=ppm_compressor.calculate_token_cost(parent_esc.data,parent_node.data+parent_esc.data)
                else:
                    if found==False:
                       found=True                     
                       node.data+=1                       
                       total_cost+=ppm_compressor.calculate_token_cost(node.data,parent_node.data)                      
                    else:                        
                        node.data+=1               
                temp_context=temp_context[1:]
            if len(current_context)>=self.order:
                current_context=current_context[1:] 
        return total_cost
    
    def analyze_and_append(self,text:list)->int:
        
        temp_tree=self.tree
        total_cost=0      
        current_context=""
        for char in range(len(text)):
            temp_tree.get_node("/root_node").data+=1
            current_context+=text[char]
            found=False     
            temp_context=current_context
            if self.weights is not None:
                self.weight=1
                for regex in self.weights:
                    matches=re.findall(regex.key,temp_context)
                    if len(matches)>0:
                        self.weight*=math.pow(len(matches),regex.value)
            while temp_context is not "":               
                node=temp_tree.get_node(temp_context)
                parent_node=temp_tree.get_node(temp_context[:-1]) or temp_tree.get_node("/root_node")                
                parent_esc=temp_tree[temp_context[:-2]+"/esc"]
                if node is None:                     
                    new_node=temp_tree.create_node(identifier=temp_context,parent=parent_node,data=1)                    
                    if len(temp_context)<self.order:
                        temp_tree.create_node(parent=new_node,data=self.esc_value,identifier=temp_context+"/esc") 
                    
                    total_cost+=ppm_compressor.calculate_token_cost(parent_esc.data,parent_node.data+parent_esc.data)
                else:
                    if found==False:
                       found=True                     
                       node.data+=1                       
                       total_cost+=ppm_compressor.calculate_token_cost(node.data,parent_node.data)                      
                    else:                        
                        node.data+=1               
                temp_context=temp_context[1:]
            if len(current_context)>=self.order:
                current_context=current_context[1:] 
        self.cost+=total_cost
        return total_cost

    def get_cost():
        return self.cost
    #
    #based on the context size and frequency of a token in the context given returns 
    #what the cost to compress said token should be
    #frequency in context must be smaller than context_frequency
    #
    @staticmethod
    def calculate_token_cost(frequency_in_context:int,context_frequency:int)->float:
        if frequency_in_context>context_frequency:
            raise ValueError("frequency_in_context:"+str(frequency_in_context)+"cannot be greater than context_frequency:"+str(context_frequency))
        return np.log2(context_frequency/frequency_in_context)
    
    #
    #given a list of strings(or anything really) returns a dictionary 
    #containing the frequency of each token
    #
    @staticmethod
    def get_token_frequencies(text:list)->dict:
        frequencies=dict()
        for token in text:
            if token in frequencies.keys():
                frequencies[token]+=1
            else:
                frequencies[token]=1
        return frequencies
    #
    #calculates the normalized compression distance between two texts
    #https://en.wikipedia.org/wiki/Normalized_compression_distance
    #
    @staticmethod
    def get_ncd(text1:str,text2:str,order:int,esc_value:int)->int:
        empty=ppm_compressor("",order,esc_value)
        text1_compressed=empty.analyze_without_appending(text1)
        text2_compressed=empty.analyze_without_appending(text2)
        combined=empty.analyze_without_appending(text1+text2)
        if text1_compressed>text2_compressed:           
            return (combined-text2_compressed)/text1_compressed
        else:            
            return (combined-text1_compressed)/text2_compressed
    #
    #when a ppm object already exists calling this method with another text will perform ncd using 
    # this text and the new text provided
    #
    def get_ncd_from_object(text2:str)->int:
        second_compressed=ppm_compressor(text2,self.order,self.esc_value,self.weights)
        combined_compressed=self.analyze_without_appending(text2)
        if self.costs>second_compressed.cost:
            return (combined_compressed-second_compressed.cost)/self.costs
        else:
            return (combined_compressed-self.costs)/second_compressed.costs


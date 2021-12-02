import nltk
from binarytree import Node
import string
from numba import jit
class compression(object):
   
   #
   #takes a dictionary of the frequency of tokens in a set of text and returns a
   # compression object   
   #
   def compress_from_frequencies(frequency_dictionary:dict)->object:
       node_list=[]
       
       for token in frequency_dictionary:          
           node_list.append({"character":token,"frequency":frequency_dictionary[token]})
                         
       node_list=sorted(node_list,key=lambda token:-token["frequency"])
       
       while len(node_list)>1:  
          
          first=node_list.pop()          
          second=node_list.pop()            
          new_node={"character":"InternalNode","frequency":first["frequency"]+second["frequency"],"left":first,"right":second}            
          
          added_to_list_yet=False
          for i in range(len(node_list)):                 
              if new_node["frequency"]>node_list[i]["frequency"]:                  
                  node_list.insert(i,new_node) 
                  added_to_list_yet=True
                  break
          if added_to_list_yet==False:
              node_list.append(new_node) 
       token_costs=dict()       
       max_token_value=compression.__get_costs(token_costs,node_list[0],0)
       return compression(token_costs,max_token_value)
   
   #
   #given a starting node of a tree an empty dictionary and the current depth of a node calculates and returns the 
   # maximum value of a character and fills the dictionary with the cost to compress each token in the tree
   #not meant to be used outside of the compress_from_dict method
   #
   def __get_costs(costs_of_tokens:dict,node:dict,current_depth:int)->int:
       
       if "left" not in node.keys() and "right" not in node.keys():
           costs_of_tokens[node["character"]]=current_depth
           return current_depth
       else:
           left_max=compression.__get_costs(costs_of_tokens,node["left"],current_depth+1)
           right_max=compression.__get_costs(costs_of_tokens,node["right"],current_depth+1)
           if left_max>right_max:
               return left_max
           else:
               return right_max
   def __init__(self,costs:dict,max_val:int):
       self.costs=costs
       self.max_val=max_val
   def get_cost_of_words(self,new_text:str):
       tknz=nltk.RegexpTokenizer(r"\w+")
       cost=0
       words=tknz.tokenize(new_text)
       for word in words:
           if word in self.costs.keys():
               cost+=self.costs[word]
           else:
               cost+=self.max_val
       return cost
   def get_cost_of_characters(self,new_text:str):
       cost=0
       for char in new_text:
           if char in self.costs.keys():
               cost+=self.costs[char]
           else:
               cost+=self.max_val
       return cost
   def calculate_node(node:dict):
       return node["frequency"]
   @staticmethod
   def get_word_frequencies(text:str)->dict:
       tknz=nltk.tokenize.TweetTokenizer()
       words=tknz.tokenize(text)       
       frequencies=dict()
       for word in words:           
           if word in frequencies.keys():              
               frequencies[word]+=1               
           else:
               frequencies[word]=1
       return frequencies
   @staticmethod
   def get_character_frequencies(text:str)->dict:
      
       new_text=text.translate(str.maketrans('', '', "/\n"))
       frequencies=dict()
       for char in new_text:
           if char in frequencies.keys():
               frequencies[char]+=1
           else:
               frequencies[char]=1
       return frequencies
   
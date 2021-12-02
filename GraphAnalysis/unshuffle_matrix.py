import ErdosRenyiGraph as erg
import numpy as np
from numba import jit



@jit
def loop_with_numba(main,correlated,vtm)->int:

    num00=0
    num01=0
    num10=0
    num11=0
    num=len(main)    
    for k in range(num):
        first=main[k]
        second=correlated[k]
        if first==0 and second==0:                
           num00+=1 
        elif first==0 and second==1:
           num01+=1
        elif first==1 and second==0:
           num10+=1
        elif  first==1 and second==1:
           num11+=1
    
    return abs(num00/num-vtm[0])+abs(num01/num-vtm[1])+abs(num10/num-vtm[2])+abs(num11/num-vtm[3])
#goes in order 00 01 10 11
def unshuffle_matrix(correlated_graph:np.array,to_unshuffle:np.array,shuffled_rows:np.array,probabilities:np.array):
    
    if not len(probabilities)==4:
        raise ValueError("probabilities is not of size 4")
    sum=0
    for n in probabilities:           
        sum+=n
        if sum<0.995 or sum>1.005:          
            raise ValueError("sum of probabilities is not 1")
    if not erg.ErdosRenyiGraph.isSymmetrical(to_unshuffle):
            raise ValueError("Graph is not symmetrical")
    value_to_match=0.5*((probabilities[0]+probabilities[1])*(probabilities[0]+probabilities[2])+probabilities[0])
    for i in shuffled_rows:
        smallest_error=sys.maxsize 
        smallest_error_index=-1
        for j in shuffled_rows:
            num00=0
            num=0
            for k in range(len(to_unshuffle)):
                if to_unshuffle[i][k]==0 and correlated_graph[j][k]==0:
                    num00+=1
                num+=1
            row_score=abs(num00/num-value_to_match)
            if row_score<smallest_error:
                smallest_error=row_score
                smallest_error_index=j
        temp=shuffled_rows[smallest_error_index]
        shuffled_rows[smallest_error_index]=shuffled_rows[i]
        shuffled_rows[i]=temp
def get_unshuffle_matchings(correlated_graph:np.array,to_unshuffle:np.array,shuffled_rows,probabilities:np.array,remove_later)->dict:
    
    matchings=dict()
    candidate_rows=shuffled_rows.copy()    
    for row in shuffled_rows:
        matchings[row]=row

    if not len(probabilities)==4:
       
        raise ValueError("probabilities is not of size 4")
    sum=0
    for n in probabilities:                 
        sum+=n
    if sum<0.995 or sum>1.005: 
        
        raise ValueError("sum of probabilities is not 1")
    if not erg.ErdosRenyiGraph.isSymmetrical(to_unshuffle):
        raise ValueError("Graph is not symmetrical")
    value_to_match00=0.5*((probabilities[0]+probabilities[1])*(probabilities[0]+probabilities[2])+probabilities[0])
    value_to_match01=0.5*((probabilities[0]+probabilities[1])*(probabilities[1]+probabilities[3])+probabilities[1])
    value_to_match10=0.5*((probabilities[2]+probabilities[3])*(probabilities[0]+probabilities[2])+probabilities[2])
    value_to_match11=0.5*((probabilities[2]+probabilities[3])*(probabilities[1]+probabilities[3])+probabilities[3])
    count=0
    for i in shuffled_rows:
        
        smallest_error=4
        smallest_error_index=-1
        num=len(to_unshuffle[i])
        count+=1
        print(count)
        count2=0
        for j in range(len(candidate_rows)):
            row_score=loop_with_numba(to_unshuffle[i].astype(int),correlated_graph[candidate_rows[j]].astype(int),np.array([value_to_match00,value_to_match01,value_to_match10,value_to_match11]))
            count2+=1
           
            #combined=list(zip(to_unshuffle[i],correlated_graph[candidate_rows[j]]))
           
            #num00=len([x for x in combined if x[0]==0 and x[1]==0])
            
            #num01=len([x for x in combined if x[0]==0 and x[1]==1])
            #num10=len([x for x in combined if x[0]==1 and x[1]==0])
            #num11=len([x for x in combined if x[0]==1 and x[1]==1])
            
            
            #for k in range(num):
             #   first=comparing_row[k]
              #  second=correlated_row[k]
               # if first==0 and second==0:
                
           #num00+=1 
            #    elif first==0 and second==1:
             #       num01+=1
              #  elif first==1 and second==0:
               #     num10+=1
                #elif  first==1 and second==1:
                 #   num11+=1
           
            
            
           # print(str(i)+" , "+str(j))
            #print(bool(remove_later[i]==j))
            #print(row_score)
            #print(num00)
            #print(num)
            #print(value_to_match)
            #print(to_unshuffle[i])
            #print(correlated_graph[j])
            #print()
            
            if row_score<smallest_error:
                smallest_error=row_score
                smallest_error_index=j
       
             
        
        
        matchings[i]=candidate_rows[smallest_error_index]
        
       
        #if not matchings[i]==remove_later[i]:
         #   correct=remove_later[i]
          #
          #  num00cor=0
           # numcor=0
            #for k in range(len(to_unshuffle)):
             #   if to_unshuffle[i][k]==0 and correlated_graph[correct][k]==0:
              #      num00cor+=1
               # numcor+=1
            #row_scorecor=abs(num00cor/numcor-value_to_match)
            
            #flag=1
        #count+=1
    return matchings


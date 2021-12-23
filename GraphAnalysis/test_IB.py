#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 23 19:01:28 2021

@author: fshiranichaharsooghi
"""
import sys, numpy as np,os
import Info_Theory as IT
import nltk
import math
# nltk.download('punkt')
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
import multiprocessing
from functools import partial
import matplotlib.pyplot as plt
import networkx as nx
import matplotlib
from datetime import datetime
import regex as re
import traceback
import line_profiler as lp


import threading
from multiprocessing import Manager
train_address='texts//Train//' 
test_address='texts//Test//' 
train_folder=os.listdir("C:\\Users\\17017\\source\\repos\\Archive\\texts\\Train")
test_folder=os.listdir("C:\\Users\\17017\\source\\repos\\Archive\\texts\\Test")

len_Train_address=len(train_address)
len_Test_address=len(test_address)
lock=threading.Lock()


def train(parameter,context_length,*,folder=None,string_list=[],inputfile=None,input_text=""):
    if inputfile is not None:
        input_text=file_to_string(inputfile)
    if folder is not None:
        for file in folder:
            string_list.append(file_to_string(file))
    freqs=test(context_length,text=input_text)
    for adversary in string_list:           
                
                if input_text!=adversary:                                                     
                    freqs2=test(context_length,text=adversary)                                           
                    for token in freqs.keys():
                        if token in freqs2.keys():
                            freqs[token]=freqs[token]-parameter*freqs2[token]                                                 
                    freqs.update((x,max(y,0)) for x,y in freqs.items())                    
                    norm=sum(freqs.values())
                    freqs.update((x,y/norm) for x,y in freqs.items())                   
                    
    return freqs                
def file_to_string(inputfile):
    input_text=""
    if inputfile is not None:
        with open(inputfile,"rt") as inp:
            input_text=inp.read() 
    return input_text
    # with open(inputfile, "rt") as inp:
    #     while(1):
    #         pos=inp.tell()
    #         symbol=inp.read(2)
    #         if not symbol:
    #             break
    #         # print(symbol)
    #         Temp=[ord(s) for s in symbol]
    #         # print(Temp)
    #         inp.seek(pos)
    #         symbol=inp.read(1)
    #         if len(Temp)==2:
    #             Freqs[Temp[0],Temp[1]]=Freqs[Temp[0],Temp[1]]+1
    #             # print(Freqs[Temp[0],Temp[1]])
    #         else:
    #             break
    # Freqs2=np.zeros((128,128))
    # with open(adversary, "rt") as inp:
    #     while(1):
    #         pos=inp.tell()
    #         symbol=inp.read(2)
    #         if not symbol:
    #             break
    #         # print(symbol)
    #         Temp=[ord(s) for s in symbol]
    #         # print(Temp)
    #         inp.seek(pos)
    #         symbol=inp.read(1)
    #         if len(Temp)==2:
    #             Freqs2[Temp[0],Temp[1]]=Freqs2[Temp[0],Temp[1]]-parameter
    #             # print(Freqs[Temp[0],Temp[1]])
    #         else:
    #             break
    # Freqs=Freqs+Freqs2
 
def multi_train(training_file,*,clen,epsval,w,folder,shared_dict):      
    temp=train(training_file,w,clen,folder)      
    temp.update((x,y+epsval) for x,y in temp.items())
    lock.acquire()    
    try:            
        shared_dict[training_file]=temp                 
    finally:
        lock.release()
    
def multi_test(testing_file,*,clen,epsval,w,shared_dict):
    temp=test(testing_file,clen)
    temp.update((x,y+epsval) for x,y in temp.items())
    lock.acquire()    
    try:
        shared_dict[testing_file]=temp        
    finally:
        lock.release()
    
def run_with_multiprocessing(training_files,testing_files,length,eps,weight):
    manager=Manager()
    trained_freqs=manager.dict()
    tested_freqs=manager.dict()
    train_names=[]   
    test_names=[]
    G=np.zeros((len(training_files),len(testing_files)))    
    with multiprocessing.Pool(processes=5) as pool:
        pool.map(partial(multi_train,clen=length,epsval=eps,w=weight,folder=training_files,shared_dict=trained_freqs),iterable=training_files)
        pool.map(partial(multi_test,clen=length,epsval=eps,w=weight,shared_dict=tested_freqs),iterable=testing_files)
    for file in training_files:
        train_names.append(file)
    for file in testing_files:
        test_names.append(file) 
    names=train_names+test_names
    Texts_Range=list(names)
    for i in range(len(train_names)):       
        for j in range(len(test_names)):
            G[i][j]=math.exp(IT.KLD(tested_freqs[test_names[j]],trained_freqs[train_names[i]],eps))
    L=len(training_files)+len(testing_files)
    min_of_rows = G.min(axis=1)   
    for i in range(0,len(training_files)):
        for j in range(0,len(testing_files)):
            G[i][j]=G[i][j]-min_of_rows[i]
            G[i][j]=math.exp(-G[i][j])      
    G_Graph=np.zeros((L,L))
    G_Graph[len(training_files):L,0: len(training_files)]=G
    G_Graph[0: len(training_files),len(training_files):L]=np.transpose(G)    
    show_graph_with_labels(G_Graph, Texts_Range)
    for i in range(0,len(testing_files)):
        Name=  testing_files[np.argmax(G[i,:])]        
        print(testing_files[i] +" is written by "+ Name)


def test(context_length,*,input_file=None,text=""): 
    if input_file is not None:
        text=file_to_string(input_file)  
    freqs=dict()
    for i in range(len(text)-1):
        symbol=text[i:i+context_length]        
        if not symbol in freqs.keys():
            freqs[symbol]=1
        else:
            freqs[symbol]+=1
    norm=sum(freqs.values())      
    freqs.update((x,y/norm) for x,y in freqs.items())
    
    return freqs

def train_and_test(training_files,testing_files,context_len,eps):
    #what does this parameter do?
    
    parameter2=0.7
    
    names=[]
    for file in training_files:
        names.append(file)
    for file in testing_files:
        names.append(file)
    Texts_Range=list(names)
    #not used
    #Texts_Range=list(Names)
    # Freqs_Sartre_1=train('Sartre_P1.rtf',parameter2)+eps
    # Freqs_Sartre_2=test('Sartre_P2.rtf')+eps
    # Freqs_Ceasar_1=train('Ceasar_P1.rtf',parameter2)+eps
    # Freqs_Ceasar_2=test('Ceasar_P2.rtf')+eps
    # Freqs_Hill_1=train('News_P1.rtf',parameter2)+eps
    # Freqs_Hill_2=test('News_P2.rtf')+eps
    # Freqs_BBC_1=train('BBC_P1.rtf',parameter2)+eps
    # Freqs_BBC_2=test('BBC_P2.rtf')+eps
    # Freqs_FT_1=train('FT_P1.rtf',parameter2)+eps
    # Freqs_FT_2=test('FT_P2.rtf')+eps
    # Freqs_Hamlet_1=train('Hamlet_P1.rtf',parameter2)+eps
    # Freqs_Hamlet_2=test('Hamlet_P2.rtf')+eps

    freqs1=[]
    #this trains each file and then tests it
    
    
    
    for i in range(len(training_files)):         
        freqs1.append(train(parameter2,context_len,training_files,inputfile=training_files[i]))        
        freqs1[i].update((x,y+eps) for x,y in freqs1[i].items())       
    freqs2=[]
    for i in range(len(testing_files)):             
        freqs2.append(test(context_len,input_file=testing_files[i]))
        freqs2[i].update((x,y+eps) for x,y in freqs2[i].items())
        
    
    
    
    
    G=np.zeros((len(training_files),len(testing_files)))
    #for each text in train and text this seems to figure out the divergence
    for i in range(0,len(training_files)):
        for j in range(0,len(testing_files)):
               
                # G[i][j]=math.exp(IT.KLD(Freqs1[j,:],Freqs2[i,:]))                
               G[i][j]=math.exp(IT.KLD(freqs2[i],freqs1[j],eps))
    
    L= len(training_files)+len(testing_files)

    # min_of_rows = G.min(axis=1)
    # G = G/ min_of_rows[:, np.newaxis]
    # G=np.reciprocal(G)
    # #G=G**6
    # G_Graph=np.zeros((L,L))
    # G_Graph[len(Texts_Train):L,0: len(Texts_Train)]=G
    # G_Graph[0: len(Texts_Train),len(Texts_Train):L]=np.transpose(G)
    
    #G = G- min_of_rows[:, np.newaxis]
    
    
    min_of_rows = G.min(axis=1)
    
    for i in range(0,len(training_files)):
        for j in range(0,len(testing_files)):
            G[i][j]=G[i][j]-min_of_rows[i]
            G[i][j]=math.exp(-G[i][j])
    
    #G=G**6
    G_Graph=np.zeros((L,L))
    G_Graph[len(training_files):L,0: len(training_files)]=G
    G_Graph[0: len(training_files),len(training_files):L]=np.transpose(G)
    
    show_graph_with_labels(G_Graph, Texts_Range)
    for i in range(0,len(testing_files)):
        Name=  testing_files[np.argmax(G[i,:])]        
        print(testing_files[i] +" is written by "+ Name)
    #for i in range(0,len(training_files)):
        #Name=  training_files[np.argmax(G[i,:])]
        #Name_Extract = re.search(r'N_(.+?)_', Name)        
        #print(testing_files[i] +" is written by "+ Name_Extract.group(1))

def test_large():
    training_files=[]
    testing_files=[]
    for file in train_folder:
        training_files.append(train_address+file)
    for file in test_folder:
        testing_files.append(test_address+file)
    train_and_test(training_files,testing_files,4,10**-20)

def test_multiprocessing():
    training_files=[]
    testing_files=[]
    for file in train_folder:
        training_files.append(train_address+file)
    for file in test_folder:
        testing_files.append(test_address+file)
    run_with_multiprocessing(training_files,testing_files,2,10**-20,0.7)
def show_graph_with_labels(adjacency_matrix, mylabels):
    gr = nx.Graph() #Create a graph object called G
    node_list = mylabels
    for node in node_list:
        gr.add_node(node)
    pos=nx.circular_layout(gr)
    plt.figure(6,figsize=(50,50))
    nx.draw_networkx_nodes(gr,pos,node_color='green',node_size=100)
    labels = {}
    for node_name in node_list:
        labels[str(node_name)] =str(node_name)
    nx.draw_networkx_labels(gr,pos,labels,font_size=40)
    rows, cols = np.where(adjacency_matrix >0)
    a=rows.tolist()
    b=cols.tolist()
    for i in range(0,len(a)):
        gr.add_edge(node_list[a[i]],node_list[b[i]],weight=adjacency_matrix[a[i],b[i]])
    all_weights=list([])
    for (node1,node2,data) in gr.edges(data=True):
        all_weights.append(data['weight'])
    unique_weights=list(set(all_weights))
    for weight in unique_weights:
        weighted_edges=[(node1,node2) for (node1,node2,edge_attr) in gr.edges(data=True) if edge_attr['weight']==weight]
        width=weight*5*len(adjacency_matrix)/sum(all_weights)
        nx.draw_networkx_edges(gr,pos,edgelist=weighted_edges,width=width)
    plt.show()
    plt.savefig( datetime.now().strftime("%Y%m%d-%H%M%S"), dpi=300, bbox_inches='tight')
 
    print(1)
   



# print(IT.KLD(Freqs_Sartre_1,Freqs_Sartre_2))
# print(IT.KLD(Freqs_Ceasar_1,Freqs_Sartre_2))
# print(IT.KLD(Freqs_Hill_1,Freqs_Sartre_2))
# print(IT.KLD(Freqs_BBC_1,Freqs_Sartre_2))
# print(IT.KLD(Freqs_FT_1,Freqs_Sartre_2))
# print(IT.KLD(Freqs_Hamlet_1,Freqs_Sartre_2))


# print('-----------')
# print(IT.KLD(Freqs_Sartre_1,Freqs_Ceasar_2))
# print(IT.KLD(Freqs_Ceasar_1,Freqs_Ceasar_2))
# print(IT.KLD(Freqs_Hill_1,Freqs_Ceasar_2))
# print(IT.KLD(Freqs_BBC_1,Freqs_Ceasar_2))
# print(IT.KLD(Freqs_FT_1,Freqs_Ceasar_2))
# print(IT.KLD(Freqs_Hamlet_1,Freqs_Ceasar_2))

# print('-----------')
# print(IT.KLD(Freqs_Sartre_1,Freqs_Hill_2))
# print(IT.KLD(Freqs_Ceasar_1,Freqs_Hill_2))
# print(IT.KLD(Freqs_Hill_1,Freqs_Hill_2))
# print(IT.KLD(Freqs_BBC_1,Freqs_Hill_2))
# print(IT.KLD(Freqs_FT_1,Freqs_Hill_2))
# print(IT.KLD(Freqs_Hamlet_1,Freqs_Hill_2))

# print('-----------')
# print(IT.KLD(Freqs_Sartre_1,Freqs_BBC_2))
# print(IT.KLD(Freqs_Ceasar_1,Freqs_BBC_2))
# print(IT.KLD(Freqs_Hill_1,Freqs_BBC_2))
# print(IT.KLD(Freqs_BBC_1,Freqs_BBC_2))
# print(IT.KLD(Freqs_FT_1,Freqs_BBC_2))
# print(IT.KLD(Freqs_Hamlet_1,Freqs_BBC_2))

# print('-----------')
# print(IT.KLD(Freqs_Sartre_1,Freqs_FT_2))
# print(IT.KLD(Freqs_Ceasar_1,Freqs_FT_2))
# print(IT.KLD(Freqs_Hill_1,Freqs_FT_2))
# print(IT.KLD(Freqs_BBC_1,Freqs_FT_2))
# print(IT.KLD(Freqs_FT_1,Freqs_FT_2))
# print(IT.KLD(Freqs_Hamlet_1,Freqs_FT_2))

# print('-----------')
# print(IT.KLD(Freqs_Sartre_1,Freqs_Hamlet_2))
# print(IT.KLD(Freqs_Ceasar_1,Freqs_Hamlet_2))
# print(IT.KLD(Freqs_Hill_1,Freqs_Hamlet_2))
# print(IT.KLD(Freqs_BBC_1,Freqs_Hamlet_2))
# print(IT.KLD(Freqs_FT_1,Freqs_Hamlet_2))
# print(IT.KLD(Freqs_Hamlet_1,Freqs_Hamlet_2))
# print('-----------')

if __name__ == '__main__':
    try:
        test_large()
    except:
        traceback.print_exc()


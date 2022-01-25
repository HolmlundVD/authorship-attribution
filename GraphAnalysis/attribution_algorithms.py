from hmmlearn import hmm
import hypothesis_testing
import json
import numpy as np
import pickle
import sys
import pandas as pd
import access_layered_structured as als
import line_profiler as lp
from striprtf.striprtf import rtf_to_text
import Info_Theory as it

alphabet="!@#$englishalphabet"
threshold=0
def adversarial_with_markov(training_file,testing_file,context_len):
    context_len=2
    all_emissions=dict()
    english=""
    
    with open(training_file) as text:
        train_data=json.load(text)
    with open(testing_file) as text:
        test_data=json.load(text)
    all_emissions[alphabet]=np.zeros(shape=(128,128))
    for author,comments in list(train_data.items()): 
                    
        print(author)
        characters=[[i] for i in range(128)]
        characters+=[[ord(i)] for i in hypothesis_testing.deEmojify(rtf_to_text(comments[1]))]  
        
        all_emissions[author]=create_model_am(characters)   
        all_emissions[alphabet]+=all_emissions[author]/len(train_data.items())
        
   
    #english_chars=[[i] for i in range(128)]
    #english_chars+=[[ord(i)] for i in hypothesis_testing.deEmojify(english)] 
    
    
    #all_emissions[alphabet]=create_model_am(english_chars)
    print("done")
     
    

    
    #all_emissions[alphabet]=model
    total_matched=0
    total_tested=0
    
    i=0
    for tweet in test_data:       
        i+=1       
        freqs=np.zeros(shape=(128,128))
        characters=[[i] for i in range(128)]
        characters+=[[ord(i)] for i in hypothesis_testing.deEmojify(rtf_to_text(tweet[1]))]

        for i in range(len(characters)-1):                   
            freqs[characters[i],characters[i+1]]+=1.0  
            
        print("freqs")
        print(freqs[58][32])
        #freqs=create_model_am(characters)
        freqs=freqs/(len(characters)-1)                
        best_matched_score=sys.maxsize
        best_matched_author=""       
        

        for author in all_emissions:  
            choices=dict()
            if author !=alphabet:      
                author_sum=0
                author_div=it.KLD(all_emissions[author],all_emissions[alphabet],10**-20)
                author_sum=it.KLD(all_emissions[author],freqs,10**-20)
               
                
                #for i in range(128):
                #    for j in range(128):    
                #        if sum(freqs[i])==0:
                #            author_sum+=0
                #            choices[(i,j)]=0
                #        else:   
                            
                #            choices[(i,j)]=(freqs[i][j]/sum(freqs[i]))*(all_emissions[author][i][j]-all_emissions[alphabet][i][j])
                #            #/sum(freqs[i])
                #            author_sum+=(freqs[i][j]/(sum(freqs[i])+0.01))*(all_emissions[author][i][j]-all_emissions[alphabet][i][j]) 
                print(author_sum)       
                #new_dict=sorted(choices.items(),key=lambda kv:kv[1],reverse=True)
                print(author)
                #for letter,score in new_dict[0:10]:
                #    print(chr(letter[0])+""+chr(letter[1]))
                #    print(score)
                #    print(freqs[letter[0]][letter[1]]*len(characters)-1)
                #    print(sum(freqs[letter[0]])*len(characters)-1)
                #    print(all_emissions[author][letter[0]][letter[1]])
                #    print(all_emissions[alphabet][letter[0]][letter[1]])
                if author_sum<best_matched_score:
                    best_matched_score=author_sum
                    best_matched_author=author     
               
        total_tested+=1
        print(tweet[0])
        print("matches")
        print(best_matched_author)
        if best_matched_author==tweet[0]:
            total_matched+=1
    print(total_tested)
    print(total_matched)

#
#given the text creates the frequency table of characters
#
def create_model_am(text:str):
    model = hmm.MultinomialHMM(n_components=4)
    model.algorithm='viterbi'
    model.params='e'
    model.n_features=128
    model.init_params=''
    model.startprob_ = np.array([0.33, 0.33, 0.1, 0.24])
    model.transmat_ = np.array([[0.1, 0.2, 0.4, 0.3],
                            [0.3, 0.2, 0.2, 0.3],
                            [0.5, 0.1, 0.3, 0.1],
                          [0.25,0.25,0.25,0.25]])  
    A=np.transpose(model.transmat_)- np.eye(4)
    A=A[0:3,0:4]
    Ap=np.ones((4,4))
    Ap[1:4,0:4]=A
    B=np.append([1],np.zeros((1,3)))
    P_stat = np.linalg.solve((Ap),(B))
    A=np.transpose(model.transmat_)- np.eye(4)
    A=A[0:3,0:4]
    Ap=np.ones((4,4))
    Ap[1:4,0:4]=A
    B=np.append([1],np.zeros((1,3)))
    stationary_prop = np.linalg.solve((Ap),(B))
    Probs=np.random.rand(4,128)
    row_sums = Probs.sum(axis=1)
    Probs = Probs / row_sums[:, np.newaxis]
    model.emissionprob_=Probs
    #
    #t-1 is row t-2 is column
    #
    reverse_trans_probs=np.zeros(shape=(4,4))
    for i in range(4):
        for j in range(4):
            reverse_trans_probs[i][j]=(model.transmat_[j][i]*stationary_prop[j])/stationary_prop[i]
       
               
    model.fit(text)   
    probabilities=np.zeros(shape=(128,128))
    temp_total=np.zeros(shape=(4))
    for i in range(128):  
            #
            #P (E(t-1))
            #           
            letter_prob=sum([stationary_prop[x]*model.emissionprob_[x][i] for x in range(4)]) 
            
            #
            #P(E(t-1)|S(t-1))
            #          
            letter_given_state=[sum([model.emissionprob_[n][i]*reverse_trans_probs[m][n] for n in range(4)]) for m in range(4)] 
            
            for j in range(128):
                sum_s=0                         
                for state in range(4):
                    #
                    #P(S(t-1)|E(t-1))
                    #
                    state_given_letter=(letter_given_state[state]*stationary_prop[state])/letter_prob                     
                    sum_s+=state_given_letter*model.emissionprob_[state][j]
                temp_total+=sum_s
                #
                #P(E(t)|E(t-1))
                #
                probabilities[i][j]=sum_s   
    
    return probabilities
def run():
    adversarial_with_markov("GraphAnalysis\\classical_tests\\train","GraphAnalysis\\classical_tests\\test",2)
if __name__=="__main__":        
    profiler=lp.LineProfiler()
    profiler.add_function(adversarial_with_markov)
    wrapper=profiler(run)
    wrapper()
    profiler.print_stats()
    


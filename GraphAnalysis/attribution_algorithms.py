from hmmlearn import hmm
import hypothesis_testing
import json
import numpy as np
import pickle
import sys
import pandas as pd
import access_layered_structured as als
import line_profiler as lp
alphabet="!@#$englishalphabet"
threshold=0
def adversarial_with_markov(training_file,testing_file,context_len):
    context_len=2
    all_emissions=dict()
    english=""
    print("access")
    with open(training_file) as text:
        train_data=json.load(text)
    with open(testing_file) as text:
        test_data=json.load(text)
    print("complete")
    print(len(test_data))
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
    stationary_prop=np.matmul(model.transmat_,model.startprob_)
    Probs=np.random.rand(4,128)
    row_sums = Probs.sum(axis=1)
    Probs = Probs / row_sums[:, np.newaxis]
    model.emissionprob_=Probs
    i=0
    print(len(train_data.items()))
    for author,comments in list(train_data.items()): 
        i+=1
        
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
        
        
        Probs=np.random.rand(4,128)
        row_sums = Probs.sum(axis=1)
        Probs = Probs / row_sums[:, np.newaxis]
        model.emissionprob_=Probs
        print(author)
        characters=[[ord(i)] for i in hypothesis_testing.deEmojify(comments[1])]  
        characters+=[[i] for i in range(128)]
        model.fit(characters)
        #all_emissions[author]=model.emissionprob_
        probabilities=np.zeros(shape=(128,128))
        for i in range(128):
            char_probs=[stationary_prop[x]*model.emissionprob_[x][i] for x in range(4)]
            for j in range(128):
                sum_s=0
                for state in range(4):
                    sum_s+=(char_probs[state]/sum(char_probs))*(model.emissionprob_[state][j]/stationary_prop[state])
                probabilities[i][j]=sum_s
        
        all_emissions[author]=probabilities
        english+=comments[1][0:1000]
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
    
    Probs=np.random.rand(4,128)
    row_sums = Probs.sum(axis=1)
    Probs = Probs / row_sums[:, np.newaxis]
    model.emissionprob_=Probs
    english_chars=[[ord(i)] for i in hypothesis_testing.deEmojify(english)] 
    english_chars+=[[i] for i in range(128)]
    model.fit(english_chars)
    all_emissions[alphabet]=model.emissionprob_
    probabilities=np.zeros(shape=(128,128))
    for i in range(128):
        char_probs=[stationary_prop[x]*model.emissionprob_[x][i] for x in range(4)]
        for j in range(128):
            sum_s=0
            for state in range(4):
                sum_s+=(char_probs[state]/sum(char_probs))*(model.emissionprob_[state][j]/stationary_prop[state])
            probabilities[i][j]=sum_s
     
    all_emissions[alphabet]=probabilities
    
    #all_emissions[alphabet]=model
    total_matched=0
    total_tested=0
    
    i=0
    for tweet in test_data:       
        i+=1       
        freqs=np.zeros(shape=(128,128))
        tweet_characters=[ord(i) for i in hypothesis_testing.deEmojify(tweet[1])]
        for i in range(len(tweet_characters)-1):                   
            freqs[tweet_characters[i],tweet_characters[i+1]]+=1.0            
        freqs=freqs/(len(tweet_characters)-1)                
        best_matched_score=-sys.maxsize
        best_matched_author=""
        
        for author in all_emissions.keys():
            
            if author !=alphabet:                
                author_sum=0
                for i in range(128):
                    for j in range(128):    
                        if sum(freqs[i])==0:
                            author_sum+=0
                        else:
                            
                            author_sum+=(freqs[i][j]/sum(freqs[i]))*(all_emissions[author][i][j]-all_emissions[alphabet][i][j]) 
                
                if author_sum>best_matched_score:
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
def run():
    adversarial_with_markov("GraphAnalysis\\bitcoin\\training800.txt","GraphAnalysis\\bitcoin\\testing800.txt",2)
if __name__=="__main__":        
    profiler=lp.LineProfiler()
    profiler.add_function(adversarial_with_markov)
    wrapper=profiler(run)
    wrapper()
    profiler.print_stats()
    


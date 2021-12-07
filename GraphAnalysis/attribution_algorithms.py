from hmmlearn import hmm
import hypothesis_testing
import json
import numpy as np
import pickle
alphabet="!@#$englishalphabet"
threshold=0
def adversarial_with_markov(training_file,testing_file,context_len):
    all_emissions=dict()
    english=""
    with open(training_file) as text:
        train_data=json.load(text)
    
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
   
    
    for author,comments in train_data.items():      
        characters=[[ord(i)] for i in hypothesis_testing.deEmojify(comments[1])]  
        model.fit(characters)
        all_emissions[author]=model.emissionprob_
        english+=comments
    english_chars=[[i] for i in hypothesis_testing.deEmojify(english)] 
    model.fit(english_chars)
    all_emissions[alphabet]=model.emissionprob_
    total_matched=0
    total_tested=0
    for tweet in test_data:
        text=hypothesis_testing.deEmojify(tweet)
        frequencies=[text.count(ord(i)) for i in range(128)]
        best_matched_score=sys.minint
        best_matched_author=""
        for author in all_emissions.keys():
            author_sum=0
            for i in range(4):
                for j in range(128):
                    author_sum+=frequencies[j]*(all_emissions[author][i][j]-all_emissions[alphabet][i][j])/all_emissions[author][i][j]
            if author_sum>best_matched_score:
                best_matched_score=author_sum
                best_matched_author=author
        total_tested+=1
        if best_matched_author==author:
            total_matched+=1
    
if __name__=="__main__":
    adversarial_with_markov("bitcoin//training80.txt","bitcoin//testing80.txt",3)


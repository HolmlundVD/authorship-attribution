import csv
import os
import nltk
import pandas as pd
import numpy as np
import string
from itertools import compress
from collections import Counter
import unicodedata
from unidecode import unidecode
import numpy as np
import pickle
from hmmlearn import hmm
from striprtf.striprtf import rtf_to_text 


PATH=''
# csv files
file1 = PATH+'Bitcoin_tweets.csv'

def deEmojify(inputString):
    returnString = ""
    print("start")
    for character in rtf_to_text(inputString):
        try:
            character.encode("ascii")
            returnString += character
        except UnicodeEncodeError:
            replaced = unidecode(str(character))
            if replaced != '':
                returnString += replaced
            else:
                try:
                     returnString += "[" + unicodedata.name(character) + "]"
                except ValueError:
                     returnString += "[x]"
    
    return returnString





def load_doc(filename):
    data = pd.read_csv(filename, usecols=['user_name', 'text'])
    return data

def find_frequent_users():
    # Make array of tweet data
    tweets = load_doc(file1)

    # Create Data Frame for ID and Tweets
    tweetFrame = pd.DataFrame({'ID': tweets['user_name'],
                           'Tweet': tweets['text']})
    #print('Printing tweets with corresponding user names:')
    #print(tweetFrame.head(5))
    Temp= [str(i).encode('unicode-escape') for i in tweets.user_name]
    (UNIQUE, COUNTS)=np.unique(Temp, return_counts=True)
    Frequent_users=list(compress(UNIQUE,COUNTS>100))
    Tweets_and_Freq_Users= pd.DataFrame(columns=['ID', 'Tweets'])
    for name in Frequent_users[0:5]:
        A=[i for i, x in enumerate(Temp) if x ==name]
        d={'ID':[name], 'Tweets':[
        deEmojify(str([tweetFrame.loc[i]['Tweet'] for i in A]))]}
        df=pd.DataFrame(data=d, columns=['ID', 'Tweets'])
        Tweets_and_Freq_Users=Tweets_and_Freq_Users.append(df)
    Tweets_and_Freq_Users.to_csv(PATH+'freq_100', sep='\t', encoding='unicode-escape')
    return Tweets_and_Freq_Users;




def unicode_to_ascii(to_transfer:pd.DataFrame):
    (A,B)=np.shape(to_transfer)
    for i in range(0,A):  
        D=[]
        print(i)
        C= Tweets_and_Freq_Users.iloc[i]['Tweets']
        for j in range(0,len(C)):
            if type(C[j])==str:
                D.append(ord(C[j]))
       
        to_transfer.iloc[i]['Tweets']=D
        return to_transfer












def run_model():
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
    model.emissionprob_= Probs


    # generate "fake" training data
    #emissions1, states1 = model.sample(10000)
    #print("Transition matrix before training: \n", model.transmat_)
    emissions1=[[i] for i in find_frequent_users().iloc[0]['Tweets'][0:100000]]
    # train
    model.fit(emissions1)
    print("Transition matrix after training: \n", model.transmat_)
    print("Emission Probabilities after training: \n", model.emissionprob_)
    P1=model.emissionprob_


if __name__=="__main__":
    run_model()




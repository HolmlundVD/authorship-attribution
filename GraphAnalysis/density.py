import numpy as np
import nltk
class WordDensity(object):
    #takes a chunk of text and divides the first times_to_divide*division_size it 
    #into times_to_divide sections with division_size elements 
   
    def __init__(self,words:int, unique_words:int):
        self.words=words
        self.unique_words=unique_words
        self.word_density=float(unique_words/words)
    @staticmethod
    def text_divider(text:str,times_to_divide:int,division_size:int)->np.array:
        
        divisions=np.empty((times_to_divide,division_size),dtype="object")
        tknz=nltk.RegexpTokenizer(r"\w+")
        words=tknz.tokenize(text)
        print(len(words))
        for i in range(times_to_divide):                 
            divisions[i]=words[(division_size*i):(division_size*(i+1))]                  
        return divisions
    @classmethod
    def get_text_averages(cls,text:str,times_to_divide,division_size)->np.array:
        
        divided_words=cls.text_divider(text,times_to_divide,division_size)
        
        densities=np.empty(len(divided_words),dtype=WordDensity)
        for i in range(len(divided_words)):
            densities[i]=cls.analyze_words(divided_words[i])
        return densities
    @classmethod
    def get_text_total_average(cls,text:str,times_to_divide,division_size)->int:
        divided_words=cls.text_divider(text,times_to_divide,division_size)        
        sum=0
        for i in range(len(divided_words)):
            sum+=cls.analyze_words(divided_words[i]).word_density
        return sum/times_to_divide
        
    @classmethod
    def analyze_words(cls,text:np.array):
        
        words_found=set()        
        for word in text:            
            if not word in words_found:               
                words_found.add(word)
        
        return WordDensity(len(text),len(words_found))
    def __str__(self):
        return "total words:"+str(self.words)+"\n"+"unique words:"+str(self.unique_words)+"\n"+"word density"+str(self.word_density)

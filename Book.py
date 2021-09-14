from networkx import *
import numpy
import nltk
class BookGraph:
    #used for tokenizer
    
    
    #iterates throuhg the sentences
    #
    #
    #
    def __makeWordGraph(self,text:str):
        self.__graph=networkx.Graph()
        self.__length=0
        self.__new_word_tracker=[]
        sentences=nltk.sent_tokenize(text)
        
        for sentence in sentences:
            self.__analyzeSentence(sentence)
     #creates a graph using the text and stemmer provided in the constructor
    def __init__(self,bookText: str,stemmers):
        #make sure the stemmer can stem
        if not hasattr(stemmers,"stem"):
            raise AttributeError("argument stemmer does not have method stem")
        self.stemmer=stemmers
        self.__makeWordGraph(bookText)
   
    def get_new_word_tracker(self):
        return self.__new_word_tracker
    #adds the passed sentance to the graph
    def __analyzeSentence(self,sentence:str):     
        tknz=nltk.RegexpTokenizer(r"\w+")
        words=tknz.tokenize(sentence)
        
        for i in range(len(words)):
            
            self.__length+=1
            firstWord=self.stemmer.stem(words[i])
            self.__new_word_tracker.append(len(self.__graph))
            
            if not firstWord in list(self.__graph.nodes):
                
                self.__graph.add_node(firstWord)    
            for j in range(i+1,len(words)):
                secondWord=self.stemmer.stem(words[j])                
                if not secondWord in list(self.__graph.adj[firstWord]):
                    if firstWord!=secondWord:
                        self.__graph.add_edge(firstWord,secondWord,frequency=1,weight=1)
                else:
                      self.__graph[firstWord][secondWord]["frequency"]+=1
                      self.__graph[firstWord][secondWord]["weight"]+=1
                     
                
    def getFrequency(self,word1:str,word2:str)->int:  
        if not word1 in list(self.__graph.nodes):
            return 0
        if not word2 in list(self.__graph.adj[word1]):
            return 0
        return self.__graph[word1][word2]["frequency"]
    def getAdjacencyMatrix(self)->numpy.array:
        return networkx.to_numpy_array(self.__graph)
    def get_text_length(self):
        return self.__length
import numpy as np
import random
#contains information about a matrix that has been shuffled
class ShuffledMatrix(object):
    #one array is the shuffled erdos renyi graph
    #the other is the array of rows that have been shuffled and you don't know 
    def __init__(self,shuffled_array:np.array,shuffled_rows:np.array,shuffle_mappings:np.array):
        self.__shuffled_array=shuffled_array
        self.__shuffled_rows=shuffled_rows
        self.__shuffled_mappings=shuffle_mappings

    def get_shuffled_array(self)->np.array:
        return self.__shuffled_array
    def get_shuffled_rows(self)->np.array:
        return self.__shuffled_rows
    def get_shuffle_mappings(self)->np.array:
        return self.__shuffled_mappings


class ShuffleMatrix(object):
   @staticmethod    
   def __shuffleRows(toShuffle:np.array,sample:np.array,sortedSample:np.array):
       tempHolder=np.empty((len(toShuffle),len(toShuffle)))
       hasBeenReplaced=np.zeros(len(toShuffle),dtype=bool)
       for i in range(len(sortedSample)):           
           fromIndex=sample[i]
           toIndex=sortedSample[i]
           
           tempHolder[toIndex]=toShuffle[toIndex]
           
           if hasBeenReplaced[fromIndex]:  
              
               toShuffle[toIndex]=tempHolder[fromIndex]
               hasBeenReplaced[toIndex]=True
           else:
               
               toShuffle[toIndex]=toShuffle[fromIndex]
              
               hasBeenReplaced[toIndex]=True
       
   #holds a single public static method that shuffles an erdos renyi graph
   #this does not parameter check if the matrix is symmetrical
   #this  will check if it is square
   @staticmethod
   def shuffle(toShuffle:np.array,propShuffled:float)->ShuffledMatrix:
      toEdit=toShuffle
      if not all (len (row) == len (toShuffle) for row in toShuffle):
          raise ValueError("provided array is not square")
      numShuffled=int(propShuffled*len(toEdit))
      sampleToShuffle=random.sample(range(0,len(toEdit)),numShuffled)
      sample_permutation=np.random.permutation(sampleToShuffle)  
      map=dict()
      for i in range(len(sample_permutation)):
          map[sample_permutation[i]]=sampleToShuffle[i]
      ShuffleMatrix.__shuffleRows(toEdit,sampleToShuffle,sample_permutation) 
      toEdit=np.transpose(toEdit)
      ShuffleMatrix.__shuffleRows(toEdit,sampleToShuffle,sample_permutation)
      return ShuffledMatrix(toEdit,sample_permutation,map)
  

      
  

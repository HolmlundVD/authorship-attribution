import numpy as np
from numba import jit

class ErdosRenyiGraph:
    @staticmethod
    @jit
    def isSymmetrical(matrix:np.array)->bool: 
     
      
      for r in range(len(matrix)):
            print(str(r)+"c")
            for c in range(len(matrix)):
                if matrix[r][c]!=matrix[c][r]:
                    return False
      return True  
    
    def __init__(self,probability:int,elements:int):
       self.__createMatrix(probability,elements)
    def __createMatrix(self,probability:int,elements:int):
        self.__adjacencyMatrix=np.zeros(shape=[elements,elements],dtype=int)
        self.__numConnections=elements*elements-elements
        for i in range(0,elements-1):
            for j in range(i+1,elements):
                num=np.random.rand()                
                if num<probability:
                    self.__adjacencyMatrix[i][j]=1
                    self.__adjacencyMatrix[j][i]=1
            self.__adjacencyMatrix[i][i]=0
    #returns numpy array
    def getAdjacencyMatrix(self)->np.ndarray:
        return np.copy(self.__adjacencyMatrix)
    #returns the proportion of the graph that is 1s
    def getResult(self)->int:       
        return np.sum(self.__adjacencyMatrix)/self.__numConnections
   

    
   
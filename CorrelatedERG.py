import numpy as np
from numba import jit
class CorrelatedERG(object):
    @jit
    def __createMatrix(self,elements:int,probabilities:np.array):
        self.matrix1=np.zeros(shape=[elements,elements],dtype=int)
        self.matrix2=np.zeros(shape=[elements,elements],dtype=int)
        n00=0
        n01=0
        n10=0
        n11=0
        for i in range(0,elements-1):
            print(i)
            for j in range(i+1,elements):
                
                if not i==j:
                    rand=np.random.rand()
                    if rand<probabilities[0]:
                        self.matrix1[i][j]=0
                        self.matrix2[i][j]=0
                        self.matrix1[j][i]=0
                        self.matrix2[j][i]=0
                        n00+=1
                    elif rand<probabilities[0]+probabilities[1]:
                        self.matrix1[i][j]=0
                        self.matrix2[i][j]=1
                        self.matrix1[j][i]=0
                        self.matrix2[j][i]=1
                        n01+=1
                    elif rand<probabilities[0]+probabilities[1]+probabilities[2]:
                        self.matrix1[i][j]=1
                        self.matrix2[i][j]=0
                        self.matrix1[j][i]=1
                        self.matrix2[j][i]=0
                        n10+=1
                    else: 
                        self.matrix1[i][j]=1
                        self.matrix2[i][j]=1
                        self.matrix1[j][i]=1
                        self.matrix2[j][i]=1
                        n11+=1
        self.result=np.array([2*n00/self.__numConnections,2*n01/self.__numConnections,2*n10/self.__numConnections,2*n11/self.__numConnections])
        
            
    #parameter checks the probabilities array and creates the matrix
    def __init__(self,elements:int,probabilities:np.ndarray):
        self.__numConnections=elements*elements-elements
        if not probabilities.size==4:
            raise ValueError("probabilities is not of size 4")
        sum=0
        for n in probabilities:           
            sum+=n
        if sum<0.995 or sum>1.005:          
            raise ValueError("sum of probabilities is not 1")
        self.__createMatrix(elements,probabilities) 
    
    def getAdjacencyMatricies(self)->np.array:
        return [self.matrix1,self.matrix2]
    def getResult(self)->np.array:
       return self.result

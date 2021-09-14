import random
import cProfile as cp
import unittest
import ErdosRenyiGraph as erg
import traceback
import CorrelatedERG as cerg
import numpy as np
import ShuffleMatrix as sh
import unshuffle_matrix as un
import line_profiler as lp
from tabulate import tabulate
class Test(unittest.TestCase):
    def TestErdosRenyi():        
            graph=erg.ErdosRenyiGraph(0.80,20)
            table = tabulate(graph.getAdjacencyMatrix(), tablefmt="fancy_grid")
            #print("ja")
            #print(table)
            #print(graph.getResult())
            assert(erg.ErdosRenyiGraph.isSymmetrical(graph.getAdjacencyMatrix()))
    def TestCERG():
            graph=cerg.CorrelatedERG(20,probabilities=np.array([0.45,0.05,0.05,0.45],dtype=float))
            table1 = tabulate(graph.getAdjacencyMatricies()[0], tablefmt="fancy_grid")
            table2 = tabulate(graph.getAdjacencyMatricies()[1], tablefmt="fancy_grid")
            print(table1)
            print("here")
            print(table2) 
            print(graph.getResult())
            assert(erg.ErdosRenyiGraph.isSymmetrical(graph.getAdjacencyMatricies()[0]))
            assert(erg.ErdosRenyiGraph.isSymmetrical(graph.getAdjacencyMatricies()[1]))
    def TestShuffling():
            graph=erg.ErdosRenyiGraph(0.5,1001)  
            
            shuffled=sh.ShuffleMatrix.shuffle(graph.getAdjacencyMatrix(),0.5)            
                
            assert(erg.ErdosRenyiGraph.isSymmetrical(graph.getAdjacencyMatrix()))
            assert(erg.ErdosRenyiGraph.isSymmetrical(shuffled.get_shuffled_array()))
            
    def test_unshuffling():
            correct_matches=dict()
            matrix_dimension=1000
            prop_shuffled=0.5
            graphs=cerg.CorrelatedERG(matrix_dimension,probabilities=np.array([0.4,0.1,0.1,0.4],dtype=float)) 
            
            shuffled=sh.ShuffleMatrix.shuffle(graphs.getAdjacencyMatricies()[1],prop_shuffled)
           
            
            
            correct_matches=shuffled.get_shuffle_mappings()                                
            unshuffled_matchings=un.get_unshuffle_matchings(graphs.getAdjacencyMatricies()[0],shuffled.get_shuffled_array(),shuffled.get_shuffled_rows().tolist(),[0.5,0,0,0.5],remove_later=correct_matches)
            num_correct=0
            for i in correct_matches.keys():
                if(correct_matches[i]==unshuffled_matchings[i]):
                    num_correct+=1
            print(num_correct)
            print(correct_matches)
            print(unshuffled_matchings)
    def TestRNG():
        oneQ=0
        twoQ=0
        threeQ=0
        fourQ=0
        for i in range(100000):
            
            
            rand=np.random.rand()
            
            if rand<0.25:
               
                oneQ=int(oneQ)+1
            elif rand<0.5:
                twoQ=int(twoQ)+1
            elif rand<0.75:
                threeQ=int(threeQ)+1
            else:
                fourQ=int(fourQ)+1
        print(oneQ)
        print(twoQ)
        print(threeQ)
        print(fourQ)
    def TestSortingMethod():
        num1234
           

if __name__ == '__main__':
    try:
        Test.TestRNG()
        Test.TestErdosRenyi()
        Test.TestCERG()
        Test.TestShuffling()
        #lprofiler = lp.LineProfiler()
        #lprofiler.add_function(un.get_unshuffle_matchings)
        #lprofiler.add_function(cerg.CorrelatedERG._CorrelatedERG__createMatrix)
        #lprofiler.add_function(un.loop_with_numba)
        #lprofiler.add_function(erg.ErdosRenyiGraph.isSymmetrical)
        #lp_wrapper=lprofiler(Test.test_unshuffling)
        #lp_wrapper()
        #lprofiler.print_stats()
        #Test.test_unshuffling()
        
    except:
        traceback.print_exc()

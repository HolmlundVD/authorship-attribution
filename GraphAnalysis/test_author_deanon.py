import unittest
from density import WordDensity
from Book import BookGraph 
import numpy as np
import os
import pandas
import traceback
from DefaultStemmer import DefaultStemmer
import numpy as np
import matplotlib.pyplot as plot
import unittest as ut
import compression
import line_profiler as lp

import ppm_compression as ppm
class Test_test_2(unittest.TestCase):
    def __test_columbus(self):
        text_lengths=[]
        unique_words=[]
        dates=[]
        ax=plot.gca()
        for filename in os.listdir("C:\\Users\\vdh24\\source\\repos\\GraphAnalysis\\wordsOfChristopherColumbus"):
            text=str()
            with open("wordsOfChristopherColumbus\\"+filename,'r') as reader:
                for line in reader.readlines():
                    text=text+line
            entry=BookGraph(text,DefaultStemmer)
            dates.append(filename)
            text_lengths.append(entry.get_text_length())
            unique_words.append(len(entry.getAdjacencyMatrix()))
        ax.scatter(text_lengths,unique_words)
       
        text_lengths2=[]
        unique_words2=[]
        for filename in os.listdir("C:\\Users\\vdh24\\source\\repos\\GraphAnalysis\\davidBArthur"):
            text=str()
            
            with open("davidBArthur\\"+filename,'r') as reader:
                for line in reader.readlines():
                    text=text+line
            entry=BookGraph(text,DefaultStemmer)
            dates.append(filename)
            text_lengths2.append(entry.get_text_length())
            unique_words2.append(len(entry.getAdjacencyMatrix()))
        ax.scatter(text_lengths2,unique_words2,color='red')
        plot.show()
    
    def __test_comparison_of_authors(self):
        text_dup=str()
        text_gift=str()
        text_barber=str()
        text_frog=str()
        ax=plot.gca()
        with open("ohenry\\duplicityohargraves.txt",'r') as reader:
                print("dup")
                for line in reader.readlines():
                    text_dup=text_dup+line
        with open("ohenry\\giftofthemagi.txt",'r') as reader:
                print("gift")
                for line in reader.readlines():
                    text_gift=text_gift+line
        with open("markTwain\\barber.txt",'r') as reader:
                print("barber")
                for line in reader.readlines():
                    text_barber=text_dup+line
        with open("markTwain\\frog.txt",'r') as reader:
                print("frog")
                for line in reader.readlines():
                    text_frog=text_dup+line
        dup_graph=BookGraph(text_dup,DefaultStemmer)
        
        assert(dup_graph.get_text_length()==len(dup_graph.get_new_word_tracker()))
        gift_graph=BookGraph(text_gift,DefaultStemmer)
        barber_graph=BookGraph(text_barber,DefaultStemmer)
        frog_graph=BookGraph(text_frog,DefaultStemmer)
        x=range(len(dup_graph.get_new_word_tracker()))
        a,b,c=np.polyfit(x,dup_graph.get_new_word_tracker(),2)
        print(str(a)+" "+str(b)+" "+str(c))
        ax.plot(x,a*x*x+b*x+c,color='red')
        plot.show()
        x=range(len(gift_graph.get_new_word_tracker()))
        a,b,c=np.polyfit(x,gift_graph.get_new_word_tracker(),2)
        ax.plot(x,a*x*x+b*x+c,color='green')
        print(str(a)+" "+str(b)+" "+str(c))
        
        x=range(len(barber_graph.get_new_word_tracker()))
        a,b,c=np.polyfit(x,barber_graph.get_new_word_tracker(),2)
        print(str(a)+" "+str(b)+" "+str(c))
        ax.plot(x,a*x*x+b*x+c,color='blue')
        x=range(len(frog_graph.get_new_word_tracker()))
        a,b,c=np.polyfit(x,frog_graph.get_new_word_tracker(),2)
        print(str(a)+" "+str(b)+" "+str(c))
        ax.plot(x,a*x*x+b*x+c,color='purple')
        plot.show()        
    
    def test_ipsum_dollar():
        
        text=str()
        with open("ipsumDollar.txt",'r') as reader:                
            for line in reader.readlines():
                text=text+line
        ave=WordDensity.get_text_averages(text,4,50)
     
        for num in ave:
            print(num)
        print(WordDensity.get_text_total_average(text,4,50))
    def compare_twain_henry():
        text_dup=str()
        text_gift=str()
        text_barber=str()
        text_frog=str()
        with open("ohenry\\duplicityohargraves.txt",'r') as reader:
                
                for line in reader.readlines():
                    text_dup=text_dup+line
                
        with open("ohenry\\giftofthemagi.txt",'r') as reader:
                
                for line in reader.readlines():
                    text_gift=text_gift+line
                
        with open("markTwain\\barber.txt",'r') as reader:
                        
                for line in reader.readlines():
                    text_barber=text_barber+line
                 
        with open("markTwain\\frog.txt",'r') as reader:
                
                for line in reader.readlines():
                    text_frog=text_frog+line
                
        ave_dup=WordDensity.get_text_averages(text_dup,30,50)
        ave_gift=WordDensity.get_text_averages(text_gift,30,50)
        ave_barber=WordDensity.get_text_averages(text_barber,30,50)
        ave_frog=WordDensity.get_text_averages(text_frog,30,50)
        print("dup")
        for num in ave_dup:
            print(num)
        print(WordDensity.get_text_total_average(text_dup,30,50))
        print("gift")        
        for num in ave_gift:
            print(num)
        print(WordDensity.get_text_total_average(text_gift,30,50))
        print("barber")        
        for num in ave_barber:
            print(num)
        print(WordDensity.get_text_total_average(text_barber,30,50))
        print("frog")        
        for num in ave_frog:
            print(num)
        print(WordDensity.get_text_total_average(text_frog,30,50))
    def test_youtube_api():
        dummy=1
    def test_compression():
        text=""
        with open('text.txt', 'r') as reader:
            for line in reader.readlines():
                text=text+line
        map=compression.compression.get_word_frequencies(text)
        tree=compression.compression.compress_from_frequencies(map)
        print(tree.costs)
    def test_big_compression():
        text=""
        with open('markTwain\\frog.txt', 'r') as reader:
            for line in reader.readlines():
                text=text+line
        map=compression.compression.get_word_frequencies(text)
        print(map)
        tree=compression.compression.compress_from_frequencies(map)
        print(tree.costs)
    def test_compression_comparison():
        text=""
        with open('markTwain\\frog.txt', 'r') as reader:
            for line in reader.readlines():
                text=text+line
        map=compression.compression.get_word_frequencies(text)
        tree=compression.compression.compress_from_frequencies(map)
        text2=""
        with open('text.txt', 'r') as reader:
            for line in reader.readlines():
                text2=text2+line
        print(tree.get_cost_of_text(text2))
    def  compare_twain_henry_press():
        text_frog=""
        with open('markTwain\\frog.txt', 'r') as reader:
            for line in reader.readlines():
                text_frog=text_frog+line
        text_barber=""
        with open('markTwain\\barber.txt', 'r') as reader:
            for line in reader.readlines():
                text_barber=text_barber+line
        text_dup=""
        with open('ohenry\\duplicityohargraves.txt', 'r') as reader:
            for line in reader.readlines():
                text_dup=text_dup+line
        text_gift=""
        with open('ohenry\\giftofthemagi.txt', 'r') as reader:
            for line in reader.readlines():
                text_gift=text_gift+line
        tree_frog=compression.compression.compress_from_frequencies(compression.compression.get_word_frequencies(text_frog))
        tree_barber=compression.compression.compress_from_frequencies(compression.compression.get_word_frequencies(text_barber))
        tree_dup=compression.compression.compress_from_frequencies(compression.compression.get_word_frequencies(text_dup))
        tree_gift=compression.compression.compress_from_frequencies(compression.compression.get_word_frequencies(text_gift))
        print("twain on twain"+str(tree_frog.get_cost_of_text(text_barber)))
        print("henry on twain"+str(tree_dup.get_cost_of_text(text_barber)))
        print("henry on twain"+str(tree_gift.get_cost_of_text(text_barber)))
        print("twain on henry"+str(tree_frog.get_cost_of_text(text_dup)))
        print("twain on henry"+str(tree_barber.get_cost_of_text(text_dup)))
        print("henry on henry"+str(tree_gift.get_cost_of_text(text_dup)))
        print("twain on henry"+str(tree_frog.get_cost_of_text(text_gift)))              
        print("twain on henry"+str(tree_barber.get_cost_of_text(text_gift)))
        print("henry on henry"+str(tree_dup.get_cost_of_text(text_gift)))
        print("henry on twain"+str(tree_dup.get_cost_of_text(text_frog)))        
        print("twain on twain"+str(tree_barber.get_cost_of_text(text_frog)))
        print("henry on twain"+str(tree_gift.get_cost_of_text(text_frog)))
        
    def test_ppm():
        
        text2=""
        with open('text.txt', 'r') as reader:
            for line in reader.readlines():
                text2=text2+line
        text3=""
        with open('markTwain\\barber.txt', 'r') as reader:
            for line in reader.readlines():
                text3=text3+line
        
        
        ppm_class=ppm.ppm_compressor(text2,2,2)
        print(ppm_class.tree)
        compressed=ppm_class.analyze_text("the fox is h0t he 1s not")
        print(compressed)
    def test_ppm_big():
        text_frog=""
        with open('markTwain\\frog.txt', 'r') as reader:
            for line in reader.readlines():
                text_frog=text_frog+line
        
        text_barber=""
        with open('markTwain\\barber.txt', 'r') as reader:
            for line in reader.readlines():
                text_barber=text_barber+line
        
        text_dup=""
        with open('ohenry\\duplicityohargraves.txt', 'r') as reader:
            for line in reader.readlines():
                text_dup=text_dup+line
       
        text_gift=""
        with open('ohenry\\giftofthemagi.txt', 'r') as reader:
            for line in reader.readlines():
                text_gift=text_gift+line
        
        compressed_frog=ppm.ppm_compressor(text_frog,2,2)
        
        compressed_barber=ppm.ppm_compressor(text_barber,2,2)
        compressed_dup=ppm.ppm_compressor(text_dup,2,2)
        compressed_gift=ppm.ppm_compressor(text_gift,2,2)
        
        print("twain on twain"+str(compressed_frog.analyze_text(text_barber)))        
        #print("henry on twain"+str(compressed_dup.analyze_text(text_barber)))       
        #print("henry on twain"+str(compressed_gift.analyze_text(text_barber)))        
        #print("twain on henry"+str(compressed_frog.analyze_text(text_dup)))
        #print("twain on henry"+str(compressed_barber.analyze_text(text_dup)))
        #print("henry on henry"+str(compressed_gift.analyze_text(text_dup)))        
        #print("twain on henry"+str(compressed_frog.analyze_text(text_gift)))        
        #print("twain on henry"+str(compressed_barber.analyze_text(text_gift)))        
        #print("henry on henry"+str(compressed_dup.analyze_text(text_gift)))       
        #print("henry on twain"+str(compressed_dup.analyze_text(text_frog)))        
        #print("twain on twain"+str(compressed_barber.analyze_text(text_frog)))
        #print("henry on twain"+str(compressed_gift.analyze_text(text_frog)))
    def test_arithmetic_coding():
        text=""
        with open('text.txt', 'r') as reader:
            for line in reader.readlines():
                text=text+line
        map=compression.compression.get_word_frequencies(text)
        print(ppm.ppm_compressor.arithmetic_coding_algorithm(map))
        
if __name__ == '__main__':
     try:
        Test_test_2.test_ipsum_dollar()
        Test_test_2.compare_twain_henry()
        Test_test_2.test_compression()
        Test_test_2.test_big_compression()
        Test_test_2.test_compression_comparison()
        Test_test_2.compare_twain_henry_press()
        Test_test_2.test_ppm()
        Test_test_2.test_arithmetic_coding()
        #lprofiler = lp.LineProfiler()
        #lprofiler.add_function(ppm.ppm_compressor.analyze_text)
        #lprofiler.add_function(compression.compression.compress_from_frequencies)
        #lprofiler.add_function(ppm.ppm_compressor._ppm_compressor__get_mini_huffman)
        #lp_wrapper=lprofiler(Test_test_2.test_ppm_big)
        #lp_wrapper()
        #lprofiler.print_stats()
     except:

        traceback.print_exc()    

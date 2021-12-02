import matplotlib.pyplot as plot
from Book import BookGraph
from density import WordDensity
from DefaultStemmer import DefaultStemmer
import traceback
import numpy as np
import pandas
import os
import unittest
class Test_Word_Density(unittest.TestCase):
    #
    #In this file I tested to see how word density changes as a text gets longer using journals from Christopher columbus and
    # civil war soldier David B. Arthur
    #
    #
    def test_columbus():
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
    #
    #In this section I used two texts from mark twain and two from O henry to try to compare how the word density changes
    #as you go through a text
    #
    def test_comparison_of_authors():
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
    #
    #I used a ipsum dollar statement to test getting the word density average of a text
    #
    def test_ipsum_dollar():
        
        text=str()
        with open("ipsumDollar.txt",'r') as reader:                
            for line in reader.readlines():
                text=text+line
        ave=WordDensity.get_text_averages(text,4,50)
     
        for num in ave:
            print(num)
        print(WordDensity.get_text_total_average(text,4,50))
    #
    #Here I compared the word density averages of two authors by taking the averages of fifty word sections in their short stories
    #
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
if __name__ == '__main__':
     try:
        Test_Word_Density.test_columbus()
        Test_Word_Density.test_comparison_of_authors()
        Test_Word_Density.test_ipsum_dollar()
        Test_Word_Density.compare_twain_henry()

     except:

        traceback.print_exc()    
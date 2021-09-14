import unittest
import compression
import traceback        
import ppm_compression as ppm
import line_profiler as lp
from treelib import Tree as tr
import os
class Test_ppm(unittest.TestCase):
    #
    #A basic test of my ppm compression algorithm
    #
    def test_ppm():
        esc=2
        text2=""
        with open('text.txt', 'r') as reader:
            for line in reader.readlines():
                text2=text2+line
        text3=""
        with open('markTwain\\barber.txt', 'r') as reader:
            for line in reader.readlines():
                text3=text3+line
        
        
        ppm_class=ppm.ppm_compressor(text2,3,esc)
        print(ppm_class.tree)
        for node in ppm_class.tree.all_nodes():
            print(node.identifier+": "+str(node.data))
        
        compressed=ppm_class.analyze_without_appending("the fox is h0t bass boosted, he 1s not, whatever.")
        print(ppm_class.tree.all_nodes())        
        print(compressed)
    #
    #attempts to test ppm using larger texts
    #and see if i can actually match two texts by the same author
    #eventually I tried using only the first 8000 characters of each text to make the lengths equal
    #
    def test_ppm_big():
        text_frog=""
        with open('markTwain\\frog.txt', 'r') as reader:
            count=0
            for line in reader.readlines():
                for char in line:
                    if count<8000:
                        count+=1
                        text_frog=text_frog+char
        
        text_barber=""
        with open('markTwain\\barber.txt', 'r') as reader:
            count=0
            for line in reader.readlines():
                for char in line:
                    if count<8000:
                        text_barber=text_barber+char
                        count+=1
        
        text_dup=""
        with open('ohenry\\duplicityohargraves.txt', 'r') as reader:
            count=0
            for line in reader.readlines():
                for char in line:
                    if count<8000:
                        count+=1
                        text_dup=text_dup+char
       
        text_gift=""
        with open('ohenry\\giftofthemagi.txt', 'r') as reader:
            count=0
            for line in reader.readlines():
                for char in line:
                    if count<8000:
                        count+=1
                        text_gift=text_gift+char
        
        
        compressed_frog=ppm.ppm_compressor(text_frog,5,1)        
        compressed_barber=ppm.ppm_compressor(text_barber,5,1)
        compressed_dup=ppm.ppm_compressor(text_dup,5,1)
        compressed_gift=ppm.ppm_compressor(text_gift,5,1)
        print(len(compressed_frog.tree.all_nodes()))
        print(len(compressed_barber.tree.all_nodes()))
        print(len(compressed_dup.tree.all_nodes()))
        print(len(compressed_gift.tree.all_nodes()))
        
        print("twain on twain"+str(compressed_frog.analyze_without_appending(text_barber)))        
        print("henry on twain"+str(compressed_dup.analyze_without_appending(text_barber)))       
        print("henry on twain"+str(compressed_gift.analyze_without_appending(text_barber)))        
        print("twain on henry"+str(compressed_frog.analyze_without_appending(text_dup)))
        print("twain on henry"+str(compressed_barber.analyze_without_appending(text_dup)))
        print("henry on henry"+str(compressed_gift.analyze_without_appending(text_dup)))        
        print("twain on henry"+str(compressed_frog.analyze_without_appending(text_gift)))        
        print("twain on henry"+str(compressed_barber.analyze_without_appending(text_gift)))        
        print("henry on henry"+str(compressed_dup.analyze_without_appending(text_gift)))       
        print("henry on twain"+str(compressed_dup.analyze_without_appending(text_frog)))        
        print("twain on twain"+str(compressed_barber.analyze_without_appending(text_frog)))
        print("henry on twain"+str(compressed_gift.analyze_without_appending(text_frog)))
    #
    #As my previous test wasn't matching very well I decided to try this with a few songs 
    #that are the same thing repeated over and over again
    #
    #
    def test_ppm_obvious():
        text_rs1=""
        with open('mick_jagger\\stones1.txt', 'r') as reader:
            count=0
            for line in reader.readlines():
                for char in line:
                    if count<900:
                        count+=1
                        text_rs1=text_rs1+char
        
        text_rs2=""
        with open('mick_jagger\\stones2.txt', 'r') as reader:
            count=0
            for line in reader.readlines():
                for char in line:
                    if count<900:
                        count+=1
                        text_rs2=text_rs2+char
        
        text_dm1=""
        with open('Mcclain\\pie_partone.txt', 'r') as reader:
            count=0
            for line in reader.readlines():
                for char in line:
                    if count<900:
                        count+=1
                        text_dm1=text_dm1+char
       
        text_dm2=""
        with open('Mcclain\\pie_parttwo.txt', 'r') as reader:
            count=0
            for line in reader.readlines():
                for char in line:
                    if count<900:
                        count+=1
                        text_dm2=text_dm2+char
        
        print(len(text_rs1))
        print(len(text_rs2))
        print(len(text_dm1))
        print(len(text_dm2))
        compressed_rs1=ppm.ppm_compressor(text_rs1,4,1)        
        compressed_rs2=ppm.ppm_compressor(text_rs2,4,1)
        compressed_dm1=ppm.ppm_compressor(text_dm1,4,1)
        compressed_dm2=ppm.ppm_compressor(text_dm2,4,1)
        
        print("stones on stones"+str(compressed_rs2.analyze_without_appending(text_rs1)))        
        print("mclean on stones"+str(compressed_dm1.analyze_without_appending(text_rs1)))       
        print("mclean on stones"+str(compressed_dm2.analyze_without_appending(text_rs1)))        
        print("stones on mclean"+str(compressed_rs1.analyze_without_appending(text_dm1)))
        print("stones on mclean"+str(compressed_rs2.analyze_without_appending(text_dm1)))
        print("mclean on mclean"+str(compressed_dm2.analyze_without_appending(text_dm1)))        
        print("stones on mclean"+str(compressed_rs1.analyze_without_appending(text_dm2)))        
        print("stones on mclean"+str(compressed_rs2.analyze_without_appending(text_dm2)))        
        print("mclean on mclean"+str(compressed_dm1.analyze_without_appending(text_dm2)))       
        print("mclean on stones"+str(compressed_dm1.analyze_without_appending(text_rs2)))        
        print("stones on stones"+str(compressed_rs1.analyze_without_appending(text_rs2)))
        print("mclean on stones"+str(compressed_dm2.analyze_without_appending(text_rs2)))
    #
    #same as test ppm_big but this time instead of calculating the cost of compression of one file when another is 
    #already compressed I use ncd to see what file matches what. A little more successful
    #
    #
    def test_ncd():
        
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
        
        print("barber on frog"+str(ppm.ppm_compressor.get_ncd(text_barber,text_frog,3,2)))        
        print("barber on dup"+str(ppm.ppm_compressor.get_ncd(text_barber,text_dup,3,2)))       
        print("barber on gift"+str(ppm.ppm_compressor.get_ncd(text_barber,text_gift,3,2)))        
        print("frog on dup"+str(ppm.ppm_compressor.get_ncd(text_frog,text_dup,3,2)))
        print("frog on gift"+str(ppm.ppm_compressor.get_ncd(text_frog,text_gift,3,2)))
        print("dup on gift"+str(ppm.ppm_compressor.get_ncd(text_dup,text_gift,3,2)))  
    #
    #the same as last test with an expanded dataset
    #
    #
    def test_expanded_ncd():
        texts=list()   
        twain_folder=os.listdir("C:\\Users\\vdh24\\source\\repos\\GraphAnalysis\\markTwain")
        henry_folder=os.listdir("C:\\Users\\vdh24\\source\\repos\\GraphAnalysis\\ohenry")
        for file in twain_folder:
            dictionary=dict()
            texts.append(dictionary)
            dictionary["filename"]=file
            dictionary["text"]=""
            with open("markTwain\\"+file,'r') as reader:
                for line in reader.readlines():
                    dictionary["text"]+=line
        for file in henry_folder:
            dictionary=dict()
            texts.append(dictionary)
            dictionary["filename"]=file
            dictionary["text"]=""
            with open("ohenry\\"+file,'r') as reader:
                for line in reader.readlines():
                    dictionary["text"]+=line
        for i in range(len(texts)-1):
            first=texts[i]
            for j in range(i+1,len(texts)):
                second=texts[j]
                print(first["filename"]+" "+second["filename"]+" "+str(ppm.ppm_compressor.get_ncd(first["text"],second["text"],3,2)))
    def test_profiling():
        twain_folder=os.listdir("C:\\Users\\vdh24\\source\\repos\\GraphAnalysis\\markTwain")
        ohenry_folder=os.listdir("C:\\Users\\vdh24\\source\\repos\\GraphAnalysis\\ohenry")
        test_folder=os.listdir("C:\\Users\\vdh24\\source\\repos\\GraphAnalysis\\test_folder")
        ohenry_text=""
        twain_text=""        
        for file in ohenry_folder:
            
            with open("ohenry\\"+file,'r') as reader:
                for line in reader.readlines():
                    ohenry_text+=line            
        for file in twain_folder:
            text=""
            with open("markTwain\\"+file,'r') as reader:                
                for line in reader.readlines():
                    twain_text+=line
            
        for file in test_folder:
            text=""
            with open("test_folder\\"+file,'r') as reader:
                for line in reader.readlines():
                    text+=line
            print(file)
            print("twain"+str(ppm.ppm_compressor.get_ncd(twain_text,text,3,2)))
            print("ohenry"+str(ppm.ppm_compressor.get_ncd(ohenry_text,text,3,2)))
    def test_appending():
        text2=""
        with open('text.txt', 'r') as reader:
            for line in reader.readlines():
                text2=text2+line
        to_append=ppm.ppm_compressor(text2,2,2,None)
        print(to_append.tree)
        for node in to_append.tree.all_nodes():
            print(node.identifier+": "+str(node.data))
        to_append.append_text("the fox is h0t bass boosted, he 1s not, whatever.")
        print(to_append.tree)
        for node in to_append.tree.all_nodes():
            print(node.identifier+": "+str(node.data))
    def test_sentences():
        twain_folder=os.listdir("C:\\Users\\vdh24\\source\\repos\\GraphAnalysis\\markTwain")
        ohenry_folder=os.listdir("C:\\Users\\vdh24\\source\\repos\\GraphAnalysis\\ohenry")
        ohenry_text=""
        twain_text=""        
        for file in ohenry_folder:
            
            with open("ohenry\\"+file,'r') as reader:
                for line in reader.readlines():
                    ohenry_text+=line            
        for file in twain_folder:
            text=""
            with open("markTwain\\"+file,'r') as reader:                
                for line in reader.readlines():
                    twain_text+=line
        count=0
        with open("single_quotes.txt",'r') as reader:
            for line in reader.readlines():
                count+=1
                if count%2==1:
                    print(line)
                else:
                    print(len(line))
                    print("twain "+str(ppm.ppm_compressor.get_ncd(twain_text,line,3,2)))
                    print("ohenry "+str(ppm.ppm_compressor.get_ncd(ohenry_text,line,3,2)))
                
if __name__ == '__main__':
    try:
        Test_ppm.test_ppm()
        Test_ppm.test_ppm_big()
        Test_ppm.test_ppm_obvious()
        Test_ppm.test_ncd()
        Test_ppm.test_expanded_ncd()
        Test_ppm.test_profiling()
        Test_ppm.test_appending()
        Test_ppm.test_sentences()
        

    except:
        traceback.print_exc()

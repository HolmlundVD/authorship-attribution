import pandas as pd
import csv
import ujson as json
import traceback
import line_profiler as lp
import test_IB as ib
class bitcoin_reader(object):
    training_file="bitcoin\\training"
    testing_file="bitcoin\\testing"
    verification_file="bitcoin\\verify"
    #
    #with this method we are reading the tweet file
    #and creating text files representing the tweets based off of it
    #
    #
    def read_csv():
        path="Bitcoin_tweets.csv"
        lines=1489948
        line=0
        comments=dict()      
        threshold=80
        with open("Bitcoin_tweets.csv",encoding="utf-8") as csv_file:            
            csv_reader=csv.reader(csv_file,delimiter=",")           
            for row in csv_reader:             
              if line==0:
                  line+=1
                  continue            
              if len(row)!=13:
                  line+=1
                  continue
              else:    
                  
                  if not row[0] in comments.keys():                     
                      comments[row[0]]=list()
                      comments[row[0]].append(row[9])
                  else:
                      
                      comments[row[0]].append(row[9])             
        
            
        filtered_comments={k:v for k,v in comments.items() if len(v)>=threshold}      
        bitcoin_reader.make_comment_file(filtered_comments,threshold)
    #
    #this does the file creation aspect of making a text file for our tweets
    #
        
    def make_comment_file(comments:dict,threshold:int):
        training=dict()
        testing=list()
        verify=list()
        for author in comments:
            line=0            
            training[author]=list()
            training[author].append(len(comments[author]))
            training[author].append("")
            total_lines=len(comments[author])
            while(line<round(total_lines*0.6)):               
                training[author][1]+=comments[author][line]+chr(3)
                line+=1                 
            while(line<round(total_lines*0.8)):
                testing.append((author,comments[author][line]))
                line+=1            
            while(line<total_lines):
                verify.append((author,comments[author][line]))
                line+=1    
        
        with open(bitcoin_reader.training_file+str(threshold)+".txt",'w') as file:
            json.dump(training,file)
        with open(bitcoin_reader.testing_file+str(threshold)+".txt",'w') as file:
            json.dump(testing,file)
        with open(bitcoin_reader.verification_file+str(threshold)+".txt",'w') as file:
            json.dump(verify,file)
    #
    #this method takes the texts and tests them according to the test_IB framework
    #
    def test_comment_file(train_file,test_file):
        total_authors=0
        total_found=0
        train_data=dict()
        test_data=list()
        with open(train_file) as text:
            train_data=json.load(text) 
        text_list=list()
        for author in train_data.keys():         
            text_list.append(train_data[author][1])
        top_authors_training=dict()
        for author in train_data.keys():
            top_authors_training[author]=ib.train(0.7,3,string_list=text_list,input_text=train_data[author][1])
            for symbol in top_authors_training[author].keys():
                top_authors_training[author][symbol]+=10**-20
        print("training concluded")
        with open(test_file) as test_texts:
            test_data=json.load(test_texts)
        for comment in test_data:
            comment_freqs=(comment[0],tib.test(2,text=comment[1]))                   
            for symbol in comment_freqs.keys():                       
               comment_freqs[1][symbol]+=10**-20
            best_matched_author=""
            best_matched_score=sys.maxsize
            for author in top_authors_training.items():
                score=it.KLD(comment_freqs[1],author[1],10**-20)
                if score<best_matched_score:                            
                    best_matched_author=author[0]
                    best_matched_score=score                    
                    if comment[0]==best_matched_author:
                        total_matched+=1
        print(len(test_data))
        print(total_matched)

    def run_test_hmm_ad(train_file,test_file,context_len:int):
        
        with open(train_file) as text:
            train_data=json.load(text)
        frequencies_list=list()
        print(len(train_data.items()))
        for author,comments in train_data.items():
            print(author)
            temp=ib.test(context_len,text=comments[1])
            temp["author"]=author
            frequencies_list.append(temp)
        print("creating frame")
        freqs_frame=pd.DataFrame(frequencies_list)
        print(freqs_frame)

    def temp_method():
        bitcoin_reader.run_test_hmm_ad(bitcoin_reader.training_file+"80.txt",bitcoin_reader.testing_file+"80.txt",3)
if __name__=="__main__":
    try:
        
        lprofiler = lp.LineProfiler()  
        lprofiler.add_function(bitcoin_reader.run_test_hmm_ad)
        lp_wrapper=lprofiler(bitcoin_reader.temp_method)
        lp_wrapper()
        lprofiler.print_stats()
       
    except:
        traceback.print_exc()
    
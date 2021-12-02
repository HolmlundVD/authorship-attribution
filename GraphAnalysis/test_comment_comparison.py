from youtube_info import youtube_info as yi
import test_IB as tib
import Info_Theory as it
import json 
import sys
import traceback
import line_profiler as lp
class test_comment_comparison(object):
    folder_prefix="commentFiles\\"
    #
    #given a youtube channel a start and an endpoint in the channels playlist. This method will attempt to
    #identify the writer of each comment that appears in the channels comment json file from the videos in the specified
    #range in the playlist
    #
    def test_comments(channel,range_start,range_end):
        with open(test_comment_comparison.folder_prefix+channel) as text:
            data=json.load(text)  
        total_matched=0
        total_found=0
        top_commenters_training=dict()
        api=yi()
        playlist=api.get_channel_upload_playlist(channel)
        videos_in_range=api.get_videos_in_playlist(playlist,range_start,range_end)        
        new_comment_testing=[]

        list_of_texts=[]
        for commenter in data:
            list_of_texts.append(commenter[0])
        for commenter in data:           
            
            top_commenters_training[commenter[0]]=tib.train(0.7,2,string_list=list_of_texts,input_text=commenter[1][1])
            for symbol in top_commenters_training[commenter[0]].keys():
                top_commenters_training[commenter[0]][symbol]+=10**-20
        
        for video in videos_in_range:
            vid_comments=api.get_comments_from_video(video)
            for comment in vid_comments:
                found_in_keys=False
                
                if comment[0] in top_commenters_training.keys():
                    total_found+=1
                    new_comment_testing.append([comment[0],tib.test(2,text=comment[1])])                    
                    for symbol in new_comment_testing[len(new_comment_testing)-1][1].keys():                       
                        new_comment_testing[len(new_comment_testing)-1][1][symbol]+=10**-20
                    best_matched_author=""
                    best_matched_score=sys.maxsize
                    for author in top_commenters_training.items():
                        score=it.KLD(new_comment_testing[len(new_comment_testing)-1][1],author[1],10**-20)
                        
                        if score<best_matched_score:
                            
                            best_matched_author=author[0]
                            best_matched_score=score                    
                    if comment[0]==best_matched_author:
                        total_matched+=1
                    print(comment[0])
                    print("was written by")
                    print(best_matched_author)
        print(total_matched)
        print(total_found)
    
    def test_functions():
        yi.make_comment_file("AGADMATOR",10,5,20)
        test_comment_comparison.test_comments("AGADMATOR",0,5)
if __name__ == '__main__':
    try:
        lprofiler = lp.LineProfiler()
        lprofiler.add_function(test_comment_comparison.test_comments)
        lprofiler.add_function(yi.make_comment_file)
        lprofiler.add_function(yi.get_videos_in_playlist)
        lprofiler.add_function(yi.get_comments_from_video)
        lprofiler.add_function(yi.get_channel_upload_playlist)
        lp_wrapper=lprofiler(test_comment_comparison.test_functions)
        lp_wrapper()
        lprofiler.print_stats()
       
    except:
        traceback.print_exc()
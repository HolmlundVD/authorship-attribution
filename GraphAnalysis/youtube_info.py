from googleapiclient.discovery import build
import traceback
import json
import sys
import os

class youtube_info(object):
    api_key_file = "api_key.txt"
    api_service_name = "youtube"
    api_version = "v3"
    path_of_files="C:\\Users\\17017\\source\\repos\\GraphAnalysis\\commentFiles\\"
    short_path="commentFiles\\"
    #
    #constructs a youtube api resource that can be used in other methods    
    #
    def __init__(self):
        with open(youtube_info.api_key_file,"r") as file:
            api_key=file.read()
        self.api_resource=build(youtube_info.api_service_name,youtube_info.api_version,developerKey=api_key)
    #
    #given a youtube channel a minimum threshold of comments and 
    # a start and end index this method will return a list of all youtube user's who have at least the threshold number 
    #of comments on videos that are in the range bounded by the given start and end index in the video playlist 
    # of the youtube channel provided
    #

    def make_comment_file(channel,threshold,start,end):
        object=youtube_info()
        id_of_playlist=object.get_channel_upload_playlist(channel)
        
        list_of_videos=object.get_videos_in_playlist(id_of_playlist,start,end)
        comments=list()
        
        for video in list_of_videos:
            print(video)
            comments.extend(object.get_comments_from_video(video))
        comments_by_person=dict()
        for comment in comments:
            
            if comment[0] in comments_by_person.keys():
                comments_by_person[comment[0]][0]+=1                
                comments_by_person[comment[0]][1]+=comment[1]+chr(3)
            else:                
                comments_by_person[comment[0]]=list()
                comments_by_person[comment[0]].append(1)
                comments_by_person[comment[0]].append(comment[1]+chr(3))
        filtered_dict={k:v for k,v in comments_by_person.items() if v[0]>=10}
        dict_sorted=sorted(filtered_dict.items(),key=lambda x:x[1][0],reverse=True)       
        with open(youtube_info.short_path+channel,'w') as file:
            json.dump(dict_sorted,file)
        return file
    @staticmethod
    def test():
        
        object=youtube_info()
        print("object")
        id_of_playlist=object.get_channel_upload_playlist("AGADMATOR")          
        list_of_videos=object.get_videos_in_playlist(id_of_playlist,0,sys.maxsize)
        comments=list()
        for i in range(50):            
            comments.extend(object.get_comments_from_video(list_of_videos[i]))
        

        comments_by_person=dict()
        for comment in comments:
            if comment[0] in comments_by_person.keys():
                comments_by_person[comment[0]][0]+=1                
                comments_by_person[comment[0]][1]+=comment[1]+chr(3)
            else:
                
                comments_by_person[comment[0]]=list()
                comments_by_person[comment[0]].append(1)
                comments_by_person[comment[0]].append(comment[1])
        filtered_dict={k:v for k,v in comments_by_person.items() if v[0]>=10}
        dict_sorted=sorted(filtered_dict.items(),key=lambda x:x[1][0],reverse=True)
        print(dict_sorted)
        print(len(dict_sorted))
        
        with open("comment_section.txt",'x') as comment_file:
            json.dump(dict_sorted,comment_file)
        
    #
    #given the name of a channel this method will return the id of it's upload playlist
    #can use either the id or username of the channel
    #
    #
    def get_channel_upload_playlist(self,channel_name:str):
        try:
            request=self.api_resource.channels().list(
                part="snippet,contentDetails,statistics,id",
                forUsername=channel_name
                )
            response=request.execute()              
            return response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
        except:
            request=self.api_resource.channels().list(
                part="snippet,contentDetails,statistics,id",
                id=channel_name
                )
            response=request.execute() 
            print("this"+str(response))
            return response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
    #
    #given the playlist id this will return a list of the 
    #of all videos in the playlist in the range of the specified integers
    #
    def get_videos_in_playlist(self,playlist_id,start,end):
        
        list_of_videos=list()              
        next_page=None
        count=0
        ##python does not have a do while loop this is very similar to one
        while count<end:                
            
            request=self.api_resource.playlistItems().list(
                part="id,snippet,contentDetails,status",
                playlistId=playlist_id,
                maxResults=50,   
                pageToken=next_page
                )                
            response=request.execute()             
            for video in response["items"]:                
                if count>=start:                  
                    if count>=end:                        
                        return list_of_videos                    
                    list_of_videos.append(video["contentDetails"]["videoId"])
                count+=1
            if "nextPageToken" not in response.keys():
                return list_of_videos
            next_page=response["nextPageToken"]
        return list_of_videos
    
    #
    #given a video id this will return a list of all comments in the video
    #
    #
    def get_comments_from_video(self,video_id):
        list_of_comments=list()
        next_page=None
        ##python does not have a do while loop this is very similar to one
        while True:
            comment_request=self.api_resource.commentThreads().list(
                part="id,replies,snippet",
                videoId=video_id,
                maxResults=100,
                pageToken=next_page
                )            
            thread_response=comment_request.execute()                        
            for comment_thread in thread_response["items"]:                 
                list_of_comments.append([comment_thread["snippet"]["topLevelComment"]["snippet"]["authorDisplayName"]
                                         ,comment_thread["snippet"]["topLevelComment"]["snippet"]["textDisplay"]])       
                if "replies" in comment_thread.keys():
                    for reply in comment_thread["replies"]["comments"]:                             
                        list_of_comments.append([reply["snippet"]["authorDisplayName"],reply["snippet"]["textDisplay"]])
            if "nextPageToken" not in thread_response.keys():               
                return list_of_comments
            next_page=thread_response["nextPageToken"]
    

if __name__ == '__main__':
        try:
            youtube_info.test()
            
        except:
            traceback.print_exc()    
    
    
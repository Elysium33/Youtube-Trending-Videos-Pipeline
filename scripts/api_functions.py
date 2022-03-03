import requests
import pandas as pd
import time
from credentials import API_KEY
from datetime import datetime

today = datetime.now()
today_string = "%s-%d-%d" %(today.month, today.day, today.year)


def request_func(url):
    response = requests.get(url)
    return response.json()


def get_video_details(region_code, video_id):
    url = "https://www.googleapis.com/youtube/v3/videos?id="+video_id+"&part=statistics&key="+API_KEY
    response = request_func(url)
    
    view_count = response['items'][0]['statistics']['viewCount']
    try:
        #this try statement is here in case likes are blocked
        like_count = response['items'][0]['statistics']['likeCount']
    except:
        like_count = 0
    try:
        #this try statement is here in case comments are blocked
        comment_count = response['items'][0]['statistics']['commentCount']
    except:
        comment_count = 0
    
    return view_count, like_count, comment_count

def get_videos(region_code, pageToken):

    page_token = pageToken
    url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet&chart=mostPopular&regionCode={region_code}&key={API_KEY}&maxResults=50&pageToken={page_token}"
    
    response = request_func(url)
    time.sleep(1)
    
    all_data = []
    
    for video in response['items']:
        final_dict = {}
        
        if video['kind'] == "youtube#video":
            
            final_dict['channel_name'] = video['snippet']['channelTitle']
            final_dict['channel_id'] = video['snippet']['channelId']
            final_dict['video_title'] = video['snippet']['title']
            final_dict['video_id'] = video['id']
            final_dict['publish_date'] = video['snippet']['publishedAt']
            final_dict['trending_date'] = today_string

            view_count, like_count, comment_count = get_video_details(region_code, video['id'])
            
            final_dict['view_count'] = view_count
            final_dict['like_count'] = like_count
            final_dict['comment_count'] = comment_count
            
            final_dict['description'] = video['snippet']['description']
            final_dict['thumbnail'] = video['snippet']['thumbnails']['high']['url']
            
            try:
                final_dict['tags'] = video['snippet']['tags']
            except:
                final_dict['tags'] = []
                
            final_dict['category_id'] = video['snippet']['categoryId']
            
        all_data.append(final_dict)
            
    return all_data, response['nextPageToken']
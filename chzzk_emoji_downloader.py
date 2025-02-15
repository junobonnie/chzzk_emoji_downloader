# -*- coding: utf-8 -*-
"""
Created on Mon Dec 23 04:21:36 2024

@author: replica
"""

import requests
import time
import os

def get_streamer_no(url: str) -> str:
    return url.split("/")[-1]

def join_path(a: str, b: str) -> str:
    if a == "":
        return b
    else:
        return "%s/%s"%(a, b)
    
def createDirectory(directory: str):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print("Error: Failed to create the directory.")

def get_streamer_name(streamer_no: str) -> str:
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"}
    
    data = requests.get("https://api.chzzk.naver.com/service/v1/channels/%s"%(streamer_no), headers = headers).json()
    return data["content"]["channelName"]

def get_emoji_ext(emoji_url: str) -> str:
    return emoji_url.split(".")[-1]
    
def download_emojis(streamer_no :str, download_path: str = ""):
    streamer_name = get_streamer_name(streamer_no)
    
    abs_path = join_path(download_path, streamer_name)
    createDirectory(abs_path)
    
    data = requests.get("https://api.chzzk.naver.com/commercial/v1/channels/%s/subscription/tiers"%(streamer_no)).json()
    emojis = data["content"]["subscriptionTierInfoList"][-1]["subscriptionEmojiList"]
    for emoji in emojis:
        # 다운받을 이미지 url
        emoji_url = emoji["imageUrl"]
        ext = get_emoji_ext(emoji_url)
        # time check
        start = time.time()
        
        with open("%s/%s.%s"%(abs_path, emoji["emojiId"], ext), 'wb') as f:
            f.write(requests.get(emoji_url).content)
        
        # 이미지 다운로드 시간 체크
        print(time.time() - start)


if __name__ == "__main__":
    url = "https://chzzk.naver.com/live/b68af124ae2f1743a1dcbf5e2ab41e0b"
    streamer_no = get_streamer_no(url)
    download_emojis(streamer_no)



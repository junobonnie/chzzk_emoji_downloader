# -*- coding: utf-8 -*-
"""
Created on Sun Feb 16 01:11:04 2025

@author: replica
"""
import chzzk_emoji_downloader as ced
import requests
import customtkinter as ctk
from tkinter import filedialog
import os
import threading

GREEN = "#1fa372"

def download_emojis(streamer_no :str, download_path: str = ""):
    streamer_name = ced.get_streamer_name(streamer_no)
    abs_path = ced.join_path(download_path, streamer_name)
    ced.createDirectory(abs_path )
    
    data = requests.get("https://api.chzzk.naver.com/commercial/v1/channels/%s/subscription/tiers"%(streamer_no)).json()
    emojis = data["content"]["subscriptionTierInfoList"][-1]["subscriptionEmojiList"]
  
    emoji_number = len (emojis)
    progress_bar.set(0.)
    for i, emoji in enumerate(emojis):
        # 다운받을 이미지 url
        emoji_url = emoji["imageUrl"]
        ext = ced.get_emoji_ext(emoji_url)
        # time check
        
        with open("%s/%s.%s"%(abs_path, emoji["emojiId"], ext), 'wb') as f:
            f.write(requests.get(emoji_url).content)
        
        # 이미지 다운로드 시간 체크
        progress_update((i+1)/emoji_number)
    progress_update(1.)
        
def on_button_click():
    def task():
        url = entry.get()
        streamer_no = ced.get_streamer_no(url)
        
        download_path = path_entry.get()
        if url == "":
            pass
        else:
            download_emojis(streamer_no, download_path)
    
    thread = threading.Thread(target=task)
    thread.start()
    
def save_download_path(path: str):
    with open("config", "w") as f:
        f.write(path)

def load_download_path():
    with open("config", "r") as f:
        path = f.read()
        if not path == "":
            path_entry.insert(0, path)
            
def select_download_path():
    init_path = path_entry.get()
    if init_path == "":
        init_path = os.getcwd()
        
    path = filedialog.askdirectory(title = "다운로드 폴더 선택창", initialdir = init_path)
    if path:
        path_entry.delete(0, "end")
        path_entry.insert(0, path)
        save_download_path(path)

def open_download_path():
    path = path_entry.get()
    if path == "":
        path = os.getcwd()
    
    if os.path.isdir(path):
        os.startfile(path)

def progress_update(value):
    progress_bar.set(value)
    download_percent_label.configure(text="%.2f%%"%(value*100))
    
# UI 초기화
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("치지직 구독티콘 다운로더")
root.geometry("500x150")
root.iconbitmap("icon.ico")

# URL 입력 필드
entry = ctk.CTkEntry(root, placeholder_text="스트리머의 방송주소를 입력하세요")
entry.pack(pady=10, padx=25, fill='x')

# 다운로드 경로 입력 필드 및 버튼
path_frame = ctk.CTkFrame(root, fg_color="transparent")
path_frame.pack(pady=10, padx=20, fill='x')

path_entry = ctk.CTkEntry(path_frame, placeholder_text="다운로드 경로를 선택하세요", width=200)
path_entry.pack(side="left", fill='x', expand=True, padx=5)

load_download_path()

path_button = ctk.CTkButton(path_frame, text="찾기", command=select_download_path, width=20)
path_button.pack(side="left", padx=5)

open_button = ctk.CTkButton(path_frame, text="열기", command=open_download_path, width=20)
open_button.pack(side="right", padx=5)

# 다운로드 버튼
download_frame = ctk.CTkFrame(root, fg_color="transparent")
download_frame.pack(pady=10, padx=20, fill='x')

# 진행 상태 바
progress_bar = ctk.CTkProgressBar(download_frame)
progress_bar.pack(side="left", fill='x', expand=True, padx=5)
progress_bar.set(0)

download_percent_label = ctk.CTkLabel(download_frame, text="0.0%", text_color=GREEN, width=50)
download_percent_label.pack(side="left", padx=5)

# 확인 버튼 및 진행 상태 바 배치
button = ctk.CTkButton(download_frame, text="다운로드", command=on_button_click, width=90)
button.pack(side="right", padx=5)

# 실행
root.mainloop()

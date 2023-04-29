from tkinter import *
from tkinter import ttk
import tkinter as tk
import requests
from bs4 import BeautifulSoup as bsp4
import re
from Play import Play
from function import ScrollableFrame

song_list = []
btn_list = []
def Open_Song(s_url = "", title=""):
    Play(s_url, title)

def Search(btn_list, frame):
    for i in range(len(btn_list)):
        btn_list[i].destroy()
    tt = title_text.get()
    url = 'https://utaten.com/search?layout_search_text='+ tt +'&layout_search_type=title'
    res = requests.get(url)
    soup = bsp4(res.text, "html.parser")
    element = soup.find("main")
    elements = element.find_all("p", class_="searchResult__title")
    elements2 = element.find_all("p", class_="searchResult__name")
    for i in range(len(elements)):
        k_u = str(elements[i].a.get('href'))
        t_t = str(elements[i].a.text).replace(" ", "").replace('\n', '')
        btn = ttk.Button(frame.scrollable_frame, 
                         text= t_t + str(elements2[i].a.text).replace(" ", ""),
                         padding=(5,10),
                         width=60,
                         command=lambda:Open_Song(k_u, t_t))
        btn.pack(side = "top")
        btn_list.append(btn)
root = Tk()
root.title("Main Window")
root.geometry("800x500")
root.minsize(width=400, height=400)

frame = ScrollableFrame(root)

label = ttk.Label(root, text = "曲名を入力", font=("", 20), padding=(5, 20), compound=CENTER)
title_text = StringVar()
entry = ttk.Entry(root, width=60, textvariable=title_text)
button = ttk.Button(root, text = "OK", command=lambda:Search(btn_list, frame))

label.pack()
entry.pack()
button.pack()
frame.pack()

root.mainloop()

from tkinter import *
from tkinter import ttk
import tkinter as t
import requests
from bs4 import BeautifulSoup as bsp4
import re

start_flag = False
ctn = 3
label = None
entry = None
root = None
kasi_list = None
def Play(url, title):
    global kasi_list
    res = requests.get("https://utaten.com" + url)
    soup = bsp4(res.text, "html.parser")
    elem = str(soup.find("div", class_="hiragana"))
    print(elem)
    exit()
    kasi_list = elem.split('<br/>')
    kasi_list = [s for s in kasi_list if s]

    global label
    global root
    root = Tk()
    root.title(title)
    root.geometry("600x300")
   
    label = ttk.Label(root, text="スペースキーでスタート", font=70)
    label.pack()
   
    root.bind("<KeyPress>", Key_down)
    root.mainloop()

def Key_down(e):
    global key
    global start_flag
    key = e.keycode
    if key == 32 and start_flag == False:
        start_flag = True
        count()
    elif key == 13 and start_flag == True:
        global kasi_list, entry
        check_text = str(entry.get()).replace(" ","")
        if check_text.casefold() == kasi_list[0].casefold():
            entry.delete(0, t.END)
            kasi_list.pop(0)
            Show()

def count():
    global label
    global ctn
    label["text"] = ctn
    ctn -= 1
    if ctn == -1:
        Show()
    else:
        root.after(1000, count)

def Show():
    global kasi_list, entry, root
    if entry == None:
        entry = ttk.Entry(root, width=300)
        entry.pack()
    
    if len(kasi_list) == 0:
        label["text"] = "終了"
    else:
        entry.focus_set()
        label["text"] = kasi_list[0]
        kasi_list[0].replace(" ", "")

from customtkinter import *
import customtkinter as ctk
import requests
from bs4 import BeautifulSoup as bsp4
from Play import Play_w

song_list = []
btn_list = []
def Open_Song(i):
    def x():
        global song_list
        play = Play_w(song_list[i][0], song_list[i][1])
    return x

def Search(btn_list, frame):
    global song_list
    song_list = []
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
        song_list.append([k_u, t_t])
        btn = CTkButton(frame, 
                         text= t_t + str(elements2[i].a.text).replace(" ", ""),
                         width=60,
                         command=Open_Song(i))
        btn.pack(side = "top")
        btn_list.append(btn)

if __name__ == "__main__":
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")
    root = CTk()
    root.title("Main Window")
    root.geometry("800x500")
    root.minsize(width=400, height=400)
    
    frame = CTkFrame(root)
    
    label = CTkLabel(root, text = "曲名を入力", font=("", 20))
    title_text = StringVar()
    entry = CTkEntry(root, width=500, textvariable=title_text)
    button = CTkButton(root, text = "OK", command=lambda:Search(btn_list, frame))
    
    label.pack()
    entry.pack()
    button.pack()
    frame.pack()
    
    root.mainloop()
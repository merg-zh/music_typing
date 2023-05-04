from customtkinter import *
import customtkinter as ctk
import requests
from bs4 import BeautifulSoup as bsp4
from Play import Play_w

song_list = []
btn_list = []

class Main():
    def __init__(self):
        self.width = 800
        self.height = 500
        self.btn_list = []
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")
        self.root = CTk()
        self.root.title("Main Window")
        self.root.geometry("800x500")
        self.root.minsize(width=400, height=400)
        self.root.configure(fg_color="white")

        self.main_font = ctk.CTkFont(family = "Yu Gothic", size = 18, weight="bold")
        self.sub_font = ctk.CTkFont(family = "Yu Gothic", size = 15, weight="bold")

        self.frame = CTkScrollableFrame(self.root, width=700, height=350, corner_radius=0, \
                                         border_width=4, border_color="gray", scrollbar_fg_color="gray", \
                                         scrollbar_button_color = "white", scrollbar_button_hover_color = "lightgray")
        self.frame.propagate(False)

        search_frame = CTkFrame(self.root, fg_color="transparent")
        self.label = CTkLabel(search_frame, text = "曲名：", font=self.main_font)
        self.label2 = CTkLabel(search_frame, text = " 歌手名：", font=self.main_font)
        self.title_text = StringVar()
        self.singer_text = StringVar()
        self.entry = CTkEntry(search_frame, width=250, textvariable=self.title_text, font=("Yu Gothic", 20))
        self.entry2 = CTkEntry(search_frame, width=250, textvariable=self.singer_text, font=("Yu Gothic", 20))
        self.button = CTkButton(search_frame, text = "OK", width=40,command=lambda:self.Search())

        self.label.pack(side=ctk.LEFT)
        self.entry.pack(side=ctk.LEFT)
        self.label2.pack(side=ctk.LEFT)
        self.entry2.pack(side=ctk.LEFT)
        self.button.pack(side=ctk.LEFT, padx = 10)
        search_frame.pack(pady = 30)
        self.frame.pack(pady = 50)

        self.root.bind("<Configure>", self.Set_window_size)
        self.root.mainloop()
    
    def Set_window_size(self, event):
        # Main Window以外のイベントは無視
        if (event.type != 'configure') and (event.widget != self.root):
            return
    
        # サイズが変わってなかった無視
        if (event.width == self.width) and (event.height == self.height):
            return
    
        # グローバル変数を更新
        self.width = event.width
        self.height = event.height

        set_fontsize = int(self.width / 44.5 * 100) / 100
        if set_fontsize > 30:
            set_fontsize = 30
        self.main_font.configure(size = int(set_fontsize))

        set_fontsize = int(self.width / 53.3 * 100) / 100
        if set_fontsize > 23:
            set_fontsize = 23
        self.sub_font.configure(size = int(set_fontsize))

        set_width = self.width / 1.14
        set_height = self.height / 1.14
        if set_width > 1000:
            set_width = 1000
        if set_height > 800:
            set_height = 800
        self.frame.configure(width = set_width, height = set_height)
        for i in range(len(self.btn_list)):
            self.btn_list[i].configure(width = set_width)
    
    def Search(self):
        self.song_list = []
        for i in range(len(self.btn_list)):
            self.btn_list[i].destroy()
        tt = self.title_text.get()
        st = self.singer_text.get()
        url = ""
        if tt != "" and st == "":
            url = 'https://utaten.com/search?layout_search_text='+ tt +'&layout_search_type=title'
        elif tt == "" and st != "":
            url = 'https://utaten.com/search?artist_name=' + st
        elif tt != "" and st != "":
            url = 'https://utaten.com/search?sort=popular_sort_asc&artist_name=' + st +'&title=' + tt
        else:
            return
        res = requests.get(url)
        soup = bsp4(res.text, "html.parser")
        element = soup.find("main")
        elements = element.find_all("p", class_="searchResult__title")
        elements2 = element.find_all("p", class_="searchResult__name")
        set_width = self.width / 1.15
        if set_width > 1000:
            set_width = 1000
        for i in range(len(elements)):
            k_u = str(elements[i].a.get('href'))
            t_t = str(elements[i].a.text).replace(" ", "").replace('\n', '')
            self.song_list.append([k_u, t_t])
            btn = CTkButton(self.frame, 
                             text= t_t + str(elements2[i].a.text).replace(" ", ""),
                             width = set_width,
                             command=self.Open_Song(i),
                             corner_radius=0,
                             fg_color="transparent",
                             text_color="#2D2D2D",
                             hover_color="white",
                             font = self.sub_font,
                            )
            btn.grid(row = i, column = 0)
            self.btn_list.append(btn)
    
    def Open_Song(self, i):
        def x():
            play = Play_w(self.song_list[i][0], self.song_list[i][1])
        return x

if __name__ == "__main__":
    main = Main()
from customtkinter import *
import customtkinter as ctk
import requests
from bs4 import BeautifulSoup as bsp4
from Play import Play_w
import os
from pathlib import Path

song_list = []
btn_list = []

class Main():
    def __init__(self):
        self.data_songs = []
        os.makedirs("datas", exist_ok=True)
        data_file = Path('datas/data.dat')
        data_file.touch(exist_ok=True)
        f = open(data_file)
        with open(os.path.join("datas", "data.dat"), encoding="UTF-8") as f:
            self.data_songs = f.readlines()
        for i in range(len(self.data_songs)):
            self.data_songs[i] = self.data_songs[i].split(",")

        self.width = 800
        self.height = 500
        self.song_datas = [[[], []], [[], []], [[], []]]
        self.choose_btns = []
        self.now_open_list = 0
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        self.root = CTk()
        self.root.title("Main Window")
        self.root.geometry("800x500")
        self.root.minsize(width=400, height=400)
        self.root.configure(fg_color="#202020")

        self.main_font = ctk.CTkFont(family = "Yu Gothic", size = 18, weight="bold")
        self.sub_font = ctk.CTkFont(family = "Yu Gothic", size = 15, weight="bold")

        self.frame = CTkScrollableFrame(self.root, width=700, height=350, corner_radius=0, \
                                         border_width=10, border_color="#404040", scrollbar_fg_color="#404040", \
                                         scrollbar_button_color = "#808080", scrollbar_button_hover_color = "#a0a0a0",fg_color="#2f2f2f")
        self.frame.propagate(False)

        search_frame = CTkFrame(self.root, fg_color="#404040", corner_radius=20)
        self.label = CTkLabel(search_frame, text = "　曲名 ", font=self.main_font, text_color="white")
        self.label2 = CTkLabel(search_frame, text = "　歌手名 ", font=self.main_font, text_color="white")
        self.title_text = StringVar()
        self.singer_text = StringVar()
        self.entry = CTkEntry(search_frame, width=250, textvariable=self.title_text, font=("Yu Gothic", 20))
        self.entry2 = CTkEntry(search_frame, width=250, textvariable=self.singer_text, font=("Yu Gothic", 20))
        self.button = CTkButton(search_frame, text = "検索", width=40,command=lambda:self.Search(), font=self.main_font)

        self.choose_frame = CTkFrame(self.root, fg_color="#202020", corner_radius=0, width = 725, height=30)
        self.choose_frame.propagate(False)
        self.search_frame_btn = CTkButton(self.choose_frame, text = "検索結果", width=80, height=30, font=self.main_font, \
                                           corner_radius=0, border_width=4, fg_color="#404040", border_color="#404040", state="disabled", hover_color="#404040", command=lambda:self.Open_list(0))
        self.popular_frame_btn = CTkButton(self.choose_frame, text = "人気の曲", width=80, height=30, font=self.main_font, \
                                            corner_radius=0, border_width=4, fg_color="#2f2f2f", border_color="#404040", hover_color="#404040", command=lambda:self.Open_list(1))
        self.history_frame_btn = CTkButton(self.choose_frame, text = "履歴", width=80, height=30, font=self.main_font, \
                                            corner_radius=0, border_width=4, fg_color="#2f2f2f", border_color="#404040", hover_color="#404040", command=lambda:self.Open_list(2))
        self.choose_btns = [self.search_frame_btn, self.popular_frame_btn, self.history_frame_btn]

        self.label.pack(side=ctk.LEFT)
        self.entry.pack(side=ctk.LEFT)
        self.label2.pack(side=ctk.LEFT)
        self.entry2.pack(side=ctk.LEFT)
        self.button.pack(side=ctk.LEFT, padx = 10)
        search_frame.pack(ipady = 12, ipadx = 12, pady = 20)
        self.search_frame_btn.pack(side=ctk.LEFT)
        self.popular_frame_btn.pack(side=ctk.LEFT)
        self.history_frame_btn.pack(side=ctk.LEFT)
        self.choose_frame.pack()
        self.frame.pack()

        self.root.bind("<Configure>", self.Set_window_size)
        self.root.bind("<KeyPress>", self.Key_down)

        self.root.protocol("WM_DELETE_WINDOW", self.Window_close)
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

        set_fontsize = int(self.width / 44.5)
        if set_fontsize > 30:
            set_fontsize = 30
        self.main_font.configure(size = set_fontsize)

        set_fontsize = int(self.width / 53.3 * 100) / 100
        if set_fontsize > 23:
            set_fontsize = 23
        self.sub_font.configure(size = int(set_fontsize))

        set_width = int(self.width / 1.14)
        set_height = int(self.height / 1.14)

        set_btn_height = int(self.width / 26.6)
        set_btn_width = int(self.width / 10)
        if set_width > 1100:
            set_width = 1100
            set_btn_width = 110
        if set_height > 800:
            set_height = 800
        if set_btn_height > 40:
            set_btn_height = 50
        self.frame.configure(width = set_width, height = set_height)
        self.choose_frame.configure(width = set_width + 26, height = set_btn_height)
        for i in range(3):
            self.choose_btns[i].configure(width = set_btn_width + 10, height = set_btn_height)
            for j in range(len(self.song_datas[i][0])):
                if j != len(self.song_datas[i][0]) - 1:
                    self.song_datas[i][0][j][0].configure(width = set_width)
                    self.song_datas[i][0][j][1].configure(width = set_width)
                else:
                    self.song_datas[i][0][j].configure(width = set_width)

    def Search(self):
        self.Open_list(0)
        self.song_datas[0][1] = []
        for i in range(len(self.song_datas[0][0])):
            if i != len(self.song_datas[0][0]) - 1:
                self.song_datas[0][0][i][0].destroy()
                self.song_datas[0][0][i][1].destroy()
            else:
                self.song_datas[0][0][i].destroy()
        self.song_datas[0][0] = []
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
        self.set_songs(url, 0)
    
    def Open_Song(self, i):
        def x():
            sl = self.song_datas[self.now_open_list][1].copy()
            k_u = sl[i][0]
            t_t = sl[i][1]
            s_t = sl[i][2].replace("\n", "")
            for j in range(len(self.data_songs)):
                if self.data_songs[j][0] == k_u:
                    self.data_songs.pop(j)
                    break
            if len(self.data_songs) > 19:
                self.data_songs.pop(19)
            self.data_songs.insert(0, [k_u, t_t, s_t])

            Play_w(sl[i][0], sl[i][1])
        return x
    
    def Key_down(self, event):
        key = event.keysym
        if key == "Return":
            self.Search()
    
    def set_songs(self, url, list_num=0):
        res = requests.get(url)
        soup = bsp4(res.text, "html.parser")
        element = soup.find("main")
        elements = element.find_all("p", class_="searchResult__title")
        elements2 = element.find_all("p", class_="searchResult__name")
        send_datas = []
        for i in range(len(elements)):
            k_u = str(elements[i].a.get('href'))
            t_t = str(elements[i].a.text).replace(" ", "").replace('\n', '')
            s_t = str(elements2[i].a.text).replace(" ", "").replace('\n', '')
            send_datas.append([k_u,t_t,s_t])
        self.create_btn_canvas(send_datas, list_num)
    
    def create_btn_canvas(self, datas, list_num = 0):
        set_width = self.width / 1.12
        if set_width > 1100:
            set_width = 1100
        for i in range(len(datas)):
            self.song_datas[list_num][1].append(datas[i])
            t_t = datas[i][1]
            s_t = datas[i][2].replace("\n", "")
            if len(t_t) > 47:
                t_t = t_t[0:45] + "\n" +t_t[45:]
            if len(s_t) > 45:
                s_t = s_t[0:45] + "\n" + s_t[45:]
            btn = CTkButton(self.frame, 
                             text = t_t + "\n" + s_t,
                             width = set_width,
                             command=self.Open_Song(i),
                             corner_radius=0,
                             fg_color="transparent",
                             text_color="white",
                             hover_color="#606060",
                             font = self.sub_font,
                            )
            btn.grid(row = i * 2, column = 0)

            if i != len(datas) - 1:
                line_canvs = ctk.CTkCanvas(self.frame, width=set_width, height=5, highlightthickness=0, bg="#404040")
                line_canvs.grid(row = i * 2 + 1, column = 0)
                self.song_datas[list_num][0].append([btn, line_canvs])
            else:
                self.song_datas[list_num][0].append(btn)
    
    def Open_list(self, list_num=0):
        self.now_open_list = list_num
        targets = []
        if list_num == 0:
            targets = [1, 2]
        elif list_num == 1:
            targets = [0, 2]
        else:
            targets = [0,1]
        self.choose_btns[list_num].configure(fg_color="#404040", state="disabled")
        for i in targets:
            self.choose_btns[i].configure(fg_color="#2f2f2f", state="normal")
        for i in range(3):
            for j in range(len(self.song_datas[i][0])):
                if i == list_num:
                    if j != len(self.song_datas[i][0]) - 1:
                        self.song_datas[i][0][j][0].grid(row = j * 2, column = 0)
                        self.song_datas[i][0][j][1].grid(row = j * 2 + 1, column = 0)
                    else:
                        self.song_datas[i][0][j].grid(row = j * 2, column = 0)
                else:
                    if j != len(self.song_datas[i][0]) - 1:
                        self.song_datas[i][0][j][0].grid_forget()
                        self.song_datas[i][0][j][1].grid_forget()
                    else:
                        self.song_datas[i][0][j].grid_forget()
        
        if list_num == 1 and len(self.song_datas[1][0]) == 0:
            url = "https://utaten.com/search?"
            self.set_songs(url, 1)
        
        if list_num == 2:
            self.song_datas[2][1] = []
            for i in range(len(self.song_datas[2][0])):
                if i != len(self.song_datas[2][0]) - 1:
                    self.song_datas[2][0][i][0].destroy()
                    self.song_datas[2][0][i][1].destroy()
                else:
                    self.song_datas[2][0][i].destroy()
            self.song_datas[2][0] = []

            self.create_btn_canvas(self.data_songs, 2)
    
    def Window_close(self):
        with open("datas/data.dat", "w", encoding="UTF-8") as f:
            for i in range(len(self.data_songs)):
                self.data_songs[i] = ",".join(self.data_songs[i])
                if not "\n" in self.data_songs[i]:
                    self.data_songs[i] += "\n"
            f.writelines(self.data_songs)
            self.root.destroy()

if __name__ == "__main__":
    main = Main()
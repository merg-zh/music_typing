from tkinter import *
from tkinter import ttk
import requests
from bs4 import BeautifulSoup as bsp4
import re
import regex
import pykakasi

class Play_w:
    def __init__(self, url, title):
        self.start_flag = False
        self.ctn = 3
        self.label = None
        self.label2 = None
        self.label3 = None
        self.root = None
        self.kasi_list = []
        self.now_str = None

        kakasi = pykakasi.kakasi()
        kakasi.setMode('H', 'a')
        kakasi.setMode('K', 'a')
        self.conversion = kakasi.getConverter()

        res = requests.get("https://utaten.com" + url)
        soup = bsp4(res.text, "html.parser")
        elem = str(soup.find("div", class_="hiragana"))[22:-7].strip()
        elem = elem.replace('<span class="ruby"><span class="rb">', ",").replace("</span></span>", ",").replace('</span><span class="rt">', ",").replace("\n", "").replace("<br>", ",<br>,").replace("<br/>", ",<br>,")
        elems = elem.split(",")
        elems = [s for s in elems if s]
        kari = ["",""]
        p = re.compile('[\u0000-\u007F]+')
        kan = regex.compile(r'\p{Script=Han}+')
        i = 0
        while i < len(elems):
            if i != 0:
                if elems[i] == "<br>" and elems[i - 1] == "<br>":
                    i += 1
                    continue
    
            if elems[i] == "<br>":
                self.kasi_list.append(kari)
                kari = ["", ""]
            elif p.fullmatch(elems[i]):
                kari[0] += elems[i]
                kari[1] += elems[i]
            elif kan.fullmatch(elems[i]):
                kari[0] += elems[i]
                kari[1] += elems[i + 1]
                i += 1
            else:
                kari[0] += elems[i]
                kari[1] += elems[i]
            i += 1
        self.root = Tk()
        self.root.title(title)
        self.root.geometry("1000x400")
        self.root.minsize(width=800, height=400)
       
        self.label = ttk.Label(self.root, text="スペースキーでスタート", font=("", 30))
        self.label2 = ttk.Label(self.root, font=("", 25))
        self.label3 = ttk.Label(self.root, text="\n", font=("", 20))
    
        self.label.pack()
        self.label2.pack()
        self.label3.pack()
       
        self.root.bind("<KeyPress>", self.Key_down)
        
        self.root.mainloop()

    def Key_down(self, e):
        key = e.keysym
        if key == "space" and self.start_flag == False:
            self.start_flag = True
            self.count()
            return
        
        if key == "comma":
            key = ","
        elif key == "exclam":
            key = "!"
        elif key == "period":
            key = "."
        elif key == "question":
            key = "?"
        elif key =="minus":
            key = "-"
        p = re.compile(r'a|i|u|e|o')
        if self.now_str[0:2] == "ch" and key == "t" or self.now_str[0:2] == "sh" and key == "s" or self.now_str[0:2] == "ts" and key == "t":
            self.label3['text'] += key
            self.now_str =self.now_str[2:]
        elif  self.now_str[0] == key or self.now_str[0] == "j" and key == "z" or self.now_str[0] == "f" and key == "h" or self.now_str[0] == "z" and key == "d":
            if len(self.now_str) == 1:
                self.label3['text'] = "\n"
                self.kasi_list.pop(0)
                self.Show()
                return
            self.label3['text'] += key
            self.now_str = self.now_str[1:]
        elif self.now_str[0] == "h" and key == "y" and self.label3['text'][-1] == "s" or p.search(self.now_str[0]) and self.label3['text'][-2:] == "ch":
            self.label3['text'] += key
            self.now_str = self.now_str[1:]
    
    def count(self):
        self.label["text"] = self.ctn
        self.ctn -= 1
        if self.ctn == -1:
            self.Show()
        else:
            self.root.after(1000, self.count)
    
    def Show(self):        
        if len(self.kasi_list) == 0:
            self.label["text"] = "終了"
            self.label2["text"] = ""
        else:
            self.label["text"] = self.kasi_list[0][0]
            self.label2["text"] = self.kasi_list[0][1]
            self.now_str = self.conversion.do(self.kasi_list[0][1].replace("\n", " ").replace("\r", " ").replace(" ", "").replace("　", "").replace("「","").replace("」","").replace("、", ",").lower())
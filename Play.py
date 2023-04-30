from tkinter import *
from tkinter import ttk
import tkinter as tk
import requests
from bs4 import BeautifulSoup as bsp4
import re
import regex
import jaconv
import datetime

class Play_w:
    def __init__(self, url, title):
        self.H2R = {"あ":"a", "い":"i","う":"u","え":"e","お":"o",
                    "か":"ka","き":"ki","く":"ku","け":"ke","こ":"ko",
                    "さ":"sa","し":"si","す":"su","せ":"se","そ":"so",
                    "た":"ta","ち":"ti","つ":"tu","て":"te","と":"to",
                    "な":"na","に":"ni","ぬ":"nu","ね":"ne","の":"no",
                    "は":"ha","ひ":"hi","ふ":"hu","へ":"he","ほ":"ho",
                    "ま":"ma","み":"mi","む":"mu","め":"me","も":"mo",
                    "や":"ya","ゆ":"yu","よ":"yo",
                    "ら":"ra","り":"ri","る":"ru","れ":"re","ろ":"ro",
                    "わ":"wa","を":"wo","ん":"n",
                    "が":"ga","ぎ":"gi","ぐ":"gu","げ":"ge","ご":"go",
                    "ざ":"za","じ":"zi","ず":"zu","ぜ":"ze","ぞ":"zo",
                    "だ":"da","ぢ":"di","づ":"du","で":"de","ど":"do",
                    "ば":"ba","び":"bi","ぶ":"bu","べ":"be","ぼ":"bo",
                    "ぱ":"pa","ぴ":"pi","ぷ":"pu","ぺ":"pe","ぽ":"po",
                    "きゃ":"kya","きゅ":"kyu","きょ":"kyo",
                    "ぎゃ":"gya","ぎゅ":"gyu","ぎょ":"gyo",
                    "しゃ":"sya","しゅ":"syu","しょ":"syo",
                    "じゃ":"zya","じゅ":"zyu","じょ":"zyo",
                    "ちゃ":"tya","ちゅ":"tyu","ちょ":"tyo",
                    "ぢゃ":"dya","ぢゅ":"dyu","ぢょ":"dyo",
                    "にゃ":"nya","にゅ":"nyu","にょ":"nyo",
                    "ひゃ":"hya","ひゅ":"hyu","ひょ":"hyo",
                    "びゃ":"bya","びゅ":"byu","びょ":"byo",
                    "ぴゃ":"pya","ぴゅ":"pyu","ぴょ":"pyo",
                    "みゃ":"mya","みゅ":"myu","みょ":"myo",
                    "りゃ":"rya","りゅ":"ryu","りょ":"ryo",
                    "ぁ":"xa","ぃ":"xi","ぅ":"xu","ぇ":"xe","ぉ":"xo",
                    "ふゃ":"fya","ふゅ":"fyu","ふょ":"fyo",
                    "ふぁ":"fa","ふぃ":"fi","ふぇ":"fe","ふぉ":"fo"}
        
        self.rossita_to_roma={"А":"a","а":"a","Б":"b","б":"b","В":"v",
                              "в":"v","Г":"g","г":"g","Д":"d","д":"d",
                              "Е":"e","е":"e","Ж":"zh","ж":"zh","З":"z",
                              "з":"z","И":"i","и":"i","Й":"y","й":"y",
                              "К":"k","к":"k","Л":"l","л":"l",
                              "М":"m","м":"m","Н":"n","н":"n","О":"o",
                              "о":"o","П":"p","п":"p","Р":"r","р":"r",
                              "С":"s","с":"s","Т":"t","т":"t","У":"u",
                              "у":"u","Ф":"f","ф":"f","Х":"kh","х":"kh",
                              "Ц":"ts","ц":"ts","Ч":"ch","ч":"ch","Ш":"sh",
                              "ш":"sh","Щ":"shch","щ":"shch","Ь":"","ь":"",
                              "Ю":"yu","ю":"yu","Я":"ya","я":"ya",
                              "ゔ":"vu"
                             }
        
        self.key_sp = {
            "comma":",","exclam":"!","period":",","question":"?",
            "minus":"-","apostrophe":"'","ampersand":"&","numbersign":"#",
            "dollar":"$","percent":"%","equal":"=","asciitilde":"~"
        }

        self.table = str.maketrans({
            v: '' for v in '\u3000 \x0c\x0b\t\r'
        })

        self.start_flag = False
        self.finish_flag = False
        self.ctn = 3
        self.label = None
        self.label2 = None
        self.label3 = None
        self.root = None
        self.kasi_list = []
        self.now_str = None
        self.typctn = 0
        self.start_time = 0

        res = requests.get("https://utaten.com" + url)
        soup = bsp4(res.text, "html.parser")
        elem = str(soup.find("div", class_="hiragana"))[22:-7].strip()
        elem = elem.replace('<span class="ruby"><span class="rb">', ",").replace("</span></span>", ",").replace('</span><span class="rt">', ",").replace("\n", "").replace("<br>", ",<br>,").replace("<br/>", ",<br>,")
        elems = elem.split(",")
        elems = [s for s in elems if s]
        kari = ["","", ""]
        self.p = re.compile('[\u0000-\u007F]+')
        kan = regex.compile(r'\p{Script=Han}+')
        i = 0
        while i < len(elems):
            if i != 0:
                if elems[i] == "<br>" and elems[i - 1] == "<br>":
                    i += 1
                    continue
    
            if elems[i] == "<br>":
                kari[0] = kari[0].translate(self.table)
                kari[1] = kari[1].translate(self.table)
                kari[2] = self.Hira_to_Roma(kari[2])
                self.kasi_list.append(kari)
                kari = ["", "", ""]
            elif self.p.fullmatch(elems[i]):
                kari[0] += elems[i]
                kari[1] += elems[i]
                kari[2] += elems[i]
            elif kan.fullmatch(elems[i]):
                kari[0] += elems[i]
                kari[1] += elems[i + 1]
                kari[2] += jaconv.kata2hira(elems[i + 1])
                i += 1
            else:
                kari[0] += elems[i]
                kari[1] += elems[i]
                kari[2] += jaconv.kata2hira(elems[i])
            i += 1
        self.root = Tk()
        self.root.title(title)
        self.root.geometry("1000x400")
        self.root.minsize(width=800, height=400)
       
        self.label = ttk.Label(self.root, text="スペースキーでスタート", font=("", 30), anchor=tk.CENTER)
        self.label2 = ttk.Label(self.root, font=("", 25), anchor=tk.CENTER)
        self.label3 = ttk.Label(self.root, text="\n", font=("", 20), anchor=tk.CENTER)
    
        self.label.pack()
        self.label2.pack()
        self.label3.pack()
       
        self.root.bind("<KeyPress>", self.Key_down)
        
        self.root.mainloop()
    
    def Hira_to_Roma(self, st):
        words_pat = re.compile(r'ゃ|ゅ|ょ|ぁ|ぃ|ぅ|ぇ|ぉ')

        st = st.replace("ー","-").replace("☆", "").replace("(","").replace(")","").replace("「","") \
            .replace("」","").replace("、", ",").replace("・",".").replace("…","...").replace("∽","") \
            .replace("。",".").replace("‥","..")
        
        st = st.translate(self.table)
        
        st = st.lower()
        i = 0
        xtu = False
        while(i < len(st)):
            if self.p.fullmatch(st[i]):
                if xtu:
                    st = st[:i-1] + "xtu" + st[i:]
                    xtu = False
                i += 1
                continue
            tu = st[i]
            if st[i] == "っ":
                xtu = True
                i+=1
                continue

            if len(st) - 1 > i:
                if bool(words_pat.search(st[i + 1])):
                    tu = st[i : i + 2]
            
            try:
                in_t = self.H2R[tu]
            except:
                try:
                    if len(tu) == 2:
                        tu = st[i]
                        in_t = self.H2R[tu]
                    else:
                        in_t = self.rossita_to_roma[tu]
                except:
                    st = st[:i-1] + st[i+1:]
                    i+=1
            
            if xtu:
                st = st[:i-1] + in_t[0] + in_t + st[i+len(tu):]
                i += len(in_t)
                xtu = False
            else:
                st = st[:i] + in_t + st[i+len(tu):]
                i += len(in_t)
            

        return st

    def Key_down(self, e):
        key = e.keysym
        if key == "space" and self.start_flag == False:
            self.start_flag = True
            self.count()
            return
        
        if self.start_flag == False or key == "LeftShift":
            return
        
        try:
            key = self.key_sp[key]
        except:
            None
        
        if  self.now_str[0] == key:
            self.typctn += 1
            if len(self.now_str) == 1:
                self.label3['text'] = "\n"
                self.kasi_list.pop(0)
                self.Show()
                return
            self.label3['text'] += key
            self.now_str = self.now_str[1:]
        elif self.now_str[0:2] == "zy" and key == "j":
            self.typctn += 1
            self.label3['text'] += key
            self.now_str = self.now_str[2:]
        elif len(self.label3['text']) > 2:
            if self.label3['text'][-1] == "n" and self.label3['text'][-2] != "n":
                self.typctn += 1
                self.label3['text'] += key
    
    def count(self):
        self.label["text"] = self.ctn
        self.ctn -= 1
        if self.ctn == -1:
            self.Show()
            self.ctn = 0
            dt = datetime.datetime.now()
            self.start_time = dt.hour * 60 * 60 + dt.minute * 60 + dt.second
        else:
            self.root.after(1000, self.count)
    
    def Show(self):        
        if len(self.kasi_list) == 0:
            self.label["text"] = "終了"
            dt = datetime.datetime.now()
            now_time = dt.hour * 60 * 60 + dt.minute * 60 + dt.second
            heikin = int(self.typctn / (now_time - self.start_time) * 10) / 10
            self.label2["text"] = "1秒あたり - " + str(heikin) + "文字"
            self.finish_flag = True
        else:
            self.label["text"] = "\n" + self.kasi_list[0][0]
            self.label2["text"] = "\n" + self.kasi_list[0][1]
            self.now_str = self.kasi_list[0][2]
            print(self.kasi_list[0][2])

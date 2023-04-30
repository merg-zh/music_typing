from tkinter import *
from tkinter import ttk
import requests
from bs4 import BeautifulSoup as bsp4
import re
import regex
import jaconv

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
                    "ぁ":"xa","ぃ":"xi","ぅ":"xu","ぇ":"xe","ぉ":"xo"}
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
       
        self.label = ttk.Label(self.root, text="スペースキーでスタート", font=("", 30))
        self.label2 = ttk.Label(self.root, font=("", 25))
        self.label3 = ttk.Label(self.root, text="\n", font=("", 20))
    
        self.label.pack()
        self.label2.pack()
        self.label3.pack()
       
        self.root.bind("<KeyPress>", self.Key_down)
        
        self.root.mainloop()
    
    def Hira_to_Roma(self, st):
        words_pat = re.compile(r'ゃ|ゅ|ょ')

        st = st.replace("ー","-").replace("☆", "").replace("(","").replace(")","").replace("「","") \
            .replace("」","").replace("、", ",").replace("・","")
        table = str.maketrans({
            v: '' for v in '\u3000 \x0c\x0b\t'
        })
        st = st.translate(table)
        i = 0
        xtu = False
        while(i < len(st)):
            if self.p.fullmatch(st[i]):
                i += 1
                continue
            tu = st[i]
            if len(st) - 1 > i:
                if bool(words_pat.search(st[i + 1])):
                    tu = st[i : i + 2]
            if st[i] == "っ":
                xtu = True
                i+=1
                continue
            in_t = self.H2R[tu]
            if xtu:
                st = st[:i-1] + in_t[0] + in_t + st[i+len(tu):]
                i += len(in_t)
                xtu = False
            else:
                st = st[:i] + in_t + st[i+len(tu):]
                i += len(in_t)
            

        return st.lower()

    def Key_down(self, e):
        key = e.keysym
        if key == "space" and self.start_flag == False:
            self.start_flag = True
            self.count()
            return
        
        if self.start_flag == False:
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
        elif key == "apostrophe":
            key = "'"
        
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
        elif self.label3[-1] == "n" and self.label3[-2] != "n":
            self.typctn += 1
            self.label3['text'] += key
    
    def count(self):
        self.label["text"] = self.ctn
        self.ctn -= 1
        if self.ctn == -1:
            self.Show()
            self.ctn = 0
            self.root.after(1000, self.count2)
        else:
            self.root.after(1000, self.count)
    
    def count2(self):
        if self.finish_flag:
            self.label2 = "1秒あたりのタイプ数 : " + str(int(self.typctn / self.ctn)) + "文字"
        else:
            self.ctn += 1
            self.root.after(1000, self.count2)
    
    def Show(self):        
        if len(self.kasi_list) == 0:
            self.label["text"] = "終了"
            self.label2["text"] = ""
            self.finish_flag = True
        else:
            self.label["text"] = self.kasi_list[0][0]
            self.label2["text"] = self.kasi_list[0][1]
            self.now_str = self.kasi_list[0][2]
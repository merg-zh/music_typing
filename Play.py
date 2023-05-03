from tkinter import *
from tkinter import ttk
import tkinter as tk
import tkinter.font as tkFont
import requests
from bs4 import BeautifulSoup as bsp4
import re
import regex
import jaconv
import datetime
import asyncio

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
                    "じゃ":"zya","じゅ":"zyu","じょ":"zyo", "じぇ":"je",
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
            "dollar":"$","percent":"%","equal":"=","asciitilde":"~",
            "period":"."
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

        self.line_ctn = 0

        self.width = 800
        self.height = 400

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
        kak = False
        while i < len(elems):
            if i != 0:
                if elems[i] == "<br>" and elems[i - 1] == "<br>":
                    i += 1
                    continue
            if "≪" in elems[i]:
                kak = True
                i += 1
                continue
            if "≫" in elems[i] and kak:
                kak = False
                elems[i] = elems[i].replace("≫", "")
                i -= 1
            if kak:
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
        self.root.geometry("800x400")
        self.root.minsize(width=800, height=400)
        self.root.configure(bg="white")

        self.main_font = tkFont.Font(self.root, family = "Yu Gothic", size = 16, weight="bold")
        self.sub_font = tkFont.Font(self.root, family = "Yu Gothic", size = 14, weight="bold")

        self.hide_frame = tk.Frame(self.root, width = 200, height = 80, relief=tk.FLAT, bg="white")
        self.hide_frame.propagate(False)
        self.main_frame = tk.Frame(self.root, width=600, height=130, relief=tk.SOLID, bd=2, bg="white")
        self.main_frame.propagate(False)

        self.line_canvs = tk.Canvas(self.main_frame, bg = "black", width=480, height=3)
        self.line_canvs2 = tk.Canvas(self.root, bg = "black", width=420, height=3)
       
        self.label = ttk.Label(self.main_frame, text="スペースキーでスタート", padding=[0, 14], background="white", anchor=tk.CENTER, font=self.main_font)
        self.label2 = ttk.Label(self.main_frame, padding=[0, 14], font=self.sub_font, background="white", anchor=tk.CENTER)
        self.label3 = ttk.Label(self.root, text="\n", font=self.sub_font, background="white", anchor=tk.CENTER)

        self.label.pack()
        self.line_canvs.pack()
        self.label2.pack()

        self.hide_frame.pack()
        self.main_frame.pack()

        self.label3.pack()
        self.line_canvs2.pack()
       
        self.root.bind("<KeyPress>", self.Key_down)
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

        #フレームサイズ
        set_width = self.width * 0.7
        set_height = self.width / 16 + 50
        if set_width < 600:
            set_width = 600
        elif set_width > 1400:
            set_width = 1400
        if set_height < 130:
            set_height = 130
        elif set_height > 180:
            set_height = 180

        self.line_canvs.config(width=set_width * 0.8)
        self.line_canvs2.config(width=set_width * 0.7)
        self.main_frame.config(height = set_height, width = set_width)
        self.hide_frame.config(height = self.height / 8)

        #フォントサイズ
        main_fontsize = int(self.width / 50)
        sub_fontsize = int(self.width / 57)
        if main_fontsize > 30:
            main_fontsize = 30
            sub_fontsize = 26
        self.main_font.configure(size=main_fontsize)
        self.sub_font.configure(size = sub_fontsize)
        return
    
    def Hira_to_Roma(self, st):
        words_pat = re.compile(r'ゃ|ゅ|ょ|ぁ|ぃ|ぅ|ぇ|ぉ')

        st = st.replace("ー","-").replace("☆", "").replace("(","").replace(")","").replace("「","") \
            .replace("」","").replace("、", ",").replace("・","").replace("…","...").replace("∽","") \
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
                    continue
            
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
                self.kasi_list.pop(0)
                self.line_ctn += 1
                loop = asyncio.get_event_loop()
                gather = asyncio.gather(
                    self.Show(0.5),
                    self.Clear_text()
                )
                loop.run_until_complete(gather)
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
            self.label["text"] = self.kasi_list[0][0]
            self.label2["text"] = self.kasi_list[0][1]
            self.now_str = self.kasi_list[0][2]
            self.ctn = 0
            dt = datetime.datetime.now()
            self.start_time = dt.hour * 60 * 60 + dt.minute * 60 + dt.second
        else:
            self.root.after(1000, self.count)
    
    async def Clear_text(self):
        self.label3['text'] = "\n"
        self.label2['text'] = ""
        self.label['text'] = ""
    
    async def Show(self, sleep_time = 0):
        if len(self.kasi_list) == 0:
            self.label["text"] = "終了"
            dt = datetime.datetime.now()
            now_time = dt.hour * 60 * 60 + dt.minute * 60 + dt.second
            heikin = int(self.typctn / (now_time - self.start_time - self.line_ctn * 0.5) * 10) / 10
            self.label2["text"] = "1秒あたり - " + str(heikin) + "文字"
            self.finish_flag = True
        else:
            await asyncio.sleep(sleep_time)
            self.label["text"] = self.kasi_list[0][0]
            self.label2["text"] = self.kasi_list[0][1]
            self.now_str = self.kasi_list[0][2]
            print(self.now_str)

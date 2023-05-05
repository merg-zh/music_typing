import customtkinter as ctk
import requests
from bs4 import BeautifulSoup as bsp4
import re
import regex
import jaconv
import datetime
import pygame

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
            "period":".", "quoteright":"'"
        }

        self.table = str.maketrans({
            v: '' for v in '\x0c\x0b\t\r'
        })

        self.start_status = 0
        self.finish_flag = False
        self.ctn = 3
        self.label = None
        self.label2 = None
        self.label3 = None
        self.root = None
        self.kasi_list = []
        self.now_str = None
        self.start_time = 0
        self.max_continue = 0

        self.line_ctn = 0

        self.width = 800
        self.height = 400

        self.now_color = "2f"
        self.anim_c = 0
        self.imx = 600

        pygame.mixer.init()
        self.true_se = pygame.mixer.Sound("data/se/typ.mp3")
        self.false_se = pygame.mixer.Sound("data/se/false.mp3")

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
            elif kan.search(elems[i]):
                kari[0] += elems[i]
                kari[1] += elems[i + 1]
                kari[2] += jaconv.kata2hira(elems[i + 1])
                i += 1
            elif self.p.fullmatch(elems[i]):
                kari[0] += elems[i]
                kari[1] += elems[i]
                kari[2] += elems[i]
            else:
                kari[0] += elems[i]
                kari[1] += elems[i]
                kari[2] += jaconv.kata2hira(elems[i])
            i += 1
        
        self.typ_ctn = 0
        self.miss_typ_ctn = 0
        
        ctk.set_appearance_mode("dark") 
        ctk.set_default_color_theme("blue")
        self.root = ctk.CTk()
        self.root.title(title)
        self.root.geometry("800x400")
        self.root.minsize(width=800, height=400)
        self.root.configure(fg_color="#202020")

        self.main_font = ctk.CTkFont(family = "Yu Gothic", size = 18, weight="bold")
        self.sub_font = ctk.CTkFont(family = "Yu Gothic", size = 16, weight="bold")

        self.hide_frame = ctk.CTkFrame(self.root, width=2000 ,height = 80, fg_color="transparent")
        self.hide_frame.propagate(False)
        self.main_frame = ctk.CTkFrame(self.root, corner_radius=50, width=600, height=130, border_width=4,border_color="#606060", fg_color="#2f2f2f")
        self.main_frame.propagate(False)
        self.sub_frame = ctk.CTkFrame(self.root, fg_color="transparent")

        self.progressbar = ctk.CTkProgressBar(self.hide_frame, width=400, height=15, border_width=2, \
                                               border_color="#404040", corner_radius=0, fg_color="#606060", \
                                               determinate_speed = int(50 / len(self.kasi_list) * 100) / 100)
        self.conb_label = ctk.CTkLabel(self.hide_frame, text="0x", font=("Yu Gothic", 25), text_color="white")
        self.progressbar.set(0)
        self.progressbar.place(relx=0, rely=0)
        self.conb_label.pack(anchor=ctk.E, padx=5)

        self.line_canvs = ctk.CTkCanvas(self.main_frame, bg = "#404040", highlightthickness=0, width=480, height=5)
        self.line_canvs2 = ctk.CTkCanvas(self.root, bg = "#404040", highlightthickness=0, width=420, height=5)
       
        self.label = ctk.CTkLabel(self.main_frame, text="スペースキーでスタート", anchor=ctk.CENTER, font=self.main_font, text_color="white")
        self.label2 = ctk.CTkLabel(self.main_frame, text="", font=self.sub_font, anchor=ctk.CENTER, text_color="white")
        self.label3 = ctk.CTkLabel(self.sub_frame, text="\n", font=self.sub_font, anchor=ctk.CENTER, text_color="white")
        self.label4 = ctk.CTkLabel(self.sub_frame, text="", font=self.sub_font, anchor=ctk.CENTER, text_color="#202020")

        self.label.place(relx=0.5, rely=0.3, anchor=ctk.CENTER)
        self.line_canvs.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)
        self.label2.place(relx=0.5, rely=0.7, anchor=ctk.CENTER)

        self.hide_frame.pack(padx=0, pady=0)
        self.main_frame.pack()

        self.label3.pack(side=ctk.LEFT, ipady=10)
        self.label4.pack(side=ctk.LEFT, ipady=10)
        self.sub_frame.pack()
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
        elif set_width > 1200:
            set_width = 1200
        if set_height < 130:
            set_height = 130
        elif set_height > 180:
            set_height = 180

        self.imx = set_width

        self.line_canvs.configure(width=set_width * 0.8)
        self.line_canvs2.configure(width=set_width * 0.7)
        self.main_frame.configure(height = set_height, width = set_width)
        self.hide_frame.configure(height = self.height / 8)

        #フォントサイズ
        main_fontsize = int(self.width / 44)
        sub_fontsize = int(self.width / 50)
        if main_fontsize > 34:
            main_fontsize = 34
            sub_fontsize = 30
        self.main_font.configure(size=main_fontsize)
        self.sub_font.configure(size = sub_fontsize)
        self.conb_label.configure(font = ("Yu Gothic", self.width / 32))

        #プログレスバーサイズ
        set_height = int(self.width / 53.3)
        set_bd_size = int(self.width / 270)
        if set_height > 25:
            set_height = 25
        if set_bd_size > 5:
            set_bd_size = 5
        self.progressbar.configure(width= int(self.width / 2), height = set_height, border_width = set_bd_size)

        
        return
    
    def Hira_to_Roma(self, st):
        words_pat = re.compile(r'ゃ|ゅ|ょ|ぁ|ぃ|ぅ|ぇ|ぉ')

        st = st.replace("ー","-").replace("☆", "").replace("(","").replace(")","").replace("「","") \
            .replace("」","").replace("、", ",").replace("・","").replace("…","...").replace("∽","") \
            .replace("。",".").replace("‥","..").replace("♪", "")
        
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
    
    def Ok(self):
        self.true_se.play()
        self.typ_ctn += 1
        self.label4.configure(text = self.now_str)
        self.conb_label.configure(text = str(int(self.conb_label.cget("text")[0:-1]) + 1) + "x")
        if self.now_str[0] == " ":
            self.label3.configure(text = self.label3.cget("text") + " ")
            self.now_str = self.now_str[1:]
    
    def Change_color(self):
        self.now_color = format((int(self.now_color, 16) - 3), 'x')
        if self.now_color != "2e":
            self.main_frame.configure(fg_color="#" + self.now_color + "2f2f")
            self.root.after(50, self.Change_color)
        else:
            self.now_color = "2f"
            self.main_frame.configure(fg_color="#" + self.now_color + "2f2f")

    def Key_down(self, e):
        key = e.keysym
        if key == "space" and self.start_status == 0:
            self.start_status = 1
            self.count()
            return
        
        if self.start_status < 2 or key == "Shift_L" or self.finish_flag:
            return
        
        try:
            key = self.key_sp[key]
        except:
            None
        
        if  self.now_str[0] == key:
            if len(self.now_str) == 1:
                self.true_se.play()
                self.kasi_list.pop(0)
                self.line_ctn += 1
                self.Clear_text()
                return
            self.label3.configure(text = self.label3.cget("text") + key)
            self.now_str = self.now_str[1:]
            self.Ok()
            return
        elif self.now_str[0:2] == "zy" and key == "j":
            self.label3.configure(text = self.label3.cget("text") + key)
            self.now_str = self.now_str[2:]
            self.Ok()
            return
        elif len(self.label3.cget("text")) > 2:
            if self.label3.cget("text")[-1] == "n" and self.label3.cget("text")[-2] != "n":
                self.label3.configure(text = self.label3.cget("text") + key)
                self.Ok()
                return
        
        self.label4.configure(text_color = "#a0a0a0")
        if self.max_continue < int(self.conb_label.cget("text")[0:-1]):
            self.max_continue = int(self.conb_label.cget("text")[0:-1])
        self.conb_label.configure(text = "0x")
        self.false_se.play()
        self.main_frame.configure(fg_color="#702f2f")
        if self.now_color == "2f":
            self.now_color = "70"
            self.Change_color()
        self.miss_typ_ctn += 1
        
    
    def count(self):
        self.label.configure(text = self.ctn)
        self.ctn -= 1
        if self.ctn == -1:
            self.start_status = 2
            self.Show()
            self.ctn = 0
            dt = datetime.datetime.now()
            self.start_time = dt.hour * 60 * 60 + dt.minute * 60 + dt.second
        else:
            self.root.after(1000, self.count)
    
    def Clear_text(self):
        if self.progressbar.get() == 0:
            self.progressbar.configure(progress_color = "#404040")
        self.progressbar.step()
        self.label4.configure(text = "", text_color = "#202020")
        self.label3.configure(text = "\n")
        self.label2.configure(text = "")
        self.label.configure(text = "")
        if len(self.kasi_list) == 0:
            self.Finish()
        else:
            self.root.after(500, self.Show)
    
    def Show(self):
        if len(self.kasi_list[0][0]) > 47:
            self.label.configure(text = self.kasi_list[0][0][:47] + "\n" + self.kasi_list[0][0][47:-1])
        else:
            self.label.configure(text = self.kasi_list[0][0])
        if len(self.kasi_list[0][1]) > 47:
            self.label2.configure(text = self.kasi_list[0][1][:47] + "\n" + self.kasi_list[0][1][47:-1])
        else:
            self.label2.configure(text = self.kasi_list[0][1])
        self.now_str = self.kasi_list[0][2]
        self.label4.configure(text = self.now_str)
        print("-------")
        print(self.kasi_list[0][1])
        print(self.now_str)
    
    def Finish(self):
        if self.anim_c == 0:
            self.finish_flag = True
            self.main_frame.configure(width = self.main_frame.cget("width") - self.imx / 150)
            self.sub_frame.configure(width = self.main_frame.cget("width") - self.imx / 150)
            self.line_canvs2.configure(width = self.main_frame.cget("width") - self.imx / 150)
            if self.main_frame.cget("width") == 0:
                self.anim_c = 1
                self.main_frame.destroy()
                self.sub_frame.destroy()
                self.line_canvs2.destroy()
            self.root.after(1, self.Finish)
        elif self.anim_c == 1:
            set_width = self.width * 0.7
            if set_width < 600:
                set_width = 600
            elif set_width > 1200:
                set_width = 1200
            self.main_frame = ctk.CTkFrame(self.root, corner_radius=50, width=set_width, height=0, border_width=6,border_color="#606060", fg_color="#2f2f2f")
            self.main_frame.pack()
            self.anim_c = 2
            self.root.after(1, self.Finish)
        elif self.anim_c == 2:
            new_line_canvas = ctk.CTkCanvas(self.main_frame, bg = "#2f2f2f", highlightthickness=0, width=self.main_frame.cget("width"), height=1)
            new_line_canvas.pack()
            new_label = ctk.CTkLabel(self.main_frame, text="タイプ数 - " + str(self.typ_ctn) + "　　ミスタイプ数 - " + str(self.miss_typ_ctn), anchor=ctk.CENTER, font=self.main_font, text_color="white")
            new_label.pack(pady = 20)
            self.anim_c = 3
            self.root.after(1000, self.Finish)
        elif self.anim_c == 3:
            self.line_canvs = ctk.CTkCanvas(self.main_frame, bg = "#404040", highlightthickness=0, width=int(self.main_frame.cget("width") * 0.7), height=5)
            self.line_canvs.pack()
            dt = datetime.datetime.now()
            now_time = dt.hour * 60 * 60 + dt.minute * 60 + dt.second
            heikin = int(self.typ_ctn / (now_time - self.start_time - self.line_ctn * 0.5) * 10) / 10
            new_label = ctk.CTkLabel(self.main_frame, text="1秒あたり - " + str(heikin) + "　　正誤率 - " + str(int(self.typ_ctn / self.miss_typ_ctn * 10) / 10) + "％", anchor=ctk.CENTER, font=self.main_font, text_color="white")
            new_label.pack(pady = 20)
            self.anim_c = 4
            self.root.after(1000, self.Finish)
        elif self.anim_c == 4:
            self.line_canvs2 = ctk.CTkCanvas(self.main_frame, bg = "#404040", highlightthickness=0, width=int(self.main_frame.cget("width") * 0.7), height=5)
            self.line_canvs2.pack()
            if self.max_continue == 0:
                self.max_continue = self.typ_ctn
            new_label = ctk.CTkLabel(self.main_frame, text="最大連続タイプ数 - " + str(self.max_continue) + "文字", anchor=ctk.CENTER, font=self.main_font, text_color="white")
            new_label.pack(pady = 20)
            self.anim_c = 5
        return

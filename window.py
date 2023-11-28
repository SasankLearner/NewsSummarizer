from tkinter import *
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
import nltk
from textblob import TextBlob
from newspaper import Article

from threading import Thread

nltk.download('punkt')

size = 20
size_s = 18
res_size = 15

frame_1_color = "#ffffff"
frame_2_color = "#222222"

url_label_color = "#555555"
url_textbox_color = "#222222"
submit_btn_color = "#222222"

copy_bg = "#222222"

result_box_color = "#cccccc"

class Window:
    def __init__(self, parent):
        self.frm1 = Frame(parent, bg=frame_1_color)
        self.frm2 = Frame(parent, bg=frame_2_color)

        self.url_label  = Label(self.frm1, bd=0, bg=url_label_color, font=("Helvetica", size), text="Enter URL:")
        self.url_box    = Text(self.frm1, bd=0, bg=url_textbox_color, font=("Comic Sans MS", size), wrap=WORD, highlightthickness=0, padx=5, pady=5)
        self.submit_btn = Button(self.frm1, bd=0, bg=submit_btn_color, command=self.send_url, fg="#ffffff", font=("Helvetica", size), text="Summarize", highlightthickness=0)

        self.title_label = Label(self.frm2, bd=0, bg=url_label_color, font=("Helvetica", size), text="Article Title            ")
        self.title_res   = Text(self.frm2, bd=0, bg=result_box_color, font=("Helvetica", res_size), wrap=WORD, state=DISABLED)
        self.title_copy = Button(self.frm2, bd=0, bg=copy_bg, font=("Helvetica", size_s), command=lambda: self.copy_to_clipboard(self.title_res), text="Copy", highlightthickness=0)

        self.sum_label = Label(self.frm2, bd=0, bg=url_label_color, font=("Helvetica", size), text="Article Summary            ")
        self.sum_res = Text(self.frm2, bd=0, bg=result_box_color, font=("Helvetica", res_size), wrap=WORD, state=DISABLED)
        self.sum_copy = Button(self.frm2, bd=0, bg=copy_bg, font=("Helvetica", size_s), command=lambda: self.copy_to_clipboard(self.sum_res), text="Copy", highlightthickness=0)

        self.place_frames()
        

    def send_url(self):
        th = Thread(target=self.send_url_thread)
        th.start()


    def send_url_thread(self):
        text = self.url_box.get("1.0", "end-1c")
        if not text: return

        try:
            article = Article(text)
            article.download()
            article.parse()
            article.nlp()
        except Exception:
            self.title_res["state"] = NORMAL
            self.title_res.insert(END, "Error Retrieving article title")
            self.title_res["state"] = DISABLED
            self.sum_res["state"] = NORMAL
            self.sum_res.insert(END, "Error Generating article summary")
            self.sum_res["state"] = DISABLED

        self.title_res["state"] = NORMAL
        self.title_res.delete("1.0", END)
        self.title_res["state"] = DISABLED
        self.sum_res["state"] = NORMAL
        self.sum_res.delete("1.0", END)
        self.sum_res["state"] = DISABLED

        self.title_res["state"] = NORMAL
        self.title_res.insert(END, article.title)
        self.title_res["state"] = DISABLED
        self.sum_res["state"] = NORMAL
        self.sum_res.insert(END, article.summary)
        self.sum_res["state"] = DISABLED    



    def copy_to_clipboard(self, widget: Text):
        widget.clipboard_append(widget.get("1.0", "end-1c"))


    def place_frames(self):
        self.frm1.place(x=0, y=0, relwidth=0.5, relheight=1)
        self.frm2.place(relx=0.5, y=0, relwidth=0.5, relheight=1)

        self.url_label.place(x=10, y=10, width=330, height=50)
        self.url_box.place(x=10, y=60, width=330, height=300)
        self.submit_btn.place(x=350/2-70, y=370, width=140, height=50)

        self.title_label.place(x=10, y=10, width=330, height=50)
        self.title_res.place(x=10, y=60, width=330, height=50)
        self.title_copy.place(x=260, y=size_s, width=70, height=30)

        self.sum_label.place(x=10, y=130, width=330, height=50)
        self.sum_res.place(x=10, y=180, width=330, height=510)
        self.sum_copy.place(x=260, y=140, width=70, height=30)
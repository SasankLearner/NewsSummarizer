from tkinter import *
from window import Window

def main():
    win = Tk()
    win.title("Article Summarizer")
    win.geometry("700x700")
    win.resizable(0, 0)

    main_window = Window(win)

    win.mainloop()



if __name__ == "__main__":
    main()
from tkinter import ttk
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib

LARGE_FONT = ("Verdana", 20)
NORMAL_FONT = ("Verdana", 12)
MAIN_COLOR = "#e6f8ff"
ACCENT_COLOR = "#ffeec2"
HEIGHT = 480
WIDTH = 800


class Transistortester(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.wm_title(self, "Transistortester")

        # self.attributes('-fullscreen', True)      #full-screen windows
        canvas = tk.Canvas(self, height=HEIGHT, width=WIDTH, bg=MAIN_COLOR)
        canvas.pack()

        self.frames = {}

        for F in (StartPage, LoadPage, HelpPage, InfoPage, Graph1Page, Graph2Page):
            frame = F(canvas, self)
            self.frames[F] = frame
            frame.place(relx=0.05, rely=0.05, relwidth=0.9, relheight=0.9)

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=MAIN_COLOR)
        label = ttk.Label(self, text="Start Page", font=LARGE_FONT, background=MAIN_COLOR)
        label.pack(pady=10, padx=10)

        style = ttk.Style()
        style.configure('Main.TButton', font=('Verdana', 12))

        bStart = ttk.Button(self, text="Start", command=lambda: controller.show_frame(LoadPage), style="Main.TButton")
        bStart.place(relx=0.4, rely=0.4, relwidth=0.2, relheight=0.1)

        bHelp = ttk.Button(self, text="Help", command=lambda: controller.show_frame(HelpPage), style="Main.TButton")
        bHelp.place(relx=0.4, rely=0.5, relwidth=0.2, relheight=0.1)


class LoadPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=MAIN_COLOR)

        style = ttk.Style()
        style.configure('Main.TButton', font=('Verdana', 12))

        bStop = ttk.Button(self, text="Stop tests", command=lambda: controller.show_frame(StartPage), style="Main.TButton")
        bStop.place(relx=0.4, rely=0.6, relwidth=0.2, relheight=0.1)

        bNext = ttk.Button(self, text="Next", command=lambda: controller.show_frame(InfoPage))
        bNext.place(relx=0.75, rely=0.85, relwidth=0.2, relheight=0.1)

        label = ttk.Label(self, text="Please wait\nPerforming tests", font=LARGE_FONT, anchor="center", background=MAIN_COLOR, justify=tk.CENTER)
        label.place(relx=0.3, rely=0.3, relwidth=0.4, relheight=0.2)


class HelpPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=MAIN_COLOR)

        style = ttk.Style()
        style.configure('bBack.TButton', font=('Verdana', 10))

        bBack = ttk.Button(self, text="Back to Start", command=lambda: controller.show_frame(StartPage), style="bBack.TButton")
        bBack.place(relx=0, rely=0, relwidth=0.15, relheight=0.1)

        label = ttk.Label(self, text="Tekst met uitleg over test", font=NORMAL_FONT, anchor="center", background=MAIN_COLOR, justify=tk.CENTER)
        label.place(relx=0.3, rely=0.4, relwidth=0.4, relheight=0.2)


class InfoPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=MAIN_COLOR)

        style = ttk.Style()
        style.configure('bBack.TButton', font=('Verdana', 10))
        style.configure('bGraph.TButton', font=('Verdana', 11))

        bBack = ttk.Button(self, text="Back to Start", command=lambda: controller.show_frame(StartPage), style="bBack.TButton")
        bBack.place(relx=0, rely=0, relwidth=0.15, relheight=0.1)

        bGraph1 = ttk.Button(self, text="Current Gain", command=lambda: controller.show_frame(Graph1Page), style="bGraph.TButton")
        bGraph1.place(relx=0.35, rely=0.6, relwidth=0.3, relheight=0.1)

        bGraph2 = ttk.Button(self, text="Collector Saturation Region", command=lambda: controller.show_frame(Graph2Page), style="bGraph.TButton")
        bGraph2.place(relx=0.35, rely=0.7, relwidth=0.3, relheight=0.1)

        frame = tk.Frame(self, bg=ACCENT_COLOR)
        frame.place(relx=0.25, rely=0.15, relwidth=0.5, relheight=0.4)

        # Type transistor
        label = ttk.Label(self, text="Type trasistor:", font=NORMAL_FONT, background=ACCENT_COLOR)
        label.place(relx=0.3, rely=0.2, relwidth=0.2, relheight=0.1)

        label = ttk.Label(self, text="BJT", font=NORMAL_FONT, anchor="center", background="white")
        label.place(relx=0.55, rely=0.21, relwidth=0.15, relheight=0.08)

        # Pin Layout
        label = ttk.Label(self, text="Pin Layout:", font=NORMAL_FONT, background=ACCENT_COLOR)
        label.place(relx=0.3, rely=0.3, relwidth=0.2, relheight=0.1)

        label = ttk.Label(self, text="C", font=NORMAL_FONT, anchor="center", background="white")
        label.place(relx=0.55, rely=0.31, relwidth=0.04, relheight=0.08)

        label = ttk.Label(self, text="B", font=NORMAL_FONT, anchor="center", background="white")
        label.place(relx=0.605, rely=0.31, relwidth=0.04, relheight=0.08)

        label = ttk.Label(self, text="E", font=NORMAL_FONT, anchor="center", background="white")
        label.place(relx=0.66, rely=0.31, relwidth=0.04, relheight=0.08)

        # V_BE
        label = ttk.Label(self, text="V_BE:", font=NORMAL_FONT, background=ACCENT_COLOR)
        label.place(relx=0.3, rely=0.4, relwidth=0.2, relheight=0.1)

        label = ttk.Label(self, text="0.635 V", font=NORMAL_FONT, anchor="center", background="white")
        label.place(relx=0.55, rely=0.41, relwidth=0.15, relheight=0.08)


class Graph1Page(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Graph Page", font=LARGE_FONT, anchor="center", background=MAIN_COLOR)
        label.place(relx=0, rely=0, relwidth=1, relheight=0.1)

        style = ttk.Style()
        style.configure('bBack.TButton', font=('Verdana', 10))

        bBack = ttk.Button(self, text="Back to Info", command=lambda: controller.show_frame(InfoPage), style="bBack.TButton")
        bBack.place(relx=0, rely=0, relwidth=0.15, relheight=0.1)

        fig = Figure(figsize=(10, 10), dpi=100, facecolor=MAIN_COLOR)
        fig.add_subplot(111).plot([1, 2, 3, 4, 5, 6, 7, 8], [2, 8, 4, 6, 7, 2, 1, 3])

        canvas = FigureCanvasTkAgg(fig, self)
        canvas.draw()

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.configure(bg=ACCENT_COLOR)
        toolbar.update()
        # canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand = True)
        canvas.get_tk_widget().place(relx=0, rely=0.1, relwidth=1, relheight=0.85)


class Graph2Page(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Graph Page", font=LARGE_FONT, anchor="center", background=MAIN_COLOR)
        label.place(relx=0, rely=0, relwidth=1, relheight=0.1)

        style = ttk.Style()
        style.configure('bBack.TButton', font=('Verdana', 10))

        bBack = ttk.Button(self, text="Back to Info", command=lambda: controller.show_frame(InfoPage), style="bBack.TButton")
        bBack.place(relx=0, rely=0, relwidth=0.15, relheight=0.1)

        fig = Figure(figsize=(10, 10), dpi=100, facecolor=MAIN_COLOR)
        fig.add_subplot(111).plot([1, 2, 3, 4, 5, 6, 7, 8], [7, 3, 6, 1, 8, 3, 4, 2])

        canvas = FigureCanvasTkAgg(fig, self)
        canvas.draw()

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        toolbar.configure(bg=ACCENT_COLOR)
        # canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand = True)
        canvas.get_tk_widget().place(relx=0, rely=0.1, relwidth=1, relheight=0.85)


app = Transistortester()
app.mainloop()


"""
root = tk.Tk()

canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
canvas.pack()

frame = tk.Frame(root, bg="#80c1ff")
frame.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.8)

start = tk.Button(frame, text="Start")
start.place(relx=0.7, rely=0.8, relwidth=0.2, relheight=0.1)

root.mainloop()
"""

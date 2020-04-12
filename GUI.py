from tkinter import ttk
import tkinter as tk

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib import style
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib

import random
import threading
import csv

import save

style.use("ggplot")

LARGE_FONT = ("Verdana", 20)
NORMAL_FONT = ("Verdana", 12)
MAIN_COLOR = "#e6f8ff"
ACCENT_COLOR = "#ffeec2"
HEIGHT = 480
WIDTH = 800


def rand(start, end, num):
    res = []

    for j in range(num):
        res.append(random.randint(start, end))

    return res


# In deze functie moet een onderscheid gemaakt worden tussen BJT en MOSFET
def load(controller):
    temp = ["C", "B", "E"]
    thread = threading.Thread(target=app.getInfo)     # Hier moet een functie komen die de gemeten waarden doorgeeft
    thread.start()

    # Type transistor
    app.transType.set("MOSFET")

    # Pinlayout
    choice = random.choice(temp)
    app.pin1.set(choice)
    temp.remove(choice)
    choice = random.choice(temp)
    app.pin2.set(choice)
    temp.remove(choice)
    app.pin3.set(temp[0])

    app.updatePlot(app.plot1, [1, 2, 3, 4, 5, 6, 7, 8, 9], app.hfe, "IC", "hfe")
    app.updatePlot(app.plot2, [1, 2, 3, 4, 5, 6, 7, 8, 9], app.V_CE, "IC", "hfe")

    thread.join()
    print("Pressed start\t", app.hfe, app.V_CE)
    controller.show_frame(InfoPageBJT)


class Transistortester(tk.Tk):
    # Labels
    pin1 = 0
    pin2 = 0
    pin3 = 0
    transType = 0

    # Graph 1
    hfe = 9*[2]
    fig1 = Figure(figsize=(10, 8), dpi=100, facecolor=MAIN_COLOR)
    plot1 = fig1.add_subplot(111)

    # Graph 2
    V_CE = 9*[2]
    fig2 = Figure(figsize=(10, 8), dpi=100, facecolor=MAIN_COLOR)
    plot2 = fig2.add_subplot(111)

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.wm_title(self, "Transistortester")

        Transistortester.pin1 = tk.StringVar()
        Transistortester.pin1.set("C")
        Transistortester.pin2 = tk.StringVar()
        Transistortester.pin2.set("B")
        Transistortester.pin3 = tk.StringVar()
        Transistortester.pin3.set("E")
        Transistortester.transType = tk.StringVar()
        Transistortester.transType.set("BJT")

        # self.attributes('-fullscreen', True)      #full-screen windows
        self.canvas = tk.Canvas(self, height=HEIGHT, width=WIDTH, bg=MAIN_COLOR)
        self.canvas.pack()

        self.frames = {}

        for F in (StartPage, HelpPage, InfoPageBJT, Graph1Page, Graph2Page):
            frame = F(self.canvas, self)
            self.frames[F] = frame
            frame.place(relx=0.05, rely=0.05, relwidth=0.9, relheight=0.9)

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def updatePlot(self, plot, x, y, xlabel, ylabel):
        plot.clear()
        plot.plot(x, y)
        plot.set_xlabel(xlabel)
        plot.set_ylabel(ylabel)

        # Update alle grafieken
        Graph1Page.updateGraph()
        Graph2Page.updateGraph()

    def getInfo(self):
        Transistortester.V_CE = rand(1, 10, 9)
        Transistortester.hfe = rand(1, 10, 9)


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=MAIN_COLOR)
        label = ttk.Label(self, text="Start Page", font=LARGE_FONT, background=MAIN_COLOR)
        label.pack(pady=10, padx=10)

        style = ttk.Style()
        style.configure('Main.TButton', font=('Verdana', 12))

        bStart = ttk.Button(self, text="Start", command=lambda: load(controller), style="Main.TButton")
        bStart.place(relx=0.4, rely=0.4, relwidth=0.2, relheight=0.1)

        bHelp = ttk.Button(self, text="Help", command=lambda: controller.show_frame(HelpPage), style="Main.TButton")
        bHelp.place(relx=0.4, rely=0.5, relwidth=0.2, relheight=0.1)


class HelpPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=MAIN_COLOR)

        style = ttk.Style()
        style.configure('bBack.TButton', font=('Verdana', 10))

        bBack = ttk.Button(self, text="Back to Start", command=lambda: controller.show_frame(StartPage), style="bBack.TButton")
        bBack.place(relx=0, rely=0, relwidth=0.15, relheight=0.1)

        label = ttk.Label(self, text="Tekst met uitleg over test", font=NORMAL_FONT, anchor="center", background=MAIN_COLOR, justify=tk.CENTER)
        label.place(relx=0.3, rely=0.4, relwidth=0.4, relheight=0.2)


# class LoadPage(tk.Frame):

#     def __init__(self, parent, controller):
#         tk.Frame.__init__(self, parent, bg=MAIN_COLOR)

#         style = ttk.Style()
#         style.configure('Main.TButton', font=('Verdana', 12))

#         bStop = ttk.Button(self, text="Stop tests", command=lambda: controller.show_frame(StartPage), style="Main.TButton")
#         bStop.place(relx=0.4, rely=0.6, relwidth=0.2, relheight=0.1)

#         bNext = ttk.Button(self, text="Next", command=lambda: controller.show_frame(InfoPage))
#         bNext.place(relx=0.75, rely=0.85, relwidth=0.2, relheight=0.1)

#         label = ttk.Label(self, text="Please wait\nPerforming tests", font=LARGE_FONT, anchor="center", background=MAIN_COLOR, justify=tk.CENTER)
#         label.place(relx=0.3, rely=0.3, relwidth=0.4, relheight=0.2)

#         hfe = rand(1, 10, 8)
#         V_CE = rand(1, 10, 8)


class InfoPageBJT(tk.Frame):

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

        label = ttk.Label(self, textvariable=Transistortester.transType, font=NORMAL_FONT, anchor="center", background="white")
        label.place(relx=0.55, rely=0.21, relwidth=0.15, relheight=0.08)

        # Pin Layout
        label = ttk.Label(self, text="Pin Layout:", font=NORMAL_FONT, background=ACCENT_COLOR)
        label.place(relx=0.3, rely=0.3, relwidth=0.2, relheight=0.1)

        label = ttk.Label(self, textvariable=Transistortester.pin1, font=NORMAL_FONT, anchor="center", background="white")
        label.place(relx=0.55, rely=0.31, relwidth=0.04, relheight=0.08)

        label = ttk.Label(self, textvariable=Transistortester.pin2, font=NORMAL_FONT, anchor="center", background="white")
        label.place(relx=0.605, rely=0.31, relwidth=0.04, relheight=0.08)

        label = ttk.Label(self, textvariable=Transistortester.pin3, font=NORMAL_FONT, anchor="center", background="white")
        label.place(relx=0.66, rely=0.31, relwidth=0.04, relheight=0.08)

        # V_BE
        label = ttk.Label(self, text="V_BE:", font=NORMAL_FONT, background=ACCENT_COLOR)
        label.place(relx=0.3, rely=0.4, relwidth=0.2, relheight=0.1)

        label = ttk.Label(self, text="0.635 V", font=NORMAL_FONT, anchor="center", background="white")
        label.place(relx=0.55, rely=0.41, relwidth=0.15, relheight=0.08)


# Current gain (bèta/hfe in functie van hfe)
class Graph1Page(tk.Frame):
    canvas = 0

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        style = ttk.Style()
        style.configure('bBack.TButton', font=('Verdana', 10))

        Graph1Page.canvas = FigureCanvasTkAgg(Transistortester.fig1, self)
        Graph1Page.canvas.draw()

        toolbar = NavigationToolbar2Tk(Graph1Page.canvas, self)
        toolbar.configure(bg=ACCENT_COLOR)
        toolbar._message_label.config(background=ACCENT_COLOR)
        toolbar.update()

        Graph1Page.canvas.get_tk_widget().pack()

        label = ttk.Label(self, text="Current gain", font=LARGE_FONT, anchor="center", background=MAIN_COLOR)
        label.place(relx=0, rely=0, relwidth=1, relheight=0.1)

        bBack = ttk.Button(self, text="Back to Info", command=lambda: controller.show_frame(InfoPageBJT), style="bBack.TButton")
        bBack.place(relx=0, rely=0, relwidth=0.15, relheight=0.1)

        bCSV = ttk.Button(self, text="Save CSV", command=lambda: save.saveCSV([1, 2, 3, 4, 5, 6, 7, 8, 9], Transistortester.hfe, "I_C", "hfe"), style="bBack.TButton")
        bCSV.place(relx=0.85, rely=0, relwidth=0.15, relheight=0.1)

    def updateGraph():
        Graph1Page.canvas.draw()


# Collector saturatie regio (I_C in functie van V_CE)
class Graph2Page(tk.Frame):
    canvas = 0

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        style = ttk.Style()
        style.configure('bBack.TButton', font=('Verdana', 10))

        Graph2Page.canvas = FigureCanvasTkAgg(Transistortester.fig2, self)
        Graph2Page.canvas.draw()

        toolbar = NavigationToolbar2Tk(Graph2Page.canvas, self)
        toolbar.configure(bg=ACCENT_COLOR)
        toolbar._message_label.config(background=ACCENT_COLOR)
        toolbar.update()

        Graph2Page.canvas.get_tk_widget().pack()

        label = ttk.Label(self, text="Collector saturatie regio", font=LARGE_FONT, anchor="center", background=MAIN_COLOR)
        label.place(relx=0, rely=0, relwidth=1, relheight=0.1)

        bBack = ttk.Button(self, text="Back to Info", command=lambda: controller.show_frame(InfoPageBJT), style="bBack.TButton")
        bBack.place(relx=0, rely=0, relwidth=0.15, relheight=0.1)

        bCSV = ttk.Button(self, text="Save CSV", command=lambda: save.saveCSV([1, 2, 3, 4, 5, 6, 7, 8, 9], Transistortester.V_CE, "I_C", "V_CE"), style="bBack.TButton")
        bCSV.place(relx=0.85, rely=0, relwidth=0.15, relheight=0.1)

    def updateGraph():
        Graph2Page.canvas.draw()


app = Transistortester()
app.mainloop()

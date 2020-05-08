from tkinter import ttk
import tkinter as tk
from PIL import ImageTk, Image

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib import style
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib

import random
import threading
import csv
import os

import saveCSV

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
    layout = ["C", "B", "E"]
    transistorTypes = ["BJT NPN", "BJT PNP", "MOSFET n-channel enhancement", "MOSFET p-channel enhancement", "MOSFET n-channel depletion", "MOSFET p-channel depletion"]
    thread = threading.Thread(target=app.getInfo)     # Hier moet een functie komen die de gemeten waarden doorgeeft
    thread.start()

    # Pinlayout
    choice = random.choice(layout)
    app.pin1.set(choice)
    layout.remove(choice)
    choice = random.choice(layout)
    app.pin2.set(choice)
    layout.remove(choice)
    app.pin3.set(layout[0])

    app.updatePlot(app.plot1, [1, 2, 3, 4, 5, 6, 7, 8, 9], app.hfe, "IC", "hfe")
    app.updatePlot(app.plot2, [1, 2, 3, 4, 5, 6, 7, 8, 9], app.V_CE, "IC", "hfe")

    thread.join()
    print("Pressed start\t", app.hfe, app.V_CE)
    kapot = random.randrange(0, 10)
    transistorType = random.choice(transistorTypes)

    if (kapot < 9):
        if (transistorType == "BJT NPN" or transistorType == "BJT PNP"):
            print("BJT")
            controller.show_frame(InfoPageBJT)
        else:
            controller.show_frame(InfoPageMOSFET)
        app.transType.set(transistorType)
    else:
        controller.show_frame(BrokePage)


class Transistortester(tk.Tk):
    # Labels
    pin1 = 0
    pin2 = 0
    pin3 = 0
    transType = 0

    """------------------------------    BJT     ------------------------------"""
    V_BE = 0

    # Graph 1
    hfe = 9*[2]
    fig1 = Figure(figsize=(10, 8), dpi=100, facecolor=MAIN_COLOR)
    plot1 = fig1.add_subplot(111)

    # Graph 2
    V_CE = 9*[2]
    fig2 = Figure(figsize=(10, 8), dpi=100, facecolor=MAIN_COLOR)
    plot2 = fig2.add_subplot(111)

    """----------------------------     MOSFET     ----------------------------"""
    # Graph 1
    # hfe = 9*[2]
    # fig1 = Figure(figsize=(10, 8), dpi=100, facecolor=MAIN_COLOR)
    # plot1 = fig1.add_subplot(111)

    # Graph 2
    # V_CE = 9*[2]
    # fig2 = Figure(figsize=(10, 8), dpi=100, facecolor=MAIN_COLOR)
    # plot2 = fig2.add_subplot(111)

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.wm_title(self, "Transistortester")

        # Zetten van initiële waarden
        Transistortester.pin1 = tk.StringVar()
        Transistortester.pin1.set("C")
        Transistortester.pin2 = tk.StringVar()
        Transistortester.pin2.set("B")
        Transistortester.pin3 = tk.StringVar()
        Transistortester.pin3.set("E")
        Transistortester.transType = tk.StringVar()
        Transistortester.transType.set("BJT NPN")
        Transistortester.V_BE = tk.StringVar()
        Transistortester.V_BE.set(str(0.635) + "V")

        # self.attributes('-fullscreen', True)      #full-screen windows
        self.canvas = tk.Canvas(self, height=HEIGHT, width=WIDTH, bg=MAIN_COLOR)
        self.canvas.pack()

        self.frames = {}

        for F in (StartPage, HelpPage, BrokePage, InfoPageBJT, InfoPageMOSFET, Graph1PageBJT, Graph2PageBJT):
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
        Graph1PageBJT.updateGraph()
        Graph2PageBJT.updateGraph()

    def getInfo(self):
        Transistortester.V_CE = rand(1, 10, 9)  # Functie met gemeten waarden
        Transistortester.hfe = rand(1, 10, 9)   # Functie met gemeten waarden


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=MAIN_COLOR)
        label = ttk.Label(self, text="Startpagina", font=LARGE_FONT, background=MAIN_COLOR)
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

        bBack = ttk.Button(self, text="Naar Start", command=lambda: controller.show_frame(StartPage), style="bBack.TButton")
        bBack.place(relx=0, rely=0, relwidth=0.15, relheight=0.1)

        label = ttk.Label(self, text="Uitleg over test", font=LARGE_FONT, background=MAIN_COLOR)
        label.pack(pady=10, padx=10)

        label = ttk.Label(self, text="● Plug de component in het breadboard. \n● Verbind de draden van de transistortester met het breadboard. \n● Ga naar de startpagina en druk op start.",
                          font=NORMAL_FONT, anchor="center", background=MAIN_COLOR, justify=tk.LEFT)
        label.place(relx=0.1, rely=0.2, relwidth=0.8, relheight=0.2)

        path = os.getcwd() + "/TransistorBreadboard.png"

        img = Image.open(path)
        img = img.resize((int(0.5*HEIGHT - 0.05*HEIGHT), int(0.5*HEIGHT - 0.05*HEIGHT)), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)
        panel = ttk.Label(self, image=img)
        panel.image = img
        panel.place(relx=0.35, rely=0.4, relwidth=0.3, relheight=0.5)


class BrokePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=MAIN_COLOR)
        label = ttk.Label(self, text="Kapot", font=LARGE_FONT, background=MAIN_COLOR)
        label.pack(pady=10, padx=10)

        style = ttk.Style()
        style.configure('Main.TButton', font=('Verdana', 12))

        bBack = ttk.Button(self, text="Naar Start", command=lambda: controller.show_frame(StartPage), style="bBack.TButton")
        bBack.place(relx=0, rely=0, relwidth=0.15, relheight=0.1)

        label = ttk.Label(self, text="Het ziet ernaar uit dat de component kapot is.\nCheck voor de zekerheid of de component goed is aangesloten.",
                          font=NORMAL_FONT, anchor="center", background=MAIN_COLOR, justify=tk.CENTER)
        label.place(relx=0.1, rely=0.2, relwidth=0.8, relheight=0.2)


class InfoPageBJT(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=MAIN_COLOR)

        style = ttk.Style()
        style.configure('bBack.TButton', font=('Verdana', 10))
        style.configure('bGraph.TButton', font=('Verdana', 11))

        bBack = ttk.Button(self, text="Naar Start", command=lambda: controller.show_frame(StartPage), style="bBack.TButton")
        bBack.place(relx=0, rely=0, relwidth=0.15, relheight=0.1)

        bGraph1 = ttk.Button(self, text="Current Gain", command=lambda: controller.show_frame(Graph1PageBJT), style="bGraph.TButton")
        bGraph1.place(relx=0.35, rely=0.6, relwidth=0.3, relheight=0.1)

        bGraph2 = ttk.Button(self, text="Collector Saturation Region", command=lambda: controller.show_frame(Graph2PageBJT), style="bGraph.TButton")
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

        label = ttk.Label(self, textvariable=Transistortester.V_BE, font=NORMAL_FONT, anchor="center", background="white")
        label.place(relx=0.55, rely=0.41, relwidth=0.15, relheight=0.08)


class InfoPageMOSFET(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=MAIN_COLOR)

        style = ttk.Style()
        style.configure('bBack.TButton', font=('Verdana', 10))
        style.configure('bGraph.TButton', font=('Verdana', 11))

        bBack = ttk.Button(self, text="Naar Start", command=lambda: controller.show_frame(StartPage), style="bBack.TButton")
        bBack.place(relx=0, rely=0, relwidth=0.15, relheight=0.1)

        bGraph1 = ttk.Button(self, text="Current Gain", command=lambda: controller.show_frame(Graph1PageBJT), style="bGraph.TButton")
        bGraph1.place(relx=0.35, rely=0.6, relwidth=0.3, relheight=0.1)

        bGraph2 = ttk.Button(self, text="Collector Saturation Region", command=lambda: controller.show_frame(Graph2PageBJT), style="bGraph.TButton")
        bGraph2.place(relx=0.35, rely=0.7, relwidth=0.3, relheight=0.1)

        frame = tk.Frame(self, bg=ACCENT_COLOR)
        frame.place(relx=0.1, rely=0.15, relwidth=0.8, relheight=0.4)

        # Type transistor
        label = ttk.Label(self, text="Type trasistor:", font=NORMAL_FONT, background=ACCENT_COLOR)
        label.place(relx=0.15, rely=0.2, relwidth=0.2, relheight=0.1)

        label = ttk.Label(self, textvariable=Transistortester.transType, font=NORMAL_FONT, anchor="center", background="white")
        label.place(relx=0.4, rely=0.21, relwidth=0.45, relheight=0.08)

        # Pin Layout
        label = ttk.Label(self, text="Pin Layout:", font=NORMAL_FONT, background=ACCENT_COLOR)
        label.place(relx=0.15, rely=0.3, relwidth=0.2, relheight=0.1)

        label = ttk.Label(self, textvariable=Transistortester.pin1, font=NORMAL_FONT, anchor="center", background="white")
        label.place(relx=0.4, rely=0.31, relwidth=0.09, relheight=0.08)

        label = ttk.Label(self, textvariable=Transistortester.pin2, font=NORMAL_FONT, anchor="center", background="white")
        label.place(relx=0.58, rely=0.31, relwidth=0.09, relheight=0.08)

        label = ttk.Label(self, textvariable=Transistortester.pin3, font=NORMAL_FONT, anchor="center", background="white")
        label.place(relx=0.76, rely=0.31, relwidth=0.09, relheight=0.08)

        # V_BE
        label = ttk.Label(self, text="V_BE:", font=NORMAL_FONT, background=ACCENT_COLOR)
        label.place(relx=0.15, rely=0.4, relwidth=0.2, relheight=0.1)

        label = ttk.Label(self, text="0.635 V", font=NORMAL_FONT, anchor="center", background="white")
        label.place(relx=0.4, rely=0.41, relwidth=0.45, relheight=0.08)


# Current gain (bèta/hfe in functie van I_C)
class Graph1PageBJT(tk.Frame):
    canvas = 0

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        style = ttk.Style()
        style.configure('bBack.TButton', font=('Verdana', 10))

        Graph1PageBJT.canvas = FigureCanvasTkAgg(Transistortester.fig1, self)
        Graph1PageBJT.canvas.draw()

        toolbar = NavigationToolbar2Tk(Graph1PageBJT.canvas, self)
        toolbar.configure(bg=ACCENT_COLOR)
        toolbar._message_label.config(background=ACCENT_COLOR)
        toolbar.update()

        Graph1PageBJT.canvas.get_tk_widget().pack()

        label = ttk.Label(self, text="Current gain", font=LARGE_FONT, anchor="center", background=MAIN_COLOR)
        label.place(relx=0, rely=0, relwidth=1, relheight=0.1)

        bBack = ttk.Button(self, text="Terug", command=lambda: controller.show_frame(InfoPageBJT), style="bBack.TButton")
        bBack.place(relx=0, rely=0, relwidth=0.15, relheight=0.1)

        bCSV = ttk.Button(self, text="Save CSV", command=lambda: saveCSV.saveCSV([1, 2, 3, 4, 5, 6, 7, 8, 9],
                                                                                 Transistortester.hfe, "I_C", "hfe", "CurrentGain.csv"), style="bBack.TButton")
        bCSV.place(relx=0.85, rely=0, relwidth=0.15, relheight=0.1)

    def updateGraph():
        Graph1PageBJT.canvas.draw()


# Collector saturatie regio (I_C in functie van V_CE)
class Graph2PageBJT(tk.Frame):
    canvas = 0

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        style = ttk.Style()
        style.configure('bBack.TButton', font=('Verdana', 10))

        Graph2PageBJT.canvas = FigureCanvasTkAgg(Transistortester.fig2, self)
        Graph2PageBJT.canvas.draw()

        toolbar = NavigationToolbar2Tk(Graph2PageBJT.canvas, self)
        toolbar.configure(bg=ACCENT_COLOR)
        toolbar._message_label.config(background=ACCENT_COLOR)
        toolbar.update()

        Graph2PageBJT.canvas.get_tk_widget().pack()

        label = ttk.Label(self, text="Collector saturation region", font=LARGE_FONT, anchor="center", background=MAIN_COLOR)
        label.place(relx=0, rely=0, relwidth=1, relheight=0.1)

        bBack = ttk.Button(self, text="Terug", command=lambda: controller.show_frame(InfoPageBJT), style="bBack.TButton")
        bBack.place(relx=0, rely=0, relwidth=0.15, relheight=0.1)

        bCSV = ttk.Button(self, text="Save CSV", command=lambda: saveCSV.saveCSV([1, 2, 3, 4, 5, 6, 7, 8, 9],
                                                                                 Transistortester.V_CE, "I_C", "V_CE", "CollectorSaturationRegion.csv"), style="bBack.TButton")
        bCSV.place(relx=0.85, rely=0, relwidth=0.15, relheight=0.1)

    def updateGraph():
        Graph2PageBJT.canvas.draw()


app = Transistortester()
app.mainloop()

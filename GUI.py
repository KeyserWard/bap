# Imports voor het maken van het venster
from tkinter import ttk
import tkinter as tk
from PIL import ImageTk, Image

# Imports voor het maken van grafieken
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib import style
import matplotlib.pyplot as plt

import numpy as np
import os
import csv
from cffi import FFI

# Import van ander document
import saveCSV
import Transistor

style.use("ggplot")

LARGE_FONT = ("Verdana", 20)
NORMAL_FONT = ("Verdana", 12)
MAIN_COLOR = "#e6f8ff"
ACCENT_COLOR = "#ffeec2"
HEIGHT = 480
WIDTH = 800
X = np.zeros(10)
Y = np.zeros(10)


def load(controller):
    global X, Y
    # Pinlayout
    layout = Transistor.getPinLayout()

    if(None in layout):
        controller.show_frame(DefectPage)

    else:
        # Bepalen transistortype
        transType = Transistor.getType()
        transStructuur = Transistor.getStructuur()

        app.pin1.set(layout[0])
        app.pin2.set(layout[1])
        app.pin3.set(layout[2])
        app.transType.set(transStructuur + " " + transType)

        dataLen = 20
        
        if(transStructuur == "BJT"):
            # Graph1: Beta in functie van I_C
            app.I_C1.resize(dataLen)
            app.Beta.resize(dataLen)

            Transistor.meting_Beta_IC(app.I_C1, app.Beta, dataLen)

            # Graph2: V_CE in functie van I_C
            IB = 50e-3  # in mA
            app.I_C2.resize(dataLen)
            app.V_CE.resize(dataLen)

            Transistor.meting_IC_VCE(IB, app.I_C2, app.V_CE, dataLen)

            # Graph3: V_CE in functie van I_C
            VCB = 0.7  # in V
            app.I_C3.resize(dataLen)
            app.V_BE.resize(dataLen)

            Transistor.meting_IC_VBE(VCB, app.I_C3, app.V_BE, dataLen)

            # Updaten plots
            app.update_plot(Graph1PageBJT, app.I_C1, app.Beta, "IC", "Beta")
            app.update_plot(Graph2PageBJT, app.I_C2, app.V_CE, "IC", "VCE")
            app.update_plot(Graph3PageBJT, app.I_C3, app.V_BE, "IC", "VCE")

            print(app.I_C1)
            print(app.I_C2)
            print(app.I_C3)

            controller.show_frame(InfoPageBJT)

        elif(transStructuur == "MOSFET"):
            controller.show_frame(InfoPageMOSFET)

        else:
            controller.show_frame(DefectPage)


class Transistortester(tk.Tk):
    # Labels
    pin1 = 0
    pin2 = 0
    pin3 = 0
    transType = 0

    """------------------------------    BJT     ------------------------------"""

    # Graph 1
    nameBJTGraph1 = "Beta in functie van IC"
    Beta = np.zeros(9)
    I_C1 = np.zeros(9)

    # Graph 2
    nameBJTGraph2 = "IC in functie van VCE"
    V_CE = np.zeros(9)
    I_C2 = np.zeros(9)

    # Graph 3
    nameBJTGraph3 = "IC in functie van VBE"
    V_BE = np.zeros(9)
    I_C3 = np.zeros(9)

    """----------------------------     MOSFET     ----------------------------"""
    # Graph 1
    # Beta = 9*[2]
    # MOSFETfig1 = Figure(figsize=(10, 8), dpi=100, facecolor=MAIN_COLOR)
    # MOSFETplot1 = MOSFETfig1.add_subplot(111)

    # Graph 2
    # V_CE = 9*[2]
    # MOSFETfig2 = Figure(figsize=(10, 8), dpi=100, facecolor=MAIN_COLOR)
    # MOSFETplot2 = MOSFETfig2.add_subplot(111)

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

        # self.attributes('-fullscreen', True)      #full-screen windows
        self.canvas = tk.Canvas(self, height=HEIGHT, width=WIDTH, bg=MAIN_COLOR)
        self.canvas.pack()

        self.frames = {}

        for F in (StartPage, HelpPage, DefectPage, InfoPageBJT, InfoPageMOSFET, Graph1PageBJT, Graph2PageBJT, Graph3PageBJT):
            frame = F(self.canvas, self)
            self.frames[F] = frame
            frame.place(relx=0.05, rely=0.05, relwidth=0.9, relheight=0.9)

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def update_plot(self, graph, x, y, xlabel, ylabel):
        self.frames[graph].plot.clear()
        self.frames[graph].plot.plot(x, y)
        self.frames[graph].plot.set_xlabel(xlabel)
        self.frames[graph].plot.set_ylabel(ylabel)
        
        self.frames[graph].update_graph()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=MAIN_COLOR)
        label = ttk.Label(self, text="Startpagina", font=LARGE_FONT, background=MAIN_COLOR)
        label.pack(pady=10, padx=10)

        style = ttk.Style()
        style.configure('Main.TButton', font=('Verdana', 12))

        bStart = ttk.Button(self, text="Start", command=lambda: load(controller), style="Main.TButton")
        # bStart = ttk.Button(self, text="Start", command=lambda: controller.show_frame(InfoPageBJT), style="Main.TButton")
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

        path = os.path.abspath("TransistorBreadboard.png")

        img = Image.open(path)
        img = img.resize((int(0.5*HEIGHT - 0.05*HEIGHT), int(0.5*HEIGHT - 0.05*HEIGHT)), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)
        panel = ttk.Label(self, image=img)
        panel.image = img
        panel.place(relx=0.35, rely=0.4, relwidth=0.3, relheight=0.5)


class DefectPage(tk.Frame):

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

        bGraph1 = ttk.Button(self, text=Transistortester.nameBJTGraph1, command=lambda: controller.show_frame(Graph1PageBJT), style="bGraph.TButton")
        bGraph1.place(relx=0.35, rely=0.6, relwidth=0.3, relheight=0.1)

        bGraph2 = ttk.Button(self, text=Transistortester.nameBJTGraph2, command=lambda: controller.show_frame(Graph2PageBJT), style="bGraph.TButton")
        bGraph2.place(relx=0.35, rely=0.7, relwidth=0.3, relheight=0.1)

        bGraph3 = ttk.Button(self, text=Transistortester.nameBJTGraph3, command=lambda: controller.show_frame(Graph3PageBJT), style="bGraph.TButton")
        bGraph3.place(relx=0.35, rely=0.8, relwidth=0.3, relheight=0.1)

        frame = tk.Frame(self, bg=ACCENT_COLOR)
        frame.place(relx=0.25, rely=0.15, relwidth=0.5, relheight=0.3)

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
        frame.place(relx=0.1, rely=0.15, relwidth=0.8, relheight=0.3)

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


# Beta in functie van I_C
class Graph1PageBJT(tk.Frame):
    canvas = 0
    fig = Figure(figsize=(10, 8), dpi=100, facecolor=MAIN_COLOR)
    plot = fig.add_subplot(111)

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        style = ttk.Style()
        style.configure('bBack.TButton', font=('Verdana', 10))

        # Graph1PageBJT.canvas = FigureCanvasTkAgg(Transistortester.BJTfig1, self)
        Graph1PageBJT.canvas = FigureCanvasTkAgg(Graph1PageBJT.fig, self)
        Graph1PageBJT.canvas.draw()

        toolbar = NavigationToolbar2Tk(Graph1PageBJT.canvas, self)
        toolbar.configure(bg=ACCENT_COLOR)
        toolbar._message_label.config(background=ACCENT_COLOR)
        toolbar.update()

        Graph1PageBJT.canvas.get_tk_widget().pack()

        label = ttk.Label(self, text=Transistortester.nameBJTGraph1, font=LARGE_FONT, anchor="center", background=MAIN_COLOR)
        label.place(relx=0, rely=0, relwidth=1, relheight=0.1)

        bBack = ttk.Button(self, text="Terug", command=lambda: controller.show_frame(InfoPageBJT), style="bBack.TButton")
        bBack.place(relx=0, rely=0, relwidth=0.15, relheight=0.1)

        bCSV = ttk.Button(self, text="Save CSV", command=lambda: saveCSV.saveCSV(Transistortester.I_C1,
                                                                                 Transistortester.Beta, "I_C", "Beta", "Beta_IC.csv"), style="bBack.TButton")
        bCSV.place(relx=0.85, rely=0, relwidth=0.15, relheight=0.1)

    def update_graph(self):
        Graph1PageBJT.canvas.draw()


# I_C in functie van V_CE
class Graph2PageBJT(tk.Frame):
    canvas = 0
    fig = Figure(figsize=(10, 8), dpi=100, facecolor=MAIN_COLOR)
    plot = fig.add_subplot(111)

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        style = ttk.Style()
        style.configure('bBack.TButton', font=('Verdana', 10))

        # Graph2PageBJT.canvas = FigureCanvasTkAgg(Transistortester.BJTfig2, self)
        Graph2PageBJT.canvas = FigureCanvasTkAgg(Graph2PageBJT.fig, self)
        Graph2PageBJT.canvas.draw()

        toolbar = NavigationToolbar2Tk(Graph2PageBJT.canvas, self)
        toolbar.configure(bg=ACCENT_COLOR)
        toolbar._message_label.config(background=ACCENT_COLOR)
        toolbar.update()

        Graph2PageBJT.canvas.get_tk_widget().pack()

        label = ttk.Label(self, text=Transistortester.nameBJTGraph2, font=LARGE_FONT, anchor="center", background=MAIN_COLOR)
        label.place(relx=0, rely=0, relwidth=1, relheight=0.1)

        bBack = ttk.Button(self, text="Terug", command=lambda: controller.show_frame(InfoPageBJT), style="bBack.TButton")
        bBack.place(relx=0, rely=0, relwidth=0.15, relheight=0.1)

        bCSV = ttk.Button(self, text="Save CSV", command=lambda: saveCSV.saveCSV(Transistortester.V_CE,
                                                                                 Transistortester.I_C2, "V_CE", "I_C", "IC_VCE.csv"), style="bBack.TButton")
        bCSV.place(relx=0.85, rely=0, relwidth=0.15, relheight=0.1)

    def update_graph(self):
        Graph2PageBJT.canvas.draw()

# I_C in functie van V_BE
class Graph3PageBJT(tk.Frame):
    canvas = 0
    fig = Figure(figsize=(10, 8), dpi=100, facecolor=MAIN_COLOR)
    plot = fig.add_subplot(111)

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        style = ttk.Style()
        style.configure('bBack.TButton', font=('Verdana', 10))

        # Graph3PageBJT.canvas = FigureCanvasTkAgg(Transistortester.BJTfig3, self)
        Graph3PageBJT.canvas = FigureCanvasTkAgg(Graph3PageBJT.fig, self)
        Graph3PageBJT.canvas.draw()

        toolbar = NavigationToolbar2Tk(Graph3PageBJT.canvas, self)
        toolbar.configure(bg=ACCENT_COLOR)
        toolbar._message_label.config(background=ACCENT_COLOR)
        toolbar.update()

        Graph3PageBJT.canvas.get_tk_widget().pack()

        label = ttk.Label(self, text=Transistortester.nameBJTGraph3, font=LARGE_FONT, anchor="center", background=MAIN_COLOR)
        label.place(relx=0, rely=0, relwidth=1, relheight=0.1)

        bBack = ttk.Button(self, text="Terug", command=lambda: controller.show_frame(InfoPageBJT), style="bBack.TButton")
        bBack.place(relx=0, rely=0, relwidth=0.15, relheight=0.1)

        bCSV = ttk.Button(self, text="Save CSV", command=lambda: saveCSV.saveCSV(Transistortester.V_BE,
                                                                                 Transistortester.I_C3, "V_BE", "I_C", "IC_VBE.csv"), style="bBack.TButton")
        bCSV.place(relx=0.85, rely=0, relwidth=0.15, relheight=0.1)

    def update_graph(self):
        Graph3PageBJT.canvas.draw()


app = Transistortester()
app.mainloop()

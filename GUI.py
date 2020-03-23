from tkinter import ttk
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib
matplotlib.use("TkAgg")

LARGE_FONT = ("Verdana", 12)
HEIGHT = 480
WIDTH = 800


class Transistortester(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.wm_title(self, "Transistortester")
        
        # self.attributes('-fullscreen', True)      #full-screen windows
        canvas = tk.Canvas(self, height=HEIGHT, width=WIDTH, bg="#80c195")
        canvas.pack()

        self.frames = {}

        for F in (StartPage, PageOne, GraphPage):
            frame = F(canvas, self)
            self.frames[F] = frame
            frame.place(relx=0.1, rely=0.05, relwidth=0.8, relheight=0.9)

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="#80c1ff")
        label = ttk.Label(self, text="Start Page", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        start = ttk.Button(self, text="Start", command=lambda: controller.show_frame(PageOne))
        start.pack()

        graph = ttk.Button(self, text="Graph", command=lambda: controller.show_frame(GraphPage))
        graph.pack()


class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="#80c1ff")
        label = ttk.Label(self, text="Page One", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        back = ttk.Button(self, text="Back to Home", command=lambda: controller.show_frame(StartPage))
        back.pack()


class GraphPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Graph Page", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        back = ttk.Button(self, text="Back to Home", command=lambda: controller.show_frame(StartPage))
        back.pack()

        fig = Figure(figsize=(5, 5), dpi=100)
        fig.add_subplot(111).plot([1, 2, 3, 4, 5, 6, 7, 8], [2, 8, 4, 6, 7, 2, 1, 3])

        canvas = FigureCanvasTkAgg(fig, self)
        canvas.draw()
        

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        # canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand = True)
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand = True)



app = Transistortester()
app.mainloop()

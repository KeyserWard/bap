import shutil
import datetime
import csv
import tkinter as tk
import pandas as pd


def saveCSV(x, y, xTitle, yTitle):
    datafile = tk.filedialog.asksaveasfile(mode="w", defaultextension=".csv")
    datacsv = xTitle + ";" + yTitle + "\n"
    for i in range(len(x)):
        datacsv += "{:.2f}".format(x[i]) + ";" + "{:.2f}".format(y[i]) + "\n"
    datafile.write(datacsv)
    datafile.close()

import os
import csv
import tkinter as tk

# "C:\\Users\\maart\\Downloads"
def saveCSV(x, y, xTitle, yTitle, filename):
    directory = os.listdir("/media/pi")
    print(os.listdir("/media/pi"))
    datafile = tk.filedialog.asksaveasfile(mode="w", title="Save file", initialfile=filename, defaultextension=".csv", initialdir = "/media/pi/"+directory[0])
    print(datafile)
    if(datafile is not None):
        datacsv = xTitle + ";" + yTitle + "\n"
        for i in range(len(x)):
            datacsv += "{:.2f}".format(x[i]) + ";" + "{:.2f}".format(y[i]) + "\n"
        datafile.write(datacsv)
        datafile.close()

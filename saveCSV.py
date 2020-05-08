import os
import csv
import tkinter.filedialog
import tkinter as tk

# "C:\\Users\\maart\\Downloads"
def saveCSV(x, y, xTitle, yTitle, filename):
    directoryUSB = os.listdir("/media/pi")
    print(directoryUSB[0])
    if len(directoryUSB) > 0:
        directoryFiles = os.listdir("/media/pi/" + directoryUSB[0])
        print(directoryFiles)
        origFilename = filename[:-4]
        i = 0
        while filename in directoryFiles:
            i += 1
            print("File already exists")
            filename = origFilename + "_" + str(i) + ".csv"
        datafile = tk.filedialog.asksaveasfile(mode="w", title="Save file", initialfile=filename, defaultextension=".csv", initialdir = "/media/pi/" + directoryUSB[0])
        print(datafile)
        if(datafile is not None):
            datacsv = xTitle + ";" + yTitle + "\n"
            for i in range(len(x)):
                datacsv += "{:.2f}".format(x[i]) + ";" + "{:.2f}".format(y[i]) + "\n"
            datafile.write(datacsv)
            datafile.close()

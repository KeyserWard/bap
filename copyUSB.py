import shutil
import datetime

# From https://stackoverflow.com/questions/43762904/copy-file-to-usb-automatically-on-mount-raspberry-pi
def copyCSV():
    # File to be copied
    source = "/home/pi/Documents/BAP_2020/data.csv"

    # USB name must be changed to 'USB1' in order for auto copy to work
    destination = "/media/pi/USB1/datalogger_backup_%s.txt" % datetime.datetime.now().date()

    try:
        # Copy file to destination
        shutil.copy2(source, destination)
    except shutil.Error as e:   
        # E.g. source and destination is the same location
        print("Error: %s" % e)
    except IOError as e:
        # E.g. source or destination does not exist
        print("Error: %s" % e.strerror)
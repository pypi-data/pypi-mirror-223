import tkinter as tk
from tkinter import *
from pathlib import Path
from PIL import Image
from PIL import ImageTk
import glob

# POT
import board
import busio
i2c = busio.I2C(board.SCL, board.SDA)
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import time

ads = ADS.ADS1115(i2c)

def remap(x, in_min, in_max, out_min, out_max):
  return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

BASE_FOLDER = 'WiggleR'
IMG_FOLDER = f"{BASE_FOLDER}/Pictures"

chan = AnalogIn(ads, ADS.P2)
image_files = sorted(glob.glob(str(Path(__file__).parent / f"{IMG_FOLDER}/*.jpg")))

# adjust window
root=tk.Tk()
root.geometry("1024x768")
l=Label()
l.pack()

stgImg = ImageTk.PhotoImage(Image.open(image_files[0]))
label=tk.Label(root, image=stgImg)

def changeImage():
    mappedValue = remap(chan.voltage, 0, 5, 0, len(image_files))
    imageIndex = round(mappedValue)
    imageFile = image_files[imageIndex]
    stgImg = ImageTk.PhotoImage(Image.open(imageFile))
    l.config(image=stgImg)
    label.image = stgImg
    root.after(200, changeImage)

'''main function''' 
def main():
    changeImage()
    root.mainloop()

if __name__ == '__main__':
    main()

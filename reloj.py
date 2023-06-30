from tkinter import Label, Frame, Tk
from tkinter.ttk import *
from time import strftime
from googletrans import Translator

def update_clock():
    label_hm.config(text=strftime ("%H:%M"))
    label_s.config(text=strftime ("%S"))
    label_date.config(text=(translator.translate(strftime ("%A,"), dest='es').text, strftime("%d/%m/%Y")))
    label_s.after(1000, update_clock)

root = Tk()
root.title("Reloj digital by LorelizDev")

frame_hour = Frame()
frame_hour.pack()
label_hm = Label(frame_hour, font=("Goudy Old Style", 100), text="H:M")
label_hm.grid(row=0, column=0)

label_s = Label(frame_hour, font=("Goudy Old Style", 50), text="s")
label_s.grid(row=0, column=1, sticky="n") # para ubicarla en la parte norte, superior

label_date = Label(font=("Goudy Old Style", 30), text="dia")
label_date.pack()

translator = Translator()

update_clock()

root.mainloop()
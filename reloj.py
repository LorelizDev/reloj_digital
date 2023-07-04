from tkinter import Label, Frame, Tk, messagebox, PhotoImage
from tkinter.ttk import *
from time import strftime
import threading, time
from googletrans import Translator
from pygame import mixer

def switch():
    global is_on

    if is_on:
        switch_alarm.config(image = on)
        is_on = False
        update_alarm()
    else:
        switch_alarm.config(image = off)
        is_on = True

def update_alarm():
    if is_on == False:
        if spinbox_h.get() == strftime("%I"):
            if spinbox_m.get() == strftime("%M"):
                if int(strftime("%S")) == 00:
                    if spinbox_ampm.get() == strftime("%p"):
                        threading.Thread(target=play_alarm).start()
                        messagebox.showinfo(message=strftime("%I:%M %p"), title="Alarma")
                        switch()
    root.after(900, update_alarm)

def play_alarm():
    mixer.init()
    mixer.music.load(f'audios/{combobox_audios.get()}.mp3')
    mixer.music.play(loops=-1)
    time.sleep(int(duration.get()))
    mixer.music.stop()
    mixer.quit()

def update_clock():
    label_hm.config(text=strftime ("%I:%M")) # Formato 12 horas
    label_s.config(text=strftime ("%S"))
    label_ampm.config(text=strftime ("%p"))
    translated_day = translator.translate(strftime("%A"), dest='es').text
    label_date.config(text=f"{translated_day}, {strftime('%d/%m/%Y')}")
    label_s.after(900, update_clock)

root = Tk()
root.title("Reloj digital by LorelizDev")
frame_hour = Frame(root)
frame_hour.pack()
tabs = Notebook(root)
tabs.pack(pady=30, padx=10)
tab1 = Frame(tabs)
tab2 = Frame(tabs)
tab3 = Frame(tabs)
tab4 = Frame(tabs)
tab1.pack()
tab2.pack()
tab3.pack()
tab4.pack()
tabs.add(tab1, text="ALARMA")
tabs.add(tab2, text="CRONÓMETRO")
tabs.add(tab3, text="TEMPORIZADOR")
tabs.add(tab4, text="RELOJ MUNDIAL")
frame_alarm = Frame(tab1)
frame_alarm.pack(pady=20)

# ---------------------- ALARMA ----------------------
list_audios = ["alarm-clock_1", "alarm-clock_2", "alarm-rooster", "alarm-relax", "alarm_evacuation", "alarm_fire", "alarm_alarma"]
list_h = []
list_m = []

for h in range(1,13):
    if h < 10:
        list_h.append(f'0{h}')
    else:
        list_h.append(h)

for m in range(0,60):
    if m < 10:
        list_m.append(f'0{m}')
    else:
        list_m.append(m)

off = PhotoImage(file="img/off.png")
on = PhotoImage(file="img/on.png")

is_on = True

spinbox_h = Combobox(frame_alarm, values=list_h, font=("Goudy Old Style", 30), width=2, state="readonly")
spinbox_h.pack(side="left")
spinbox_h.set(strftime("%I"))

label_colon = Label(frame_alarm, text=":", font=("Goudy Old Style", 40))
label_colon.pack(side="left")

spinbox_m = Combobox(frame_alarm, values=list_m, font=("Goudy Old Style", 30), width=2, state="readonly")
spinbox_m.pack(side="left")
spinbox_m.set(strftime("%M"))

spinbox_ampm = Combobox(frame_alarm, values=["AM", "PM"], font=("Goudy Old Style", 20), width=3, state="readonly")
spinbox_ampm.pack(side="left", ipady=7)
spinbox_ampm.set(strftime("%p"))

switch_alarm = Button(frame_alarm, image=off, command=switch)
switch_alarm.pack(side="right")

label_audios = Label(tab1, text="Audio:", font=("Goudy Old Style", 16))
label_audios.pack(side="left", padx=(30,5))

combobox_audios = Combobox(tab1, values=list_audios, state="readonly",font=("Goudy Old Style", 14), width=15)
combobox_audios.pack(side="left")
combobox_audios.current(0)

label_duration = Label(tab1, text="Duración:", font=("Goudy Old Style", 16))
label_duration.pack(side="left", padx=(50,5))

duration = Combobox(tab1, values=(5,10,15,20,25,30), state="readonly", width=5, font=("Goudy Old Style", 14))
duration.pack(side="left", padx=(0, 30))
duration.current(1)

# ---------------------- RELOJ -----------------------
label_hm = Label(frame_hour, font=("Goudy Old Style", 100), text="H:M")
label_hm.grid(row=0, column=0, rowspan=2)

label_s = Label(frame_hour, font=("Goudy Old Style", 40), text="s")
label_s.grid(row=0, column=1, sticky="n") # para ubicarla en la parte norte, superior

label_ampm = Label(frame_hour, font=("Goudy Old Style", 30), text="am/pm")
label_ampm.grid(row=1, column=1)

label_date = Label(font=("Goudy Old Style", 30), text="dia")
label_date.pack(after=frame_hour)

translator = Translator()
update_clock()

root.mainloop()
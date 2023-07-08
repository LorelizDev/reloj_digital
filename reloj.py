import subprocess
import sys
from tkinter import Label, Frame, Tk, messagebox, PhotoImage, Button
from tkinter.ttk import *
from datetime import datetime
import threading, time
from googletrans import Translator
from pygame import mixer
import pytz
import requests

# ---------------------- FUNCIONALIDAD DEL RELOJ ----------------------
def update_clock():
    try:
        label_hm.config(text=datetime.now().strftime("%I:%M")) # Formato 12 horas
        label_s.config(text=datetime.now().strftime("%S"))
        label_ampm.config(text=datetime.now().strftime("%p"))
        translated_day = translator.translate(datetime.now().strftime("%A"), dest='es').text
        label_date.config(text=f'{translated_day}, {datetime.now().strftime("%d/%m/%Y")}')
        label_s.after(200, update_clock)
    except:
        root.destroy() # Cerrar la ventana principal
        python = sys.executable # Reiniciar la aplicación
        cmd = [python] + sys.argv
        subprocess.call(cmd) # Ejecutar nuevamente el script Python

# ---------------------- FUNCIONALIDAD DE LA ALARMA ----------------------
def switch():
    global is_on

    if is_on:
        switch_alarm.config(image = off)
        is_on = False
    else:
        switch_alarm.config(image = on)
        is_on = True
        update_alarm()

def update_alarm():
    if is_on:
        if alarm_h.get() == datetime.now().strftime("%I"):
            if alarm_m.get() == datetime.now().strftime("%M"):
                if int(datetime.now().strftime("%S")) == 00:
                    if alarm_ampm.get() == datetime.now().strftime("%p"):
                        threading.Thread(target=play_alarm).start()
                        messagebox.showinfo(message=datetime.now().strftime("%I:%M %p"), title="Alarma")
                        switch()
    root.after(200, update_alarm)

def play_alarm():
    mixer.init()
    mixer.music.load(f'audios/{alarm_audios.get()}.mp3')
    mixer.music.play(loops=-1)
    time.sleep(int(duration.get()))
    mixer.music.stop()
    mixer.quit()

# ---------------------- FUNCIONALIDAD DEL CRONOMETRO ----------------------
def start_stop_t():
    threading.Thread(target=start_stop).start()

def start_stop():
    global chrono_h, chrono_m, chrono_s, click_start, click_restore
    
    if click_start:
        click_start = False
        stop_button.grid_forget()
        start_button.grid(column=0, row=0)
        if click_restore:
            click_restore = False
    else:
        click_start = True
        start_button.grid_forget()
        stop_button.grid(column=0, row=0)
    
    while click_start:
        if int(chrono_s) == 59:
            chrono_s = "00"
            if int(chrono_m) == 59:
                chrono_m = "00"
                if int(chrono_h) == 23:
                    chrono_h = "00"
                else:
                    chrono_h = str(int(chrono_h) + 1).zfill(2)
            else:
                chrono_m = str(int(chrono_m) + 1).zfill(2)
        else:
            chrono_s = str(int(chrono_s) + 1).zfill(2)
        
        label_chrono.config(text=f'{chrono_h}:{chrono_m}:{chrono_s}')
        time.sleep(1)

def lap():
    global laps
    laps += 1

    if laps == 1:
        lap_1.config(text=f'{chrono_h}:{chrono_m}:{chrono_s}')
    elif laps == 2:
        lap_2.config(text=f'{chrono_h}:{chrono_m}:{chrono_s}')
    elif laps == 3:
        lap_3.config(text=f'{chrono_h}:{chrono_m}:{chrono_s}')
    elif laps == 4:
        lap_4.config(text=f'{chrono_h}:{chrono_m}:{chrono_s}')
    elif laps == 5:
        lap_5.config(text=f'{chrono_h}:{chrono_m}:{chrono_s}')
        laps = 0

def restore_chrono():
    global chrono_h, chrono_m, chrono_s, laps, click_restore
    chrono_h = "00"
    chrono_m = "00"
    chrono_s = "00"
    label_chrono.config(text=f'{chrono_h}:{chrono_m}:{chrono_s}')
    lap_1.config(text="Vuelta 1")
    lap_2.config(text="Vuelta 2")
    lap_3.config(text="Vuelta 3")
    lap_4.config(text="Vuelta 4")
    lap_5.config(text="Vuelta 5")
    laps = 0
    if click_start:
        click_restore = True
        start_stop_t()

# ---------------------- FUNCIONALIDAD DEL TEMPORIZADOR ----------------------
def click_play():
    global is_running

    if timer_s.get() != "00" or timer_m.get() != "00" or timer_h.get() != "00":
        if is_running:
            timer_play.config(image = play, text="continue")
            is_running = False
        else:
            timer_play.config(image = pause)
            is_running = True
        play_stop_t()

def play_stop_t():
    threading.Thread(target=play_stop).start()

def play_stop():
    global timer_hh, timer_mm, timer_ss, is_running

    if timer_play.cget("text") == "play":
        timer_hh = timer_h.get()
        timer_mm = timer_m.get()
        timer_ss = timer_s.get()
    
    if is_running:
        while is_running:
            label_timer.config(text=f'{timer_hh}:{timer_mm}:{timer_ss}')
            if label_timer.cget("text") == "00:00:00":
                threading.Thread(target=timer_alarm).start()
                messagebox.showinfo(message="Se ha agotado el tiempo", title="Temporizador")
                click_play()
            elif int(timer_ss) == 0:
                timer_ss = 59
                if int(timer_mm) == 0:
                    timer_mm = 59
                    if int(timer_hh) != 0:
                        timer_hh = str(int(timer_hh) - 1).zfill(2)
                else:
                    timer_mm = str(int(timer_mm) - 1).zfill(2)
            else:
                timer_ss = str(int(timer_ss) - 1).zfill(2)
            time.sleep(1)

def timer_alarm():
    mixer.init()
    mixer.music.load("audios/alarm-clock_2.mp3")
    mixer.music.play()
    time.sleep(4)
    mixer.music.stop()
    mixer.quit()

def restore_timer():
    global is_running    
    label_timer.config(text="00:00:00")
    timer_play.config(text="play", image=play)
    is_running = False
    play_stop_t()

# ---------------------- FUNCIONALIDAD DEL RELOJ MUNDIAL -----------------------
def world_time():
    time_zone = pytz.timezone(box_locations.get())
    current_time_location = datetime.now(time_zone)
    label_world_hm.config(text=current_time_location.strftime("%I:%M"))
    label_world_s.config(text=current_time_location.strftime("%S"))
    label_world_ampm.config(text=current_time_location.strftime("%p"))
    label_world_date.config(text=current_time_location.strftime("%d/%m/%Y"))
    label_world_s.after(200, world_time)

# ---------------------- CLIMA MUNDIAL -----------------------
def get_city(locations, location):
    for city, loc in locations.items():
        if loc == location:
            return city

def wheater():
    city = get_city(locations, box_locations.get())

    if city != "GMT" and city != "UTC":
        API = f'https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&lang=es&appid=2d870eb188bdc4d8c687ae187bd09444'
        json_data = requests.get(API).json()
        label_temp.config(text=f"{int(json_data['main']['temp'])} ºC")
        label_description_w.config(text=json_data['weather'][0]['description'])
    else:
        label_temp.config(text="-")
        label_description_w.config(text="-")

    label_temp.after(200, wheater)

# ---------------------- FRAMES Y PESTAÑAS -----------------------
root = Tk()
root.title("Reloj digital by LorelizDev")

frame_hour = Frame(root)
frame_hour.pack()

tabs = Notebook(root)
tabs.pack(pady=30, padx=10)
tab_alarm = Frame(tabs)
tab_chrono = Frame(tabs)
tab_timer = Frame(tabs)
tab_world = Frame(tabs)
tab_alarm.pack()
tab_chrono.pack()
tab_timer.pack()
tab_world.pack()
tabs.add(tab_alarm, text="ALARMA")
tabs.add(tab_chrono, text="CRONÓMETRO")
tabs.add(tab_timer, text="TEMPORIZADOR")
tabs.add(tab_world, text="RELOJ MUNDIAL")

frame_alarm = Frame(tab_alarm)
frame_alarm.pack(pady=(50,30))
frame_audios = Frame(tab_alarm)
frame_audios.pack(pady=20)

frame_chrono = Frame(tab_chrono)
frame_chrono.pack(pady=20)
frame_laps = Frame(tab_chrono)
frame_laps.pack()
frame_chrono_buttons = Frame(tab_chrono)
frame_chrono_buttons.pack(pady=20)

frame_timer = Frame(tab_timer)
frame_timer.pack(pady=20)
frame_timer_config = Frame(tab_timer)
frame_timer_config.pack()
frame_timer_button = Frame(tab_timer)
frame_timer_button.pack(pady=20)

frame_world = Frame(tab_world)
frame_world.pack(pady=20)
frame_locations = Frame(tab_world)
frame_locations.pack()

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

# ---------------------- ALARMA ----------------------
list_audios = ["alarm-clock_1", "alarm-clock_2", "alarm-rooster", "alarm-relax", "alarm_evacuation", "alarm_fire", "alarm_alarma"]
list_h = []
list_m = []

for h in range(1,13):
    list_h.append(str(h).zfill(2))

for m in range(0,60):
    list_m.append(str(m).zfill(2))

off = PhotoImage(file="img/off.png")
on = PhotoImage(file="img/on.png")

is_on = False

alarm_h = Combobox(frame_alarm, values=list_h, font=("Goudy Old Style", 30), width=2, state="readonly")
alarm_h.pack(side="left")
alarm_h.set(datetime.now().strftime("%I"))

label_colon = Label(frame_alarm, text=":", font=("Goudy Old Style", 40))
label_colon.pack(side="left")

alarm_m = Combobox(frame_alarm, values=list_m, font=("Goudy Old Style", 30), width=2, state="readonly")
alarm_m.pack(side="left")
alarm_m.set(datetime.now().strftime("%M"))

alarm_ampm = Combobox(frame_alarm, values=["AM", "PM"], font=("Goudy Old Style", 20), width=3, state="readonly")
alarm_ampm.pack(side="left", ipady=7)
alarm_ampm.set(datetime.now().strftime("%p"))

switch_alarm = Button(frame_alarm, image=off, command=switch)
switch_alarm.pack(side="right", padx=10)

label_audios = Label(frame_audios, text="Audio:", font=("Goudy Old Style", 16))
label_audios.pack(side="left", padx=(30,5))

alarm_audios = Combobox(frame_audios, values=list_audios, state="readonly",font=("Goudy Old Style", 14), width=15)
alarm_audios.pack(side="left")
alarm_audios.current(0)

label_duration = Label(frame_audios, text="Duración:", font=("Goudy Old Style", 16))
label_duration.pack(side="left", padx=(50,5))

duration = Combobox(frame_audios, values=(5,10,15,20,25,30), state="readonly", width=5, font=("Goudy Old Style", 14))
duration.pack(side="left", padx=(0, 30))
duration.current(1)

# ---------------------- CRONÓMETRO ----------------------
chrono_h = "00"
chrono_m = "00"
chrono_s = "00"
click_start = False
click_restore = False
laps = 0
play = PhotoImage(file="img/play.png")
pause = PhotoImage(file="img/pause.png")
restore = PhotoImage(file="img/restore.png")
lap_image = PhotoImage(file="img/lap.png")

label_chrono = Label(frame_chrono, font=("Goudy Old Style", 50), text="00:00:00")
label_chrono.pack()

lap_1 = Label(frame_laps, font=("Goudy Old Style", 14), text="Vuelta 1")
lap_1.grid(row=0, column=0, padx=15)

lap_2 = Label(frame_laps, font=("Goudy Old Style", 14), text="Vuelta 2")
lap_2.grid(row=0, column=1, padx=15)

lap_3 = Label(frame_laps, font=("Goudy Old Style", 14), text="Vuelta 3")
lap_3.grid(row=0, column=2, padx=15)

lap_4 = Label(frame_laps, font=("Goudy Old Style", 14), text="Vuelta 4")
lap_4.grid(row=0, column=3, padx=15)

lap_5 = Label(frame_laps, font=("Goudy Old Style", 14), text="Vuelta 5")
lap_5.grid(row=0, column=4, padx=15)

stop_button = Button(frame_chrono_buttons, width=20, image=pause, command=start_stop_t)
stop_button.grid(row=0, column=0)

start_button = Button(frame_chrono_buttons, width=20, image=play, command=start_stop_t)
start_button.grid(row=0, column=0)

lap_button = Button(frame_chrono_buttons, width=20, image=lap_image, command=lap)
lap_button.grid(row=0, column=1)

restore_button = Button(frame_chrono_buttons, width=20, image=restore, command=restore_chrono)
restore_button.grid(row=0, column=2)

# ---------------------- TEMPORIZADOR ----------------------
is_running = 0
timer_hh = "00"
timer_mm = "00"
timer_ss = "00"

label_timer = Label(frame_timer, font=("Goudy Old Style", 50), text="00:00:00")
label_timer.pack()

timer_h = Spinbox(frame_timer_config, values=list_m, font=("Goudy Old Style", 30), width=2, state="readonly")
timer_h.grid(row=0, column=0)
timer_h.set(list_m[0])

timer_colon_1 = Label(frame_timer_config, font=("Goudy Old Style", 30), text=":")
timer_colon_1.grid(row=0, column=1)

timer_m = Spinbox(frame_timer_config, values=list_m, font=("Goudy Old Style", 30), width=2, state="readonly")
timer_m.grid(row=0, column=2)
timer_m.set(list_m[0])

timer_colon_2 = Label(frame_timer_config, font=("Goudy Old Style", 30), text=":")
timer_colon_2.grid(row=0, column=3)

timer_s = Spinbox(frame_timer_config, values=list_m, font=("Goudy Old Style", 30), width=2, state="readonly")
timer_s.grid(row=0, column=4)
timer_s.set(list_m[0])

timer_play = Button(frame_timer_button, text="play", image=play, command=click_play)
timer_play.grid(row=0, column=0)

timer_restore = Button(frame_timer_button, image=restore, command=restore_timer)
timer_restore.grid(row=0, column=1)

# ---------------------- RELOJ MUNDIAL -----------------------
locations = {'Cairo':'Africa/Cairo', 'Johannesburg':'Africa/Johannesburg', 'Lagos':'Africa/Lagos', 'Luanda':'Africa/Luanda', 'Nairobi':'Africa/Nairobi', 'Buenos Aires':'America/Argentina/Buenos_Aires', 'Asuncion':'America/Asuncion', 'Barbados':'America/Barbados', 'Bogota':'America/Bogota', 'Caracas':'America/Caracas', 'Chicago':'America/Chicago', 'El Salvador':'America/El_Salvador', 'Guayaquil':'America/Guayaquil', 'Jamaica':'America/Jamaica', 'La Paz':'America/La_Paz', 'Lima':'America/Lima', 'Los Angeles':'America/Los_Angeles', 'Mexico City':'America/Mexico_City', 'New York':'America/New_York', 'Panama':'America/Panama', 'Santiago':'America/Santiago', 'Santo Domingo':'America/Santo_Domingo', 'Sao Paulo':'America/Sao_Paulo', 'Amman':'Asia/Amman', 'Baghdad':'Asia/Baghdad', 'Beirut':'Asia/Beirut', 'Dubai':'Asia/Dubai', 'Hong Kong':'Asia/Hong_Kong', 'Jerusalem':'Asia/Jerusalem', 'Qatar':'Asia/Qatar', 'Seoul':'Asia/Seoul', 'Shanghai':'Asia/Shanghai', 'Singapore':'Asia/Singapore', 'Tokyo':'Asia/Tokyo', 'Cabo Verde':'Atlantic/Cape_Verde', 'Sydney':'Australia/Sydney', 'Amsterdam':'Europe/Amsterdam', 'Berlin':'Europe/Berlin', 'Brussels':'Europe/Brussels', 'Budapest':'Europe/Budapest', 'Dublin':'Europe/Dublin', 'Istanbul':'Europe/Istanbul', 'Lisbon':'Europe/Lisbon', 'London':'Europe/London', 'Luxembourg':'Europe/Luxembourg', 'Madrid':'Europe/Madrid', 'Moscow':'Europe/Moscow', 'Paris':'Europe/Paris', 'Rome':'Europe/Rome', 'Vatican':'Europe/Vatican', 'Vienna':'Europe/Vienna', 'Zurich':'Europe/Zurich', 'GMT':'GMT', 'Auckland':'Pacific/Auckland', 'Easter':'Pacific/Easter', 'Alaska':'US/Alaska',  'Central':'US/Central', 'Eastern':'US/Eastern', 'Hawaii':'US/Hawaii', 'Pacific':'US/Pacific', 'UTC':'UTC'}

list_locations = []

for loc in locations.values():
    list_locations.append(loc)

label_world_hm = Label(frame_world, font=("Goudy Old Style", 50), text="H:M")
label_world_hm.grid(row=0, column=0, rowspan=2)

label_world_s = Label(frame_world, font=("Goudy Old Style", 30), text="s")
label_world_s.grid(row=0, column=1, sticky="n")

label_world_ampm = Label(frame_world, font=("Goudy Old Style", 20), text="am/pm")
label_world_ampm.grid(row=1, column=1)

label_world_date = Label(frame_world, font=("Goudy Old Style", 16), text="dd/mm/Y")
label_world_date.grid(row=3, columnspan=2, pady=10)

label_locations = Label(frame_locations, font=("Goudy Old Style", 20), text="Ubicación:")
label_locations.grid(row=0, column=0, padx=10)

box_locations = Combobox(frame_locations, values=list_locations, font=("Goudy Old Style", 16), state="readonly")
box_locations.grid(row=0, column=1)
box_locations.set(list_locations[0])

world_time()

# ---------------------- CLIMA MUNDIAL -----------------------
label_temp = Label(frame_world, font=("Goudy Old Style", 20))
label_temp.grid(row=4, columnspan=2)

label_description_w = Label(frame_world, font=("Goudy Old Style", 16))
label_description_w.grid(row=5, columnspan=2)

wheater()

root.mainloop()
import time
from kalibrasi import Kalibrasi_sensor_jarak
from service import Service
from time import sleep as dellay
# port = "/dev/ttyUSB1"
port = "COM6"
kalibrasi = Kalibrasi_sensor_jarak()
ser = Service(kalibrasi,port)

import tkinter as tk

class GUI:
    def __init__(self,service:Service):
        self.service = service
        self.page = "main"
        self.dist = 0
        self.window = tk.Tk()
        self.window.geometry("500x300")
        self.label = tk.Label(self.window, text=str(self.dist)+" cm")
        self.label.pack()
        self.update_sensor()
        self.main()
        self.window.mainloop()

    def update_sensor(self):
        self.dist = self.service.get_distace_from_sensor()
        if self.page == "main": self.label['text'] = str(self.dist)  +" cm"
        if self.dist<20 and self.page == "main": self.controler(); self.page="controler"
        if self.dist>20 and self.page == "controler": self.main(); self.page="main"
        self.window.after(500,self.update_sensor)

    def main(self):
        self.window.title("Main")
        for i in self.window.winfo_children(): i.destroy()
        self.label = tk.Label(self.window, text=str(self.dist)+" cm")
        self.label.pack()

    def controler(self):
        self.window.title("Controler")
        for i in self.window.winfo_children(): i.destroy()
        button = tk.Button(self.window, text=f"alarm", command=self.service.trigger_alarm)
        button.pack()
        button = tk.Button(self.window, text=f"Open Locker{0}", command=lambda : self.service.open_locker(0))
        button.pack()
        button = tk.Button(self.window,text=f"Close Locker{0}", command=lambda : self.service.close_locker(0))
        button.pack()
        button = tk.Button(self.window, text=f"Open Locker{1}", command=lambda : self.service.open_locker(1))
        button.pack()
        button = tk.Button(self.window,text=f"Close Locker{1}", command=lambda : self.service.close_locker(1))
        button.pack()
        button = tk.Button(self.window, text=f"Open Locker{2}", command=lambda : self.service.open_locker(2))
        button.pack()
        button = tk.Button(self.window,text=f"Close Locker{2}", command=lambda : self.service.close_locker(2))
        button.pack()
        button = tk.Button(self.window, text=f"Open Locker{3}", command=lambda : self.service.open_locker(3))
        button.pack()
        button = tk.Button(self.window,text=f"Close Locker{3}", command=lambda : self.service.close_locker(3))
        button.pack()
        button = tk.Button(self.window,
                                text=f"Open ALL",
                                command=self.service.open_all)
        button.pack()
        button = tk.Button(self.window,
                                text=f"Close ALL",
                                command=self.service.close_all)
        button.pack()
    


        # self.service.send_to_serial("0")
        # self.service.automatic_calibration()
        # self.service.ser.write(bytes(str(1), "utf-8"))
        # self.service.send_to_serial("2")
        # self.service.send_to_serial(0)
        # print("haha")
        # # self.service.open_locker(1)
        # self.service.send_to_serial(2)
        # dellay(2)
        # self.service.open_all()
        # self.service.close_all()
        # # self.service.send_to_serial(1)
    
gui = GUI(ser)
# gui.main()
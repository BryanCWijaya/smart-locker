import serial

from kalibrasi import Kalibrasi_sensor_jarak
from service import Service
# ser = serial.Serial('/dev/ttyUSB1', 9600, timeout=1)
# ser.reset_input_buffer()
kalibrasi = Kalibrasi_sensor_jarak()
service = Service(kalibrasi,"/dev/ttyUSB0")

service.automatic_calibration()
# while True:
#     ser.write(bytes(str(8), "utf-8"))
#     # # ser.write(bytes(str(9), "utf-8"))
#     print("haha")
#     # # service.send_to_serial(9)
#     res = ser.readline().decode().strip()
#     print(res)
#     if  res != "":
#         duration, distance = res.split()
#         print(float(duration),"|",distance)
#         duration = float(res.decode())/(10**6)
#         jarak = kalibrasi.kalibrasi(duration)
#         jarak_asli = duration * 0.034 / 2
#         print(jarak,jarak_asli)
#     # a = input()
    # ser.write(bytes(str(a), "utf-8"))
    # print(ser.readline())
    # print(ser.readline())
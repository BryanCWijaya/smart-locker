from service import Service
from ui import UI
from kalibrasi import Kalibrasi_sensor_jarak
from repository import FaceDB

if __name__ == "__main__":
    serv = Service(kalibrasi=Kalibrasi_sensor_jarak(), port = "/dev/ttyUSB0")
    ui = UI(serv)
    ui.start()
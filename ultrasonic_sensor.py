#Libraries
import RPi.GPIO as GPIO
import time
from kalibrasi import Kalibrasi_sensor_jarak
 
class Distance_Sensor:
    def __init__(self, kalibration:Kalibrasi_sensor_jarak):
        GPIO.setmode(GPIO.BCM)
        self.GPIO_TRIGGER = 18
        self.GPIO_ECHO = 24
        GPIO.setup(self.GPIO_TRIGGER, GPIO.OUT)
        GPIO.setup(self.GPIO_ECHO, GPIO.IN)
        self.kalibration = kalibration.kalibrasi
    
        
    def get_distance(self):
        # set Trigger to HIGH
        GPIO.output(self.GPIO_TRIGGER, True)
    
        # set Trigger after 0.01ms to LOW
        time.sleep(0.00001)
        GPIO.output(self.GPIO_TRIGGER, False)
        StartTime = time.time()
        StopTime = time.time()
    
        # save StartTime
        while GPIO.input(self.GPIO_ECHO) == 0:
            StartTime = time.time()
            
        # save time of arrival
        while GPIO.input(self.GPIO_ECHO) == 1:
            StopTime = time.time()
        
        # time difference between start and arrival
        TimeElapsed = StopTime - StartTime

        return self.kalibration(TimeElapsed)

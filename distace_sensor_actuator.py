#Libraries
import RPi.GPIO as GPIO
import time
import serial
 
#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
 
#set GPIO Pins
GPIO_TRIGGER = 18
GPIO_ECHO = 24
 
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
 
def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
    StartTime = time.time()
    StopTime = time.time()
    
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
        
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
    print(TimeElapsed,distance)
 
    return distance

def getTimeElapsed():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
    StartTime = time.time()
    StopTime = time.time()
    
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
        
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
 
    return TimeElapsed


if __name__ == '__main__':
    try:
        ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
        ser.reset_input_buffer()
        # data = []
        # for i in range(0,61,3):
        #     input(f"Ambil data untuk {i} cm.")
        #     TimeElcapsed = getTimeElapsed()
        #     print("Pencatatan waktu:",TimeElcapsed)
        #     data.append((i,TimeElcapsed))
        # for i,j in data:
        #     print(i,j)
        while True:
            dist = distance()
            print ("Measured Distance = %.1f cm" % dist)
            if dist<=10:
                ser.write(b'2')
                print("MAsukk")
            elif dist <= 20:
                ser.write(b'1')
            else:
                ser.write(b'0')
                print('GKkkk')
            time.sleep(1)
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()




    

        
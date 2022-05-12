import os, cv2, dlib
from turtle import distance
# from signal import alarm
import numpy as np
from threading import Thread
from kalibrasi import Kalibrasi_sensor_jarak
from repository import FaceDB
from time import sleep as dellay
import serial
import random
import time

class WebcamVideoStream:
    def __init__(self):
        # initialize the video camera stream and read the first frame
		# from the stream
        self.stream = cv2.VideoCapture(0)
        (self.grabbed, self.frame) = self.stream.read()
		# initialize the variable used to indicate if the thread should
		# be stopped
        self.stopped = False
    def start(self):
		# start the thread to read frames from the video stream
        Thread(target=self.update, args=()).start()
        return self
    def update(self):
		# keep looping infinitely until the thread is stopped
        while True:
            # if the thread indicator variable is set, stop the thread
            if self.stopped:
                return
            # otherwise, read the next frame from the stream
            (self.grabbed, image) = self.stream.read()
            # self.frame = cv2.rotate(image, cv2.ROTATE_180)
            self.frame = image
    def read(self):
        # return the frame most recently read
        return self.frame
    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True


class FaceEncoder:
    def __init__(self, cam) -> None:
        self.cam = cam
        # https://github.com/davisking/dlib-models
        self.pose_predictor = dlib.shape_predictor("shape_predictor_5_face_landmarks.dat")
        # self.pose_predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks_GTX.dat")
        self.face_encoder = dlib.face_recognition_model_v1("dlib_face_recognition_resnet_model_v1.dat")
        self.face_detector = dlib.get_frontal_face_detector()
    
        img = cam.read()
        face_locations = self.face_detector(img) # return list of dlib rect object
        self.bounds = self.trim_face_locations(img, face_locations)
        self.encoded_faces = self.get_face_encode(img, face_locations)  
        self.stopped = False
    
    def trim_face_locations(self, img, face_locations):
        bounds = []
        for face in face_locations: # convert dlib rect to tuple of bound 
            height, width, channel = img.shape
            bound = max(face.top(), 0), min(face.right(), width), min(face.bottom(), height), max(face.left(), 0)
            bounds.append(bound)
        return bounds
    
    def get_face_encode(self, img, face_locations):
        encoded_face = []
        for face in face_locations:
            points = self.pose_predictor(img, face) # predict 5 point
            # for showing 5 points
            # for point in points.parts():
            #     img = cv2.circle(img, (point.x, point.y), 5, (255,255,255), 5)
            # cv2.imshow('cam', img)
            encoded = np.array(self.face_encoder.compute_face_descriptor(img, points, 1)) # encode information
            encoded_face.append(encoded)
        # print(encoded_face)
        return encoded_face

    def start(self):
        Thread(target=self.process, args=()).start()
        return self

    def process(self):
        while True:
            if self.stopped:
                return
            img = self.cam.read()
            face_locations = self.face_detector(img) # return list of dlib rect object
            self.bounds = self.trim_face_locations(img, face_locations)
            self.encoded_faces = self.get_face_encode(img, face_locations)    
    
    def get_encoded_faces(self):
        return self.encoded_faces
    
    def get_encoded_faces_and_bounds(self):
        return self.encoded_faces, self.bounds
    
    def stop(self):
        self.stopped = True


class Service:
    # kalibrasi : Kalibrasi_sensor_jarak,port="/dev/ttyUSB1"
    def __init__(self, kalibrasi : Kalibrasi_sensor_jarak,port="/dev/ttyUSB0") -> None:
        self.DB = FaceDB()
        self.ser = serial.Serial(port, 9600, timeout=1)
        self.ser.reset_input_buffer()
        self.kalibrasi = kalibrasi
        self.locker_state = [0,0,0,0]
        dellay(2)
        self.automatic_calibration()

    def open_locker(self,num):
        if self.locker_state[num] == 0:
            self.send_to_serial(num)
            self.locker_state[num] = 1
    
    def close_locker(self,num):
        if self.locker_state[num] == 1:
            self.send_to_serial(num)
            self.locker_state[num] = 0

    def close_all(self):
        self.send_to_serial(4)
        self.locker_state = [0,0,0,0]

    def open_all(self):
        [self.open_locker(i) for i in range(4)]
        self.locker_state = [1,1,1,1]
    
    def trigger_alarm(self):
        self.send_to_serial(5)

    def receive_from_serial(self):
        self.ser.readline()
        res = self.ser.readline().decode().strip()
        return res
        
    def send_to_serial(self,code):
        # Code:
        # 0 -> Open/close servo 0
        # 1 -> Open/close servo 1
        # 2 -> Open/close servo 2
        # 3 -> Open/close servo 3
        # 4 -> Close all
        # 5 -> Alarm
        # 6 -> Get duration
        # 7 -> Get distance
        # 8 -> Get duration & distance
        # 9 -> Stop get anything
        self.ser.write(bytes(str(code)+"\n", "utf-8"))

    def get_distace_from_sensor(self):
        self.send_to_serial(9)
        self.send_to_serial(6)
        res = self.receive_from_serial()
        if res != "":
            dist = self.kalibrasi.calculate(float(res))
            return dist
        return self.get_distace_from_sensor()
    
    def automatic_calibration(self):
        print("New Calibration Start")
        list_durasi = []
        list_jarak = []
        self.ser.flushInput()
        for i in range(20):
            self.send_to_serial(8)
            res = self.receive_from_serial()
            print(res)
            if  res != "":
                duration, distance = res.split()
                list_durasi.append(float(duration))
                list_jarak.append(int(distance))
        self.send_to_serial(9)
        print(list_durasi,list_jarak)
        self.kalibrasi.new_calibration(list_jarak,list_durasi)
        print("Calibration Complete")

    def get_distance(self, known_face_encodings, face_encoding_to_check):
        if len(known_face_encodings) == 0 or len(face_encoding_to_check) == 0:
            return -1
        else:
            euclidean_distance = np.linalg.norm(known_face_encodings - face_encoding_to_check, axis=1)
            return list(euclidean_distance)

    def get_registered_image(self):
        encoded_faces = []
        names = []
        folder = 'known_face'
        for img_name in os.listdir(folder):
            name = os.path.splitext(img_name)[0]
            with open('known_face/'+img_name, 'r') as f:
                encode = np.array(f.read().split(","), 'float64')
            names.append(name)
            encoded_faces.append(encode)
        return encoded_faces, names

    def face_regis(self, name):
        cam = WebcamVideoStream().start()
        bryan = FaceEncoder(cam).start()
        
        not_captured = True
        while not_captured:
            img = cam.read()
            
            encoded_faces = bryan.get_encoded_faces()
            for encoded_face in encoded_faces:
                not_captured = False
                path = "known_face/"+name.replace(" ", "_")+".txt"
                with open(path, 'w') as f:
                    f.write(",".join(list(map(str, encoded_face)))) #save encode
                cv2.waitKey(100);
                print("Image captured")
            cv2.imshow("Face",img)
            cv2.waitKey(1)
            
        cam.stop()
        bryan.stop()
        cv2.destroyAllWindows()

        # Write matrix, locker_no, and name into database
        matrix_file = open(path, "r")
        locker_no = random.randint(1, 4)
        regis_info = {
            'name': name,
            'locker_no': locker_no,
            'matrix': str(matrix_file.read())
        }
        self.DB.insert_people(regis_info)
        return regis_info

    def face_check(self):
        threshold = 0.35 # if >= threshold: face match; else: face not match
        print("Starting camera...")
        time.sleep(1)
        cam = WebcamVideoStream().start()
        bryan = FaceEncoder(cam).start()
        encoded_registered_faces, names = self.get_registered_image()
        unknow_count = 0
        while True:
            img = cam.read()
            encoded_faces, bounds = bryan.get_encoded_faces_and_bounds()
            
            for bound, encoded_face in zip(bounds, encoded_faces):
                distance = self.get_distance(encoded_registered_faces, encoded_face)
                #################
                if distance == -1:
                    cam.stop()
                    bryan.stop()
                    cv2.destroyAllWindows()
                    self.trigger_alarm()
                    return "Unknown"
                else:
                    pass
                ################
                print(distance)
                if min(distance) <= threshold:
                    index = distance.index(min(distance))
                    name = names[index]
                    y1, x2, y2, x1 = bound
                    cv2.rectangle(img, (x1, y1), (x2, y2), (0,255,0), 5)
                    print(name)
                    self.ser.write(bytes(str(index), "utf-8"))
                    cam.stop()
                    bryan.stop()
                    cv2.destroyAllWindows()
                    return name
                else:
                    if unknow_count > 100:
                        self.ser.write(bytes(str(4), "utf-8"))
                        cam.stop()
                        bryan.stop()
                        self.trigger_alarm()
                        cv2.destroyAllWindows()
                        return name
                    name = "Unknown"
                    print(name)
                    unknow_count += 1
                    
            cv2.imshow('Webcam', img)
            if cv2.waitKey(1) == ord("q"):
                break
        
        cam.stop()
        bryan.stop()
        cv2.destroyAllWindows()

    def get_members_info(self):
        data_from_db = self.DB.get_members_info()
        return data_from_db
    
    def get_locker_no(self, name):
        return self.DB.get_locker_no(name)

    def verify_admin_login(self, login_info):
        username_inp = login_info['username']
        pswd_inp = login_info['password']

        pswd_from_db = self.DB.get_admin_password(username_inp)
        if pswd_inp == pswd_from_db:
            return 1
        else:
            return -1
    
    def update_member(self, update_info):
        name = update_info['member_name']
        locker_no = update_info['locker_no']
        self.DB.update_members_info(update_info)
        locker_no_from_db = self.DB.get_locker_no(name)
        if int(locker_no) == locker_no_from_db:
            return 1
        else:
            return -1
    
    def delete_member(self, member_name):
        self.DB.delete_member(member_name)
        del_state = self.DB.get_member(member_name)
        filepath = "known_face/"+str(member_name)+".txt"
        if not del_state:
            if os.path.isfile(filepath):
                os.remove(filepath)
                print("File has been removed.")
                return 1
            else:
                return -1
        else:
            print("Deletion failed")
            return -1
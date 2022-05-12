# Smart Locker System
Smart locker system that can detect user through the face using arduino and raspberry pi
![image](https://user-images.githubusercontent.com/82359659/168004867-bef4feb9-e7b5-4b6d-a42f-1b40bcc432c0.png)
![image](https://user-images.githubusercontent.com/82359659/168004885-8bd5e95e-32d1-4020-8802-8d081279a5a1.png)
![image](https://user-images.githubusercontent.com/82359659/168004952-3b9744ac-d8bd-48be-86be-031a52890728.png)
![image](https://user-images.githubusercontent.com/82359659/168004963-c483ef62-1ccb-4dc9-8d1a-f5683d426a0e.png)
![image](https://user-images.githubusercontent.com/82359659/168004976-f8232ffe-fe29-4ea3-a809-ebfbc890e76b.png)
![image](https://user-images.githubusercontent.com/82359659/168004980-eb151213-c99a-44de-9728-988613569293.png)

Sensors used:
- Raspberry Camera Module
- Ultrasonic sensor

Actuator used:
- LED Monitor
- Servo
- Buzzer

Woekflow:
First, all lockers are closed, then if there is someone standing in front of the locker with a distance of <= 20 cm, the camera will turn on and recognize that person with face recognition. If that person is not registered in the database, a buzzer will sound to call the security, while if that person is registered, a certain locker (servo) key will be opened automatically according to the locker registered as belonging to that person. After the user takes or puts things away and moves away from the locker, the locker lock (servo) will automatically close again.

Trained Model Source:
https://github.com/davisking/dlib-models

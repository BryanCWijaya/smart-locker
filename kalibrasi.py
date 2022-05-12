from statistics import mode
import numpy as np
from sklearn.linear_model import LinearRegression

# Data yang sudah diambil
# sebenarnya =  [0, 3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36, 39, 42, 45, 48, 51, 54, 57, 60]
# dibaca_sensor = [0.0001343941688537597, 0.0002694129943847656, 0.00037026405334472656, 0.0005681514739990234, 0.0007414817810058594, 0.0008809566497802734, 0.0010831356048583984, 0.0012638568878173828, 0.0014281272888183594, 0.0015568733215332031, 0.0018200874328613281, 0.002017498016357422, 0.002185821533203125, 0.0024056434631347656, 0.0025463104248046875, 0.0026209354400634766, 0.002784252166748047, 0.002988100051879883, 0.003111124038696289, 0.0033822059631347656, 0.003408670425415039]
sebenarnya =  [59, 61, 10, 10, 10, 8, 13, 10, 15, 26, 28, 32, 39, 102, 184, 32, 24, 19, 22]
dibaca_sensor = [3501.0, 3594.0, 632.0, 613.0, 625.0, 485.0, 807.0, 618.0, 894.0, 1558.0, 1702.0, 1886.0, 2335.0, 6034.0, 10863.0, 1911.0, 1442.0, 1127.0, 
1311.0]

class Kalibrasi_sensor_jarak():
    def __init__(self,jarak_sebenarnya = sebenarnya,dibaca_sensor=dibaca_sensor):
        self.X = None
        self.Y = None
        self.coef = None
        self.intercept =  None
        self.new_calibration(jarak_sebenarnya,dibaca_sensor)

    def new_calibration(self,jarak_sebenarnya,dibaca_sensor):
        self.X = np.array(dibaca_sensor).reshape((-1, 1))
        self.Y = np.array(jarak_sebenarnya)
        model = LinearRegression().fit(self.X,self.Y) 

        self.coef = np.mean(model.coef_)
        self.intercept =  model.intercept_
        print(f"Rumus: f(x)= {self.coef}x + {self.intercept}")
        
    def calculate(self,x):
        result = self.coef * x + self.intercept
        return round(result,3) 

a = Kalibrasi_sensor_jarak()
print(a.calculate(1311.0))



"""
3501.0
3594.0
632.0
613.0
625.0
485.0
807.0
618.0
894.0
1558.0
1702.0
1886.0
2335.0
6034.0
10863.0
1911.0
1442.0
1127.0
1311.0

59
61
10
10
10
8
13
10
15
26
28
32
39
102
184
32
24
19
22
"""
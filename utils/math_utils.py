import math
import numpy as np

'''
iki nokta arasındaki uzaklık hesabı için örnek algoritma

p1 = np.random.randint(0, 100, size=2)
p2 = np.random.randint(0, 100, size=2)

x1, y1 = p1
x2, y2 = p2

distance = math.sqrt((x2-x1)**2 + (y2-y1)**2)

print(f"x1 ve x2: ",x1,x2)
print(f"y1 ve y2: ",y1,y2)
print(f"Mesafe: ", distance)
'''
class myMath:
    # İki nokta arasındaki uzaklığın hesabını yapan fonksiyon
    def calc_distance(p1, p2):
        x1, y1 = p1
        x2, y2 = p2
        distance = math.sqrt((x2-x1)**2 + (y2-y1)**2)
        return distance
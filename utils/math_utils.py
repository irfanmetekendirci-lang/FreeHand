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


    @staticmethod
    def aci_hesapla(a, b, c):
        """
        Üç nokta (a, b, c) arasındaki 3D açıyı hesaplar.
        b noktası merkez (köşe/bükülme) noktasıdır.
        """
        a = np.array(a)
        b = np.array(b)
        c = np.array(c)

        ba = a - b      # b merkez noktasından a ve c'ye giden vektörler
        bc = c - b

        # İki vektörü skaler çarpıyoruz
        dot_product = np.dot(ba, bc)
        norm_ba = np.linalg.norm(ba)
        norm_bc = np.linalg.norm(bc)

        # Sıfıra bölünme koruması
        if norm_ba * norm_bc == 0:
            return 0.0

        # Kosinüs değerini hesaplayıp [-1.0, 1.0] aralığına kırpıyoruz
        cosine_angle = dot_product / (norm_ba * norm_bc)
        cosine_angle = np.clip(cosine_angle, -1.0, 1.0)
        
        angle = np.degrees(np.arccos(cosine_angle))

        return angle



    # Parmakların Bükülme Noktalarındaki Açıların Hesabı
    @staticmethod
    def calc_handAngel(landmarks):
        """
        MediaPipe'ın 21 landmark noktasından 14 temel parmak bükülme açısını çıkarır.
        """
        pts = [[lm.x, lm.y, lm.z] for lm in landmarks]    # Bize 21 noktanında x, y, z koordinatlarını tutar / pts[1] başparmak kök eklemini verir

        angels = [
            # Başparmak için iki tane bükülme vardır çünkü başparmağın kökü bileğe (pts[0]) bağlı değildir
                    myMath.aci_hesapla(pts[1], pts[2], pts[3]),
                    myMath.aci_hesapla(pts[2], pts[3], pts[4]),
            
                    # İşaret Parmağı (3 Açı)
                    myMath.aci_hesapla(pts[0], pts[5], pts[6]),
                    myMath.aci_hesapla(pts[5], pts[6], pts[7]),
                    myMath.aci_hesapla(pts[6], pts[7], pts[8]),
                    
                    # Orta Parmak (3 Açı)
                    myMath.aci_hesapla(pts[0], pts[9], pts[10]),
                    myMath.aci_hesapla(pts[9], pts[10], pts[11]),
                    myMath.aci_hesapla(pts[10], pts[11], pts[12]),
                    
                    # Yüzük Parmağı (3 Açı)
                    myMath.aci_hesapla(pts[0], pts[13], pts[14]),
                    myMath.aci_hesapla(pts[13], pts[14], pts[15]),
                    myMath.aci_hesapla(pts[14], pts[15], pts[16]),
                    
                    # Serçe Parmak (3 Açı)
                    myMath.aci_hesapla(pts[0], pts[17], pts[18]),
                    myMath.aci_hesapla(pts[17], pts[18], pts[19]),
                    myMath.aci_hesapla(pts[18], pts[19], pts[20])
        ]

        return angels
import cv2
import config
from utils.hand_tracking import HandDetector        # El tespiti sınıfını içe aktarıyoruz.
from utils.mouse_control import MouseController     # Mouse kontrolü için sınıfımızı içe aktarıyoruz.
from utils.math_utils import myMath                 # Tıklama için uzaklık hesabı yapan fonksiyonu çağıralım.

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, config.CAM_WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, config.CAM_HEIGHT)

print("Kamera başlatıldı. Çıkış için 'q' tuşuna basın.")

# HandDetactor classımızdan nesnemizi oluşturalım.
detector = HandDetector()

# MouseController classımızdan nesnemizi oluşturalım.
mouse_ctrl = MouseController()

# Oluşturduğumuz kameranın açık kalması için "While loop":
while True:
    success, frame = cap.read()
    if not success:
        print("Kamera görüntüsü alınamadı!")

    frame = cv2.flip(frame, 1)

    h, w, c = frame.shape  # Yükseklik ve genişliği al.

     # Çizeceğimiz dikdörtgenin başlanfıç ve bitiş koordinatlarını veriyoruz. (150,150) - (w-150, h-150)
    cv2.rectangle(frame, (config.FRAME_REDUCTION, config.FRAME_REDUCTION), (w-config.FRAME_REDUCTION, h-config.FRAME_REDUCTION),
                    (255, 0, 255),  2 # Renk ve Kalınlık
                )

    frame = detector.findHands(frame)           # Görüntüdeki elleri bulur ve ekleme noktalarını çizer.
    lm_list = detector.findPosition(frame)      # Tespit edilen elin 21 eklem noktasının piksel koordinatlarını döner.

    # Sadece el VARSA hareket ve tıklama mantığını çalıştır
    if len(lm_list) != 0:

        x1, y1 = lm_list[8][1], lm_list[8][2]       # işaret parmağı koordinatları (x, y)
        x2, y2 = lm_list[4][1], lm_list[4][2]       # Baş parmak koordinatları (x, y)
        x3, y3 = lm_list[12][1], lm_list[12][2]     # Orta Parmak koordinatları (x, y)
        x4, y4 = lm_list[16][1], lm_list[16][2]     # Yüzük parmağı koordinatları (x, y)

        mouse_ctrl.move_cursor(x1, y1)                      # move_cursor kameran alınan ham x ve y koordinatlarını bounding boxa oranlar ve imleci kaydırır.
        
       # Mesafeleri hesapla
        dist_index = myMath.calc_distance((x1, y1), (x2, y2))   # İşaret - Başparmak
        dist_middle = myMath.calc_distance((x3, y3), (x2, y2))  # Orta - Başparmak
        dist_ring = myMath.calc_distance((x4, y4), (x2, y2))    # Sağ Tık için

        # İki mesafeyi de kontrole gönder
        mouse_ctrl.check_click(dist_index, dist_middle, dist_ring)

    cv2.imshow('frame', frame)

    keyQuit = cv2.waitKey(1) # akıcı görüntü için 1 yapıyoruz, 1ms'de bir yenileniyor.

    if keyQuit == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
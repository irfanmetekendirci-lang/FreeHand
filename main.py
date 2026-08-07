import cv2
import config
from utils.hand_tracking import HandDetector        # El tespiti sınıfını içe aktarıyoruz

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, config.CAM_WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, config.CAM_HEIGHT)

print("Kamera başlatıldı. Çıkış için 'q' tuşuna basın.")

# HandDetactor classımızdan nesen oluşturalım
detector = HandDetector()

# Oluşturduğumuz kameranın açık kalması için "While loop":

while True:
    success, frame = cap.read()
    if not success:
        print("Kamera görüntüsü alınamadı!")

    frame = cv2.flip(frame, 1)

    h, w, c = frame.shape  # Yükseklik ve genişliği al

    frame = detector.findHands(frame)
    lm_list = detector.findPosition(frame)

    # Çizeceğimiz dikdörtgenin başlanfıç ve bitiş koordinatlarını veriyoruz (150,150) - (w-150, h-150)
    cv2.rectangle(frame, (config.FRAME_REDUCTION, config.FRAME_REDUCTION), (w-config.FRAME_REDUCTION, h-config.FRAME_REDUCTION),
                    (255, 0, 255),  2 # Renk ve Kalınlık
                )

    cv2.imshow('frame', frame)

    keyQuit = cv2.waitKey(1) # akıcı görüntü için 1 yapıyoruz, 1ms'de bir yenileniyor 

    if keyQuit == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
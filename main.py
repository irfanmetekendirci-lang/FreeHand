import cv2
import config
from utils.hand_tracking import HandDetector        # El tespiti sınıfını içe aktarıyoruz
from utils.mouse_control import MouseController     # Mouse kontrolü için sınıfımızı içe aktarıyoruz

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, config.CAM_WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, config.CAM_HEIGHT)

print("Kamera başlatıldı. Çıkış için 'q' tuşuna basın.")

# HandDetactor classımızdan nesnemizi oluşturalım
detector = HandDetector()

# MouseController classımızdan nesnemizi oluşturalım
mouse_ctrl = MouseController()

# Oluşturduğumuz kameranın açık kalması için "While loop":
while True:
    success, frame = cap.read()
    if not success:
        print("Kamera görüntüsü alınamadı!")

    frame = cv2.flip(frame, 1)

    h, w, c = frame.shape  # Yükseklik ve genişliği al

    frame = detector.findHands(frame)           # Görüntüdeki elleri bulur ve ekleme noktalarını çizer.
    lm_list = detector.findPosition(frame)      # Tespit edilen elin 21 eklem noktasının piksel koordinatlarını döner.

    # Algılanan elin işaret parmağının ucunu ilgili fonksiyona gönderiyoruz
    if len(lm_list) != 0:
        x, y = lm_list[8][1], lm_list[8][2]
        mouse_ctrl.move_cursor(x, y)            # move_cursor kameran alınan ham x ve y koordinatlarını bounding boxa oranlar ve imleci kaydırır.

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
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
    if len(lm_list) != 0 and detector.results.multi_hand_landmarks:
        
        hand_landmarks = detector.results.multi_hand_landmarks[0]
        fingers = detector.fingersUp(hand_landmarks.landmark)

        # Takip Noktası: ID 9 (Elin tam merkezi / orta parmak kökü)
        # Bu nokta elini yumruk da yapsan, açsan da asla titremez!
        x_center, y_center = lm_list[9][1], lm_list[9][2]

        # 1. HAREKET KURALI:
        # El açıkken GEZER, Yumruk yapıp sürüklerken de İMLEÇLE BİRLİKTE TAŞIR!
        # Sadece tek tık / sağ tık anında imleci dondurur.
        if fingers == [1, 1, 1, 1, 1] or (fingers[1] == 1 and fingers[2] == 1) or mouse_ctrl.is_dragging:
            mouse_ctrl.move_cursor(x_center, y_center)

        # 2. TIKLAMA VE SÜRÜKLEME KONTROLÜ
        mouse_ctrl.check_click(fingers)

    cv2.imshow('frame', frame)

    keyQuit = cv2.waitKey(1) # akıcı görüntü için 1 yapıyoruz, 1ms'de bir yenileniyor.

    if keyQuit == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
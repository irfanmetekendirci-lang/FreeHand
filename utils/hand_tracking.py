import cv2
import mediapipe as mp
from utils.math_utils import myMath

class HandDetector:
    def __init__(self, max_hands=1, detection_con=0.7, tracking_con=0.7):
        self.mp_hands = mp.solutions.hands
        self.mp_draw = mp.solutions.drawing_utils  # Değişken adı sabitlendi
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=max_hands,
            min_detection_confidence=detection_con,
            min_tracking_confidence=tracking_con
        )

    def findHands(self, img, draw=True):
        """Görüntüdeki elleri bulur ve ekleme noktalarını çizer."""
        # NOT: Aynalama (flip) işlemini main.py içinde yapmak en temizidir.
        # Görüntüyü MediaPipe için RGB formatına çeviriyoruz
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(img_rgb)

        if self.results.multi_hand_landmarks and draw:
            for hand_landmarks in self.results.multi_hand_landmarks:
                # self.mp_draw kullanılarak hata düzeltildi
                self.mp_draw.draw_landmarks(
                    img, hand_landmarks, self.mp_hands.HAND_CONNECTIONS
                )
        return img

    def findPosition(self, img):
        """Tespit edilen elin 21 eklem noktasının piksel koordinatlarını döner."""
        lm_list = []
        if self.results.multi_hand_landmarks:
            my_hand = self.results.multi_hand_landmarks[0]
            h, w, c = img.shape
            for id, lm in enumerate(my_hand.landmark):
                cx, cy = int(lm.x * w), int(lm.y * h)
                lm_list.append([id, cx, cy])
        return lm_list

    def fingersUp(self, landmarks):
        """
        MediaPipe'tan gelen el landmarks nesnesini alır.
        myMath.calc_handAngel ile hesaplanan eklem açılarına göre 
        5 parmağın açık (1) veya kapalı (0) olma durumunu liste olarak döner.
        """
        # 14 açıyı myMath sınıfından çekiyoruz
        angels = myMath.calc_handAngel(landmarks)

        fingers = []

        # 1. Başparmak
        if angels[1] > 160:
            fingers.append(1)
        else:
            fingers.append(0)

        # 2. İşaret Parmağı
        if angels[3] > 160:
            fingers.append(1)
        else:
            fingers.append(0)

        # 3. Orta Parmak
        if angels[6] > 160:
            fingers.append(1)
        else:
            fingers.append(0)

        # 4. Yüzük Parmağı
        if angels[9] > 160:
            fingers.append(1)
        else:
            fingers.append(0)

        # 5. Serçe Parmak
        if angels[12] > 160:
            fingers.append(1)
        else:
            fingers.append(0)

        return fingers
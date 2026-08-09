from pynput import mouse
import pyautogui
import numpy as np
import config
import smoothing

class MouseController:
    """
    Kameradan gelen parmak koordinatlarını monitör çözünürlüğüne oranlayan,
    titreşimleri yumuşatan ve fiziksel fare imlecini hareket ettiren sınıf.
    """
    def __init__(self):
        # 1. Monitörün piksel genişlik ve yüksekliğini alıyoruz (Örn: 1920x1080)
        self.screen_width, self.screen_height = pyautogui.size()
        print(f"Ekran Çözünürlüğü: {self.screen_width}x{self.screen_height}")

        # 2. Yumuşatma (Lerp) algoritması için bir önceki karedeki (frame) imleç konumlarını tutuyoruz
        self.prev_x, self.prev_y = 0, 0

        # 3. İşletim sistemi seviyesinde fare kontrolü sağlayan pynput nesnesi
        self.myMouse = mouse.Controller()

    def move_cursor(self, raw_x, raw_y):
        """
        Kameradan gelen ham parmak koordinatlarını (raw_x, raw_y) alır,
        Bounding Box (mor kutu) sınırlarına göre ekran boyutuna oranlar ve imleci kaydırır.
        """
        # ADIM 1: ORANLAMA (MAPPING / INTERPOLATION)
        # Kameradaki ham parmak konumunu, mor kutu (FRAME_REDUCTION) sınırlarını baz alarak
        # bilgisayar ekranının piksel boyutlarına (0 -> screen_width/height) oranlıyoruz.
        self.hedef_x = np.interp(
            raw_x, 
            [config.FRAME_REDUCTION, config.CAM_WIDTH - config.FRAME_REDUCTION], 
            [0, self.screen_width]
        )
        self.hedef_y = np.interp(
            raw_y, 
            [config.FRAME_REDUCTION, config.CAM_HEIGHT - config.FRAME_REDUCTION], 
            [0, self.screen_height]
        )

        # ADIM 2: YUMUŞATMA (SMOOTHING / LERP)
        # El titreşimlerini engellemek için önceki konum ile yeni hedef konum arasında
        # SMOOTH_FACTOR oranında yumuşak bir süzülme hesaplıyoruz.
        self.smooth_x, self.smooth_y = smoothing.smooth_location(
            self.prev_x, self.prev_y, 
            self.hedef_x, self.hedef_y, 
            config.SMOOTH_FACTOR
        )

        # ADIM 3: İMLECİ TAŞIMA
        # Hesaptaki yeni yumuşatılmış koordinatları pynput ile işletim sisteminin faresine uyguluyoruz.
        self.myMouse.position = (self.smooth_x, self.smooth_y)

        # ADIM 4: HAFIZA GÜNCELLEME
        # Bir sonraki kamera karesinde (frame) Lerp hesabı yapabilmek için mevcut konumu "geçmiş" olarak kaydediyoruz.
        self.prev_x, self.prev_y = self.smooth_x, self.smooth_y
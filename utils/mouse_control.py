from pynput import mouse
import pyautogui
import numpy as np
import config
from utils import smoothing

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

        # Tıklama bayrağı (Seri tıklamayı engellemek için)
        self.is_clicked = False


    def move_cursor(self, raw_x, raw_y):
        """
        Kameradan gelen ham parmak koordinatlarını (raw_x, raw_y) alır,
        Bounding Box (mor kutu) sınırlarına göre ekran boyutuna oranlar ve imleci kaydırır.
        """

        # Eğer o an tık yapılmışsa imlecin kaymasını engellemek için hareketi donduruyoruz (sonradan eklendi 4.faz)
        if self.is_clicked:
            return

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



    def check_click(self, dist_index, dist_middle, dist_ring):
        """
        İşaret, orta ve yüzük parmaklarının başparmağa olan mesafelerini alır.
        Mesafeler eşiğin altındaysa ilgili tıklama eylemini gerçekleştirir.
        """
        # 1. ÇİFT TIK: Orta parmak başparmağa yakınsa
        if dist_middle <= config.CLICK_THRESHOLD and not self.is_clicked:
            self.myMouse.click(mouse.Button.left, 2)
            self.is_clicked = True
            print("Çift Tık Yapıldı!")

        # 2. SOL TIK: İşaret parmağı başparmağa yakınsa
        elif dist_index <= config.CLICK_THRESHOLD and not self.is_clicked:
            self.myMouse.click(mouse.Button.left, 1)
            self.is_clicked = True
            print("Sol Tık Yapıldı!")

        # 3. SAĞ TIK: Yüzük parmağı yakınsa VE işaret parmağı açıksa (Tetiklenme koruması)
        elif dist_ring <= (config.CLICK_THRESHOLD - 5) and dist_index > (config.CLICK_THRESHOLD + 15) and not self.is_clicked:
            self.myMouse.click(mouse.Button.right, 1)
            self.is_clicked = True
            print("Sağ Tık Yapıldı!")

        # 4. BIRAKMA (RELEASE): Tüm parmaklar açıldıysa kilidi kaldır
        elif (dist_index > (config.CLICK_THRESHOLD + 10) and 
              dist_middle > (config.CLICK_THRESHOLD + 10) and 
              dist_ring > (config.CLICK_THRESHOLD + 10)):
            self.is_clicked = False
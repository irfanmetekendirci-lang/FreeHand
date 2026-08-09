from pynput import mouse
import pyautogui
import numpy as np

class MouseContreller():
    def __init__(self):
        # 1. Ekran boyutlarını alıp self değişkenlerine atıyoruz
        self.screen_width, self.screen_height = pyautogui.size()
        print(f"Screen Width: ",self.screen_width,"Screen Height: ",self.screen_height)

        # 2. Önceki konumları 0 olarak başlatıyoruz
        self.prev_x, self.prev_y = 0

        # 3. pynput Mouse nesnesini başlatıyoruz
        self.myMouse = mouse.Controller()


    def move_cursor(self, raw_x, raw_y):

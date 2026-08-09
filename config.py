# ----- KAMERA AYARLARI -----
CAM_WIDTH = 1280
CAM_HEIGHT = 720
FRAME_REDUCTION = 150 # Bounding Box (Etkin Alan) kenar payı (piksel) (kesinti miktarı)

# ----- TIKLAMA VE HAREKET EŞİKLERİ (THRESHOLD) -----
        # --- Piksel Cinsinden Mesafe ---
CLICK_THRESHOLD = 35
SCROLL_THRESHOLD = 30
ZOOM_THRESHOLD = 40

# ----- İMLEÇ YUMUŞATMA KATSAYISI (LERP) -----
# 0 ile 1 arası: Küçük değerler daha pürüzsüz ama daha yavaş, büyük değerler daha hızlı ama titrek olur.
SMOOTH_FACTOR = 0.25
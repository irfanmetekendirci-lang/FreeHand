# FreeHand: AI-Powered Contactless Hand Gesture Controller 🖐️🖱️

FreeHand, tek bir RGB web kamerası kullanarak el hareketlerini ve eklem bükülme açılarını gerçek zamanlı analiz eden, temassız bir sanal fare ve jest kontrol sistemidir.

Proje; klasik 2D piksel mesafesi yaklaşımlarının aksine, **3D vektörel eklem açıları (Euler/Dot Product)** ve **doğrusal enterpolasyonlu yumuşatma (Lerp)** algoritmaları kullanarak kararlı bir kontrol mimarisi sunar.

---

## 🚀 Temel Özellikler

- **3D Vektörel Açı Tabanlı Karar Mekanizması:** MediaPipe 3D landmark noktalarından vektörler çıkarılarak 14 temel eklem açısı `np.arccos` ve skaler çarpım (`dot product`) ile hesaplanır.
- **Lerp (Linear Interpolation) Filtreleme:** El titreşimlerini sönümlemek ve imleç akışını pürüzsüzleştirmek için doğrusal enterpolasyon uygulanır.
- **Merkezi Eklem Takibi (MCP Anchoring):** İmleç koordinatı parmak ucundan değil, el ayasından (Landmark 9) referans alınarak tıklama/bükülme esnasındaki imleç kaymaları önlenir.
- **Modüler Mimari:** Matematiksel hesaplar, el tespiti, konfigürasyon ve fare kontrol katmanları bağımsız modüllere ayrılmıştır.

---

## 🖐️ Jest ve Kontrol Tablosu

| Jest | Durum / Parmaklar | Eylem |
| :--- | :--- | :--- |
| **Gezinme (İmleç)** | Bütün El Açık / İşaret Dik | İmleç ekran koordinatlarına oranlanarak pürüzsüzce gezinir. |
| **Sol Tık** | İşaret Parmağı Bükülü (Tetik Hareketi) | Tek sol tıklama gerçekleştirir. |
| **Sağ Tık** | Orta Parmak Bükülü | Sağ tıklama menüsünü açar. |
| **Sürükle & Bırak** | Yumruk (`[0, 0, 0, 0, 0]`) $\rightarrow$ El Açma | Yumruk yapıldığında sol tık basılı tutulur (`MouseDown`), el açıldığında bırakılır (`MouseUp`). |

---

## 📁 Proje Mimarisi

```text
FreeHand/
│
├── utils/
│   ├── hand_tracking.py   # MediaPipe el tespiti ve 14-açı çıkarımı
│   ├── math_utils.py      # Vektörel açı ve Öklid mesafe hesaplayıcıları
│   ├── mouse_control.py   # pynput ve durum bazlı fare kontrolcüsü
│   └── smoothing.py       # Lerp tabanlı imleç yumuşatma algoritması
│
├── config.py              # Çözünürlük, eşik ve katsayı parametreleri
├── main.py                # Gerçek zamanlı kamera döngüsü ve orkestrasyon
├── requirements.txt       # Bağımlılıklar
└── README.md              # Proje dokümantasyonu
```

---

## 🛠️ Kurulum ve Çalıştırma

### 1. Repoyu Klonlayın
```bash
git clone [https://github.com/KULLANICI_ADIN/FreeHand.git](https://github.com/KULLANICI_ADIN/FreeHand.git)
cd FreeHand
```

### 2. Bağımlılıkları Yükleyin
```bash
pip install -r requirements.txt
```

### 3. Uygulamayı Başlatın
```bash
python main.py
```

> **Not:** Çıkış yapmak için kamera penceresi seçiliyken klavyeden **`q`** tuşuna basabilirsiniz.
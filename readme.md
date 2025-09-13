
````markdown
# Hand Gesture Recognition dengan Suara

Program ini menggunakan **MediaPipe** untuk mendeteksi gesture tangan dan **gTTS + Pygame** untuk mengeluarkan suara sesuai gesture. Semua audio disimpan di folder `audio/`.

## Fitur
- Deteksi gesture tangan: Halo, Perkenalkan, Nama saya, Fathan Jamil, Aku, Dan, Kamu, Cinta.
- Mengeluarkan suara sesuai gesture.
- Semua audio disimpan di folder `audio/`.

## Daftar Gesture

| Gesture        | Posisi Jari                                                                 |
|----------------|----------------------------------------------------------------------------|
| Halo           | Semua jari terbuka                                                          |
| Perkenalkan    | Telunjuk + tengah terbuka, jari lain tertutup                               |
| Nama saya      | Hanya telunjuk terbuka                                                     |
| Fathan Jamil   | Jempol + kelingking terbuka, jari lain tertutup                             |
| Aku            | Hanya telunjuk terbuka, arah tangan ke kiri                                 |
| Dan            | Tengah + manis terbuka, jari lain tertutup                                  |
| Kamu           | Telunjuk + tengah + manis terbuka, jempol + kelingking tertutup             |
| Cinta          | Jempol + kelingking terbuka atau semua jari terbuka                         |

## Persiapan
Pastikan **Python >= 3.8** sudah terinstall dan pip tersedia.

## Instalasi
1. Clone repository:
```bash
git clone https://github.com/username/hand-gesture-sound.git
cd hand-gesture-sound
````

2. Install dependencies:

```bash
pip install opencv-python mediapipe pygame gTTS
```

3. Jalankan program:

```bash
python hand_gesture.py
```

## Penggunaan

1. Program akan membuka kamera.
2. Tunjukkan gesture tangan sesuai tabel di atas.
3. Nama gesture akan muncul di layar dan suara akan dimainkan.
4. Tekan `q` untuk keluar dari program.

## Struktur Folder

```
hand-gesture-sound/
│
├─ audio/         # Semua file mp3 hasil generate TTS
├─ hand_gesture.py
└─ README.md
```

## Catatan

* Audio akan otomatis dibuat saat pertama kali program dijalankan jika belum ada.
* Pastikan kamera dapat diakses.
* Program hanya mendukung **satu tangan**.
* Pastikan gesture sesuai posisi jari pada tabel untuk hasil akurat.

`

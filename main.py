import cv2
import mediapipe as mp
import os
import time
import pygame
from gtts import gTTS

pygame.mixer.init()

# Folder untuk menyimpan audio
audio_folder = "audio"
os.makedirs(audio_folder, exist_ok=True)

voices = {
    "Halo": "halo.mp3",
    "Perkenalkan": "perkenalkan.mp3",
    "Nama saya": "nama_saya.mp3",
    "Fathan Jamil": "fathan_jamil.mp3",
    "Aku": "aku.mp3",
    "Dan": "dan.mp3",
    "Kamu": "kamu.mp3",
    "Cinta": "cinta.mp3"
}

for text, file in voices.items():
    file_path = os.path.join(audio_folder, file)
    if not os.path.exists(file_path):
        tts = gTTS(text=text, lang="id")
        tts.save(file_path)
    voices[text] = file_path 

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

last_gesture = None
last_time = 0
cooldown = 2

def speak(file):
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.stop()
    pygame.mixer.music.load(file)
    pygame.mixer.music.play()

def stop_speak():
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.stop()

def finger_status(hand_landmarks):
    landmarks = hand_landmarks.landmark
    status = []

    status.append(landmarks[mp_hands.HandLandmark.THUMB_TIP].x <
                  landmarks[mp_hands.HandLandmark.THUMB_IP].x)

    finger_tips = [
        mp_hands.HandLandmark.INDEX_FINGER_TIP,
        mp_hands.HandLandmark.MIDDLE_FINGER_TIP,
        mp_hands.HandLandmark.RING_FINGER_TIP,
        mp_hands.HandLandmark.PINKY_TIP
    ]
    finger_pips = [
        mp_hands.HandLandmark.INDEX_FINGER_PIP,
        mp_hands.HandLandmark.MIDDLE_FINGER_PIP,
        mp_hands.HandLandmark.RING_FINGER_PIP,
        mp_hands.HandLandmark.PINKY_PIP
    ]

    for tip, pip in zip(finger_tips, finger_pips):
        status.append(landmarks[tip].y < landmarks[pip].y - 0.02)

    return status, landmarks

def recognize_gesture(hand_landmarks):
    fingers, landmarks = finger_status(hand_landmarks)

    if all(fingers):
        return "Halo"
    if fingers[1] and fingers[2] and not (fingers[0] or fingers[3] or fingers[4]):
        return "Perkenalkan"
    if fingers[1] and not any([fingers[0], fingers[2], fingers[3], fingers[4]]):
        if landmarks[mp_hands.HandLandmark.INDEX_FINGER_TIP].x < 0.5:
            return "Aku"
        return "Nama saya"
    if fingers[0] and fingers[4] and not any([fingers[1], fingers[2], fingers[3]]):
        return "Fathan Jamil"
    if (fingers[0] and fingers[4]) or all(fingers):
        return "Cinta"
    if fingers[1] and fingers[2] and fingers[3] and not (fingers[0] or fingers[4]):
        return "Kamu"
    if fingers[2] and fingers[3] and not any([fingers[0], fingers[1], fingers[4]]):
        return "Dan"

    return None

def detect_hand_gesture(image, hand):
    global last_gesture, last_time
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hand.process(image_rgb)

    gesture = None
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            gesture = recognize_gesture(hand_landmarks)
            mp_draw.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    if gesture:
        cv2.putText(image, gesture, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        if gesture != last_gesture or time.time() - last_time > cooldown:
            last_gesture = gesture
            last_time = time.time()
            if gesture in voices:
                speak(voices[gesture])
    else:
        cv2.putText(image, "Tidak ada gesture", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        if last_gesture:
            stop_speak()
            last_gesture = None

    return image

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Tidak dapat membuka kamera")
    exit()

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    frame = detect_hand_gesture(frame, hands)
    cv2.imshow("Hand Gesture Recognition", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

stop_speak()
cap.release()
cv2.destroyAllWindows()

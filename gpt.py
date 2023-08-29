import cv2
import mediapipe as mp
import pyautogui
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Authenticate with the Spotify API
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="f480c149f90f4a209b90137fb927819f",
                                               client_secret="605e122713814a73a1d775c65a0cda27",
                                               redirect_uri="http://localhost:8000",
                                               scope="user-read-playback-state,user-modify-playback-state"))

# Set up Mediapipe for hand detection
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

cap = cv2.VideoCapture(0)
with mp_hands.Hands(min_detection_confidence=0.5) as hands:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            break

        # Convert the image from BGR to RGB
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Process the image with Mediapipe
        results = hands.process(image)

        # Check if any hands were detected
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Map hand landmarks to specific controls
                thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
                index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]

                # Play/Pause button
                if thumb_tip.y < index_finger_tip.y:
                    pyautogui.press('F8')

                # Skip track button
                elif thumb_tip.x > index_finger_tip.x:
                    sp.next_track()

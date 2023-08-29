import cv2
import mediapipe as mp
import datetime
import numpy as np
import pyautogui
import time
import spotipy
from spotipy.oauth2 import SpotifyOAuth

gest=0
prev=0
next=0
flag=0
# Authenticate with the Spotify API
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="**************",
                                               client_secret="*************",
                                               redirect_uri="http://localhost:8000",
                                               scope="user-read-playback-state,user-modify-playback-state"))
cap = cv2.VideoCapture(0)
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils
mp_holistic = mp.solutions.holistic.Holistic()
start_time=time.time()
while True:
    success, image = cap.read()
    imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(imageRGB)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            lmList=[]
            for id, lm in enumerate(handLms.landmark):
                h, w, c = image.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])

            thumb = handLms.landmark[mpHands.HandLandmark.THUMB_TIP]
            index = handLms.landmark[mpHands.HandLandmark.INDEX_FINGER_TIP]
            middle = handLms.landmark[mpHands.HandLandmark.MIDDLE_FINGER_TIP]
            ring = handLms.landmark[mpHands.HandLandmark.RING_FINGER_TIP]
            pinky = handLms.landmark[mpHands.HandLandmark.PINKY_TIP]
            wrist = handLms.landmark[mpHands.HandLandmark.WRIST]

            # Calculate the distances between each finger tip and the wrist
            thumb_distance = ((thumb.x - wrist.x) ** 2 + (thumb.y - wrist.y) ** 2) ** 0.5
            index_distance = ((index.x - wrist.x) ** 2 + (index.y - wrist.y) ** 2) ** 0.5
            middle_distance = ((middle.x - wrist.x) ** 2 + (middle.y - wrist.y) ** 2) ** 0.5
            ring_distance = ((ring.x - wrist.x) ** 2 + (ring.y - wrist.y) ** 2) ** 0.5
            pinky_distance = ((pinky.x - wrist.x) ** 2 + (pinky.y - wrist.y) ** 2) ** 0.5
            thumb_index_distance = ((thumb.x - index.x) ** 2 + (thumb.y - index.y) ** 2) ** 0.5

            angle = np.arctan2(thumb.y - index.y, thumb.x - index.x)
            angle = angle * 180 / np.pi

            thumbIsOpen = False
            indexIsOpen = False
            middelIsOpen = False
            ringIsOpen = False
            pinkyIsOpen = False
            handLandmarks=handLms.landmark
            pseudoFixKeyPoint = handLandmarks[2].x
            if handLandmarks[3].x < pseudoFixKeyPoint and handLandmarks[4].x < pseudoFixKeyPoint:
                thumbIsOpen = True

            pseudoFixKeyPoint = handLandmarks[6].y
            if handLandmarks[7].y < pseudoFixKeyPoint and handLandmarks[8].y < pseudoFixKeyPoint:
                indexIsOpen = True

            pseudoFixKeyPoint = handLandmarks[10].y
            if handLandmarks[11].y < pseudoFixKeyPoint and handLandmarks[12].y < pseudoFixKeyPoint:
                middelIsOpen = True

            pseudoFixKeyPoint = handLandmarks[14].y
            if handLandmarks[15].y < pseudoFixKeyPoint and handLandmarks[16].y < pseudoFixKeyPoint:
                ringIsOpen = True

            pseudoFixKeyPoint = handLandmarks[18].y

            if handLandmarks[19].y < pseudoFixKeyPoint and handLandmarks[20].y < pseudoFixKeyPoint:
                pinkyIsOpen = True
            if thumb_distance < 0.3 and index_distance < 0.3 and middle_distance < 0.3 and ring_distance < 0.3 and pinky_distance < 0.3:
                now = datetime.datetime.now()
                current_time = datetime.time(now.hour, now.minute, now.second)
                text = current_time.strftime('%H:%M:%S')
                font = cv2.FONT_HERSHEY_SIMPLEX
                org = (100, 100)
                fontScale = 1
                color = (255, 255, 255)
                thickness = 2
                print("Fist!!")
                # Create a black rectangle with white text
                cv2.rectangle(image, (80, 60), (280, 120), (0, 0, 0), -1)
                cv2.putText(image, text, org, font, fontScale, color, thickness)

            elif thumbIsOpen and indexIsOpen and not middelIsOpen and not ringIsOpen and pinkyIsOpen:
                if gest==0:
                    gest=1
                    start_time=time.time()
                    if flag==0:
                        sp.start_playback()
                        flag = 1
                    elif flag == 1:
                        flag = 0
                        sp.pause_playback()
                    print("Rock sign!")
                # elif angle > 60 and angle < 120:
                #     sp.previous_track()
                #     print("Thumbs up!")
                # elif angle < -60 and angle > -120:
                #     sp.next_track()
                #     print("Thumbs up!")
                else:
                    if(time.time() > start_time+1):
                        gest=0
            elif not thumbIsOpen and indexIsOpen and not middelIsOpen and not ringIsOpen and not pinkyIsOpen:
                if prev==0:
                    prev=1
                    flag=1
                    start_time=time.time()
                    sp.previous_track()
                    print("one sign!")
                else:
                    if(time.time() > start_time+1):
                        prev=0
            elif not thumbIsOpen and indexIsOpen and middelIsOpen and not ringIsOpen and not pinkyIsOpen:
                if next == 0:
                    next = 1
                    flag=1
                    start_time = time.time()
                    sp.next_track()
                    print("two sign!")
                else:
                    if (time.time() > start_time + 1):
                        next = 0

    cv2.imshow("Output", image)
    cv2.waitKey(1)

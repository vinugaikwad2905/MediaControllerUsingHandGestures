import cv2
import mediapipe as mp
import pyttsx3
import pyautogui as p

from google.protobuf.json_format import MessageToDict

mpHands = mp.solutions.hands
hands = mpHands.Hands(min_tracking_confidence = 0.75,max_num_hands = 2)
mpDraw = mp.solutions.drawing_utils

fingercoordinates = [(8,6),(12,10),(16,14),(20,18)]
thumbcoordinates = (4,2)

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voices',voices[0].id)

def speak(audio):
    engine.say(audio)
    print(audio)
    engine.runAndWait()

cap = cv2.VideoCapture(0)
cap.set(3,1920)
cap.set(4,1080)
Resume = 0
Pause = 0

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    multiLandMarks = results.multi_hand_landmarks
    if results.multi_hand_landmarks:
        handPoints = []
        for handLms in multiLandMarks:
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

            for idx, lm in enumerate(handLms.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                handPoints.append((cx, cy))

        for point in handPoints:
            cv2.circle(img, point, 10, (255, 0, 0))

        upCount = 0
        if len(results.multi_handedness) == 2:
            speak("Both hand are not allowed.")
        else:
            for i in results.multi_handedness:
                label = MessageToDict(i)['classification'][0]['label']

                if label == 'Left':
                    cv2.putText(img, label + ' Hand', (20, 50), cv2.FONT_HERSHEY_COMPLEX, 0.9, (0, 255, 0), 2)
                    for coordinate in fingercoordinates:
                        if handPoints[coordinate[0]][1] < handPoints[coordinate[1]][1]:
                            upCount += 1
                    if handPoints[thumbcoordinates[0]][0] > handPoints[thumbcoordinates[1]][0]:
                        upCount += 1
                    if upCount == 0:
                        if Resume == 0:
                            Resume = 1
                            p.press("space")
                            speak("Resum.")
                            Pause = 0
                        elif Resume == 1:
                            speak("Already Resumd.")
                    elif upCount == 5:
                        if Pause == 0:
                            Pause = 1
                            p.press("space")
                            Resume = 0
                            speak("Pause.")
                        elif Pause == 1:
                            speak("Already paused")
                    elif upCount == 1:
                        p.keyDown("ctrl")
                        p.press("up")
                        p.keyUp("ctrl")
                    elif upCount == 2:
                        p.keyDown("ctrl")
                        p.press("down")
                        p.keyUp("ctrl")
                    elif upCount == 3:
                        p.keyDown("ctrl")
                        p.press("left")
                        p.keyUp("ctrl")
                    elif upCount == 4:
                        p.keyDown("ctrl")
                        p.press("right")
                        p.keyUp("ctrl")
                    cv2.putText(img, str(upCount), (150, 150), cv2.FONT_HERSHEY_PLAIN, 12, (255, 128, 0), 12)

            if label == 'Right':
                    cv2.putText(img, label + ' Hand', (460, 50),cv2.FONT_HERSHEY_COMPLEX,0.9, (0, 255, 0), 2)
                    for coordinate in fingercoordinates:
                        if handPoints[coordinate[0]][1] < handPoints[coordinate[1]][1]:
                            upCount += 1
                    if handPoints[thumbcoordinates[0]][0] > handPoints[thumbcoordinates[1]][0]:
                       pass
                    else:
                        upCount+=1


                    if upCount == 0:
                        if Resume == 0:
                            Resume = 1
                            p.press("space")
                            speak("Resum.")
                            Pause = 0
                        elif Resume == 1:
                            speak("Already Resumd.")
                    elif upCount == 5:
                        if Pause == 0:
                            Pause = 1
                            p.press("space")
                            Resume = 0
                            speak("Pause.")
                        elif Pause == 1:
                            speak("Already paused")
                    elif upCount == 1:
                        p.keyDown("ctrl")
                        p.press("up")
                        p.keyUp("ctrl")
                    elif upCount == 2:
                        p.keyDown("ctrl")
                        p.press("down")
                        p.keyUp("ctrl")
                    elif upCount == 3:
                        p.keyDown("ctrl")
                        p.press("left")
                        p.keyUp("ctrl")
                    elif upCount == 4:
                        p.keyDown("ctrl")
                        p.press("right")
                        p.keyUp("ctrl")
                    cv2.putText(img, str(upCount), (150, 150), cv2.FONT_HERSHEY_PLAIN, 12, (255, 128, 0), 12)
    cv2.imshow('Image', img)
    if cv2.waitKey(1) & 0xff == ord('q'):
        break

import math
import time
from ctypes import cast, POINTER
import cv2
import mediapipe as mp
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

raisedFinger = ""
indexThresh = 100
midThresh = 100
ringThresh = 100
pinkyThresh = 100

indexOp = False
midOp = False
ringOp = False
pinkyOp = False

#BOJADGREATGREAT
def switch_tab(driverTab, finger_position):
    # Get the current window handle
    current_handle = driverTab.current_window_handle
    # Get all window handles
    all_handles = driverTab.window_handles

    # Switch tabs based on finger position
    if finger_position == "index":
        target_handle = all_handles[0]  # Switch to the first tab
    elif finger_position == "middle":
        target_handle = all_handles[1]  # Switch to the second tab
    elif finger_position == "ring":
        target_handle = all_handles[2]  # Switch to the third tab
    elif finger_position == "pinky":
        target_handle = all_handles[3]  # Switch to the fourth tab
    else:
        print("Invalid finger position")
        return

    # Switch to the target tab
    if target_handle != current_handle:
        driverTab.switch_to.window(target_handle)
        print("Switched to tab:", finger_position)
    else:
        print("Already on tab:", finger_position)


brave_path = "C:\Program Files\BraveSoftware\Brave-Browser\Application"  # Replace with the actual path to Brave executable
options = webdriver.ChromeOptions()
options.binary_location = brave_path
driver = webdriver.Chrome(options=options)

while True:
    status, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    multiRes = results.multi_hand_landmarks

    if multiRes:
        indexPoint = ()
        midPoint = ()
        ringPoint = ()
        pinkyPoint = ()
        wristPoint = ()

        for handLms in multiRes:
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

            for idHand, lm in enumerate(handLms.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)

                if idHand == 0:
                    wristPoint = (cx, cy)
                if idHand == 8:
                    indexPoint = (cx, cy)
                if idHand == 12:
                    midPoint = (cx, cy)
                if idHand == 16:
                    ringPoint = (cx, cy)
                if idHand == 20:
                    pinkyPoint = (cx, cy)

        cv2.circle(img, indexPoint, 15, (255, 255, 0), cv2.FILLED)
        cv2.circle(img, midPoint, 15, (255, 255, 0), cv2.FILLED)
        cv2.circle(img, ringPoint, 15, (255, 255, 0), cv2.FILLED)
        cv2.circle(img, pinkyPoint, 15, (255, 255, 0), cv2.FILLED)

        cv2.line(img, indexPoint, wristPoint, (255, 255, 0), 3)
        cv2.line(img, midPoint, wristPoint, (255, 255, 0), 3)
        cv2.line(img, ringPoint, wristPoint, (255, 255, 0), 3)
        cv2.line(img, pinkyPoint, wristPoint, (255, 255, 0), 3)

        indexLength = math.sqrt(((indexPoint[0] - wristPoint[0]) ** 2) + ((indexPoint[1] - wristPoint[1]) ** 2))
        midLength = math.sqrt(((midPoint[0] - wristPoint[0]) ** 2) + ((midPoint[1] - wristPoint[1]) ** 2))
        ringLength = math.sqrt(((ringPoint[0] - wristPoint[0]) ** 2) + ((ringPoint[1] - wristPoint[1]) ** 2))
        pinkyLength = math.sqrt(((pinkyPoint[0] - wristPoint[0]) ** 2) + ((pinkyPoint[1] - wristPoint[1]) ** 2))

        if (indexLength > indexThresh) and (midLength < midThresh) and (ringLength < ringThresh) and (
                pinkyLength < pinkyThresh):
            if not indexOp:
                indexOp = True
                driver.execute_script("window.open('https://www.google.com', '_blank')")
        elif (indexLength > indexThresh) and (midLength > midThresh) and (ringLength < ringThresh) and (
                pinkyLength < pinkyThresh):
            if not midOp:
                midOp = True
                driver.execute_script("window.open('https://www.facebook.com', '_blank')")
        elif (indexLength > indexThresh) and (midLength > midThresh) and (ringLength > ringThresh) and (
                pinkyLength < pinkyThresh):
            if not ringOp:
                ringOp = True
                driver.execute_script("window.open('https://www.youtube.com', '_blank')")
        elif (indexLength > indexThresh) and (midLength > midThresh) and (ringLength > ringThresh) and (
                pinkyLength > pinkyThresh):
            if not pinkyOp:
                pinkyOp = True
                driver.execute_script("window.open('https://www.youtube.com/watch?v=dQw4w9WgXcQ', '_blank')")
        else:
            indexOp = False
            midOp = False
            ringOp = False
            pinkyOp = False
            print("No Finger Raised")

    cv2.imshow("Browser Control", img)
    cv2.waitKey(1)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

hands.close()
cap.release()
cv2.destroyAllWindows()

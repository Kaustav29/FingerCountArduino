import cv2
import mediapipe as mp
import serial
import time

cap = cv2.VideoCapture(0)
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils
fingerCoordinates = [(8, 6), (12, 10), (16, 14), (20, 18)]
thumbCoordinates = (4, 2)

# Initialize serial communication with Arduino
ser = serial.Serial('COM3', 9600)  # Replace 'COM3' with your Arduino's serial port

while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    multiLandmarks = results.multi_hand_landmarks

    if multiLandmarks:
        handPoints = []
        for handLms in multiLandmarks:
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

            for lm in handLms.landmark:
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                handPoints.append((cx, cy))

        upCount = 0
        for coordinates in fingerCoordinates:
            if handPoints[coordinates[0]][1] < handPoints[coordinates[1]][1]:
                upCount += 1
        if handPoints[thumbCoordinates[0]][0] > handPoints[thumbCoordinates[1]][0]:
            upCount += 1

        # Send upCount value to Arduino
        ser.write(str(upCount).encode())

        cv2.putText(img, str(upCount), (10, 100), cv2.FONT_ITALIC, 4, (255, 0, 255), 4)

    cv2.imshow("Finger Counter", img)
    cv2.waitKey(10)

    if cv2.waitKey(1) & 0xFF == ord('x'):
        break

cap.release()
cv2.destroyAllWindows()

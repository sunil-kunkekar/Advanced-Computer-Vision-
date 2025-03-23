#ProjectExample.py
import cv2
import mediapipe as mp
import time
import handtracking_module as htm
pTime = 0
cTime = 0
cap = cv2.VideoCapture(0)
detector = htm.handDetector()

while True:
    success, img = cap.read()
    
    if not success or img is None:
        print("Warning: Could not read frame from camera.")
        continue  # Skip this iteration and try again
    
    img = detector.findHands(img, draw=True)
    lmList = detector.findPosition(img, draw=False)

    if lmList:
        print(lmList[4])

    cTime = time.time()
    fps = 1 / (cTime - pTime) if (cTime - pTime) > 0 else 0
    pTime = cTime

    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
    cv2.imshow("Image", img)

    if cv2.waitKey(1) & 0xFF == 27:  
        break

cap.release()
cv2.destroyAllWindows()

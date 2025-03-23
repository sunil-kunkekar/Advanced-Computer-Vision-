# import cv2
# import mediapipe as mp
# import time
# pTime = 0  # Initialize pTime

# cap = cv2.VideoCapture(0)
# mpHands = mp.solutions.hands
# hands = mpHands.Hands()

# mpDraw = mp.solutions.drawing_utils

# while True:
#     success,img = cap.read()
#     imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
#     result = hands.process(imgRGB)
#     # print(result.multi_hand_landmarks)
    
#     if result.multi_hand_landmarks:
#         for handLms in result.multi_hand_landmarks:
#             for id,lm in enumerate(handLms.landmark):
#                 # print(id,lm)
#                 h,w,c = img.shape
#                 cx,cy = int(lm.x*w),int(lm.y*h)
#                 # print(id,cx,cy)
#                 if id==0:
#                     cv2.circle(img,(cx,cy),10,(255,0,255),cv2.FILLED)
#             mpDraw.draw_landmarks(img,handLms,mpHands.HAND_CONNECTIONS)
                
#     cTime = time.time()
#     # fps   = 1/(cTime - pTime)
#     fps = 1 / (cTime - pTime)

#     pTime = cTime
    
#     cv2.putText(img, str(int(fps)),(10,70),cv2.FONT_HERSHEY_PLAIN,3,(255,2,255),3) 
    
#     cv2.imshow('image',img)
#     cv2.waitKey(1)
#===================================================
#handtracking_module.py

import cv2
import mediapipe as mp
import time

class handDetector():
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(
            static_image_mode=self.mode,
            max_num_hands=self.maxHands,
            min_detection_confidence=self.detectionCon,
            min_tracking_confidence=self.trackCon
        )
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self, img, handNo=0, draw=True):
        lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 10, (255, 0, 255), cv2.FILLED)
        return lmList

def main():
    pTime = 0
    cap = cv2.VideoCapture(0)  # Ensure the correct camera index (0 or 1)
    detector = handDetector()
    while True:
        success, img = cap.read()
        if not success:
            print("Failed to capture image")
            continue
        
        img = detector.findHands(img)
        lmList = detector.findPosition(img)
        if len(lmList) != 0:
            print(lmList[4])

        cTime = time.time()
        fps = 1 / (cTime - pTime) if (cTime - pTime) > 0 else 0
        pTime = cTime

        cv2.putText(img, f"FPS: {int(fps)}", (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
        cv2.imshow("Image", img)

        if cv2.waitKey(1) & 0xFF == 27:  # Press ESC to exit
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

    
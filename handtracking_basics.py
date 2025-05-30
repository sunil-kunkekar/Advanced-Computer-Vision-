import cv2
import mediapipe as mp
import time
pTime = 0  # Initialize pTime
cTime=0
cap = cv2.VideoCapture(0)
mpHands = mp.solutions.hands
hands = mpHands.Hands()

mpDraw = mp.solutions.drawing_utils

while True:
    success,img = cap.read()
    imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    result = hands.process(imgRGB)
    # print(result.multi_hand_landmarks)
    
    if result.multi_hand_landmarks:
        for handLms in result.multi_hand_landmarks:
            for id,lm in enumerate(handLms.landmark):
                # print(id,lm)
                h,w,c = img.shape
                cx,cy = int(lm.x*w),int(lm.y*h)
                # print(id,cx,cy)
                if id==0:
                    cv2.circle(img,(cx,cy),10,(255,0,255),cv2.FILLED)
            mpDraw.draw_landmarks(img,handLms,mpHands.HAND_CONNECTIONS)
                
    cTime = time.time()
    # fps   = 1/(cTime - pTime)
    fps = 1 / (cTime - pTime)

    pTime = cTime
    
    cv2.putText(img, str(int(fps)),(10,70),cv2.FONT_HERSHEY_PLAIN,3,(255,2,255),3) 
    
    cv2.imshow('image',img)
    cv2.waitKey(1)
    
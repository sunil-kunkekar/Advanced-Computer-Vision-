import cv2
import mediapipe as mp
import time
import os
import matplotlib.pyplot as plt

# Suppress TensorFlow/MediaPipe warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# Initialize MediaPipe Pose Estimation
mpDraw = mp.solutions.drawing_utils
mpPose = mp.solutions.pose
pose = mpPose.Pose()

# Load Video
video_path = 'E:/New_year_2025/Computer_vision/pose_Estimation/new.mp4'
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print(f"Error: Cannot open video file {video_path}")
    exit()

pTime = 0
while True:
    success, img = cap.read()
    if not success:
        print("End of video or error reading frame.")
        break  # Exit loop if video ends

    # Convert to RGB
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = pose.process(imgRGB)

    # Draw landmarks if detected
    if results.pose_landmarks:
        mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
        for id, lm in enumerate(results.pose_landmarks.landmark):
            h, w, c = img.shape
            cx, cy = int(lm.x * w), int(lm.y * h)
            cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)

    # Calculate FPS
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    # Display FPS on Frame
    cv2.putText(img, f"FPS: {int(fps)}", (70, 50), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)

    # Display frame
    try:
        cv2.imshow("Pose Estimation", img)
        key = cv2.waitKey(1)
        if key == 27:  # Press ESC to exit
            break
    except cv2.error:
        print("OpenCV GUI functions are not available. Using Matplotlib instead.")
        plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        plt.axis("off")
        plt.show()
        break

cap.release()
cv2.destroyAllWindows()

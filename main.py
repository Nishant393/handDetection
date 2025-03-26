import cv2
import math
import numpy as np
from HandTracker import HandTracker
from VolumeControl import VolumeControl

# Initialize Hand Tracker
tracker = HandTracker(cam_index=1)  # Change cam_index if needed
volume_control = VolumeControl()


while True:
    frame = tracker.get_frame()
    if frame is None:
        print("Error: Couldn't read frame!")
        break

    # Get hand landmarks
    landmarks, multi_hand_landmarks = tracker.get_hand_landmarks(frame)
    print(multi_hand_landmarks)
    # Draw landmarks
    tracker.draw_landmarks(frame, multi_hand_landmarks)

    # Draw circles at each landmark
    for idx, x, y in landmarks:
        cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)

    # for volume finger
    if len(landmarks)!=0:
        i1 ,x1 , y1 = landmarks[4]
        i2 ,x2 , y2 = landmarks[8]
        cv2.circle(frame, (x1, y1), 5, (100, 100, 255), -1)
        cv2.circle(frame, (x2, y2), 5, (100, 100, 255), -1)
        cv2.line(frame, (x2, y2),(x1,y1), (255, 255, 255), 2)
        dist = math.hypot(x2 - x1 ,y2 - y1 )
        vol = np.interp(dist, [30,150],[0,100])
        print(vol)# 50 to 150
        volume_control.set_volume(vol)

        # print("Current  Volume:", volume_control.get_volume_range())

    # Show result
    cv2.imshow("Hand Tracker", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

tracker.release()

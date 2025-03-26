import cv2
import mediapipe as mp
import time

class HandTracker:
    def __init__(self, min_detection_conf=0.6, min_tracking_conf=0.6, cam_index=0):
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(min_detection_confidence=min_detection_conf,
                                         min_tracking_confidence=min_tracking_conf)
        self.cap = cv2.VideoCapture(cam_index)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1000)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)
        self.prev_time = 0

    def get_hand_landmarks(self, image):
        """ Returns the position of all hand landmark points as a list of tuples """
        rgb_frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        result = self.hands.process(rgb_frame)
        landmark_positions = []
        
        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                for idx, landmark in enumerate(hand_landmarks.landmark):
                    h, w, _ = image.shape
                    cx, cy = int(landmark.x * w), int(landmark.y * h)
                    landmark_positions.append((idx, cx, cy))
        
        return landmark_positions, result.multi_hand_landmarks

    def draw_landmarks(self, image, landmarks):
        """ Draws hand landmarks and connections """
        if landmarks:
            for hand_landmarks in landmarks:
                self.mp_drawing.draw_landmarks(image, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)

    def get_frame(self):
        """ Captures a frame from the webcam """
        ret, frame = self.cap.read()
        return frame if ret else None
    
    def release(self):
        """ Releases the camera resources """
        self.cap.release()
        cv2.destroyAllWindows()

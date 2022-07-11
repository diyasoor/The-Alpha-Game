import cv2
import mediapipe as mp
from settings import *
import numpy as np
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_gloves = mp.solutions.hands



class GloveTracking:
    def __init__(self):
        self.glove_tracking = mp_gloves.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)
        self.glove_x = 0
        self.glove_y = 0
        self.results = None
        self.glove_closed = False


    def scan_gloves(self, image):
        rows, cols, _ = image.shape

        # Flip the image horizontally for a later selfie-view display, and convert
        # the BGR image to RGB.
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        image.flags.writeable = False
        self.results = self.glove_tracking.process(image)

        # Draw the glove annotations on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        self.glove_closed = False

        if self.results.multi_hand_landmarks:
            for glove_landmarks in self.results.multi_hand_landmarks:
                x, y = glove_landmarks.landmark[9].x, glove_landmarks.landmark[9].y

                self.glove_x = int(x * SCREEN_WIDTH)
                self.glove_y = int(y * SCREEN_HEIGHT)

                x1, y1 = glove_landmarks.landmark[12].x, glove_landmarks.landmark[12].y

                if y1 > y:
                    self.glove_closed = True

                mp_drawing.draw_landmarks(
                    image,
                    glove_landmarks,
                    mp_gloves.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style())
        return image

    def get_hand_center(self):
        return (self.glove_x, self.glove_y)


    def display_hand(self):
        cv2.imshow("image", self.image)
        cv2.waitKey(1)

    def is_hand_closed(self):

        pass



# POSTURE MODULE
# This file analyses a players head and embouchure (mouth) position 
# using MediaPipe's face landmark model.

import math
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# LOADING THE FACE LANDMARKER MODEL

face_base_options = python.BaseOptions(
    model_asset_path="face_landmarker.task"
)

face_options = vision.FaceLandmarkerOptions(
    base_options=face_base_options,
    running_mode=vision.RunningMode.VIDEO,
    # Confidence thresholds determine how certain mediapipe has to be to detect the face
    min_face_detection_confidence=0.7,
    min_face_presence_confidence=0.7,
    min_tracking_confidence=0.7
)

face_detector = vision.FaceLandmarker.create_from_options(face_options)

# ANALYSING THE POSTURE OF BOTH THE HEAD AND EMBOUCHURE (MOUTH POSITION)

def analyse_the_posture(face):

    left_eye_outer = face[33]
    right_eye_outer = face[263]

    mouth_left = face[76]
    mouth_right = face[308]
    mouth_top = face[0]
    mouth_bottom = face[17]

    # ANALYSING THE HEAD ANGLE

    # Using the outer corners of the eyes to estimate the head angle
    o = (right_eye_outer.x - left_eye_outer.x)
    p = (right_eye_outer.y - left_eye_outer.y)

    # Calculating the angle that the line between the two eyes makes with the horizontal
    # o is the horizontal difference and p is the vertical difference
    face_angle = math.degrees(
        math.atan2(p, o)
    )

    # Initialising the feedback messages as empty strings
    # so that they can be updated later depending on the value of the head angle
    head_feedback_1 = ""
    head_feedback_2 = ""

    # Thresholds were determined through testing to identify an acceptable head position when playing flute
    if abs(face_angle) < 10:

        head_feedback_1 = "Head level"

    else:

        head_feedback_2 = "Straighten head"

    # ANALYSING THE EMBOUCHURE (MOUTH POSITION)

    # Calculating the mouth width
    mouth_width = abs(
        mouth_right.x - mouth_left.x
    )

    # Calculating the mouth height
    mouth_height = abs(
        mouth_bottom.y - mouth_top.y
    )

    if mouth_width > 0:

        # Compare the mouth height to the mouth width to determine how open/closed the mouth is
        mouth_ratio = (
                mouth_height /
                mouth_width
        )

    else:

        mouth_ratio = 0

    # Clamping the embouchure value between 0 and 1 for simplicity
    flute_embouchure = min(
        max(mouth_ratio, 0),
        1
    )

    # Initialising the feedback messages as empty strings
    # so that they can be updated later depending on the detected mouth position
    embouchure_feedback_1 = ""
    embouchure_feedback_2 = ""
    embouchure_feedback_addition = ""
    embouchure_correct = ""

    # Thresholds were determined through testing to identify an acceptable 
    # mouth position when playing flute without relying on audio analysis
    if flute_embouchure <= 0.45:

        embouchure_feedback_1 = "Open mouth"
        embouchure_feedback_addition = "more"

    elif flute_embouchure >= 0.62:

        embouchure_feedback_2 = "Close mouth"
        embouchure_feedback_addition = "more"

    elif 0.45 < flute_embouchure < 0.62:

        embouchure_correct = "PERFECT!"
        embouchure_feedback_addition = ""

    return {
        "face_angle": face_angle,
        "head_feedback_1": head_feedback_1,
        "head_feedback_2": head_feedback_2,
        "embouchure_feedback_1": embouchure_feedback_1,
        "embouchure_feedback_2": embouchure_feedback_2,
        "embouchure_feedback_addition": embouchure_feedback_addition,
        "embouchure_correct": embouchure_correct,
        "embouchure": flute_embouchure,
    }

# MAIN PROGRAM
# This file connects the hand-tracking, posture analysis, calibration, note detection
# and user interface (UI) modules together.

# IMPORTS

import cv2
import mediapipe as mp
import time
import numpy as np
import random

from hand_tracking import (
  detector, 
  get_finger_values, 
  check_menu_buttons, 
  check_back_button
)

from practice import (check_note)

from posture import (
  face_detector, 
  analyse_the_posture
)

from flute_fingering import (
  notes, 
  flute_fingerings
)

import UI
from UI import hand_lines

# SETUP OPENCV WINDOW

cap = cv2.VideoCapture(0)

cv2.namedWindow(
  "Camera", 
  cv2.WINDOW_NORMAL
)

cv2.resizeWindow(
  "Camera", 
  1000, 
  650
)

cv2.moveWindow(
  "Camera", 
  145, 
  30
)

overlay = cv2.imread("flutetracker.png")

# VARIABLES NEEDED (MAINLY FOR THE CALIBRATION SYSTEM)

calibration_stage = 0
hold_frames = 0
flute_keys_open_stage = []
flute_keys_close_stage = []
binary_values = []
calibration_start_time = None
calculated = False
calibrated = False

pbutton_pressed = False
backbutton_pressed = False
pobutton_pressed = False

mode = "menu"
random_note = None
correct_time = 0
condition = "waiting"
previous_state = [0] * 8

# THE "WHITE TRUE" LOOP

while True:
    
    success, img = cap.read()

    type_text = ""

    # Preventing webcam frame bug
    if not success:
        print("Error with camera frames")
        break

    # Flipping webcam image (so it behaves like a normal camera and feels more natural)
    img = cv2.flip(img, 1)

    full_order = None

    h, w, _ = img.shape

    overlay = cv2.resize(overlay, (640, 160))

    # Position overlay at (x, y)
    x, y = 0, 0

    # Draw overlay onto webcam frame
    img[y:y + overlay.shape[0], x:x + overlay.shape[1]] = overlay

    UI.draw_detection_box(img, w)

# MEDIAPIPE ESSENTIALS

    # Converting colour channels from RGB to BGR
    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Makes format of image readable to mediapipe
    mp_image = mp.Image(
        image_format=mp.ImageFormat.SRGB,
        data=rgb_img
    )

    # Creating timestamps in milliseconds for stable tracking between frames.
    timestamp_ms = int(time.time() * 1000)

    # Sends current image frame and timestamp to the hand-tracking model.
    result = detector.detect_for_video(mp_image, timestamp_ms)

# DRAW HAND LANDMARKS/HAND LINES AND CHECK IF THEY ARE IN THE DETECTION BOX

    if result.hand_landmarks:

        aligned_hands = 0
        left = None
        right = None

        for hand_landmarks in result.hand_landmarks:

            inside_count = 0

            UI.draw_hand_landmarks(
                img,
                hand_landmarks,
                hand_lines,
                w,
                h
            )

            for landmark in hand_landmarks:
                x = int(landmark.x * w)  # Width of frame
                y = int(landmark.y * h)  # Height of frame

                if 0 <= x <= w and \
                    160 <= y <= 470:
                    inside_count += 1

            ratio = inside_count / 21

            if ratio >= 0.85:
                aligned_hands += 1

        flute_aligned = (aligned_hands == 2)

        for i, hand_landmarks in enumerate(result.hand_landmarks):

                if not result.handedness or i >= len(result.handedness):
                    continue

                hand_type = result.handedness[i][0].category_name

                # We have to flip it because we flipped the webcam before
                if hand_type == "Left":
                    hand_type = "Right"
                else:
                    hand_type = "Left"

# ORDERING THE VALUES OBTAINED

                order = get_finger_values(
                    hand_landmarks
                )

                if hand_type == "Left":
                    left = order
                else:
                    right = order

                # Handles cases where both hands, one hand, or neither hand, is detected
                if left is not None and right is not None:
                    full_order = left + right
                elif left is not None:
                    full_order = left
                elif right is not None:
                    full_order = right
                else:
                    full_order = None

# CALIBRATION
# Calibration allows the system to calculate personalised finger thresholds 
# rather than relying on fixed thresholds. This helps account for differences
# in finger size, camera position, hand position, depth and lighting conditions.

        calibration_wait_time = 3.0

        if calibrated:
            type_text = "Select a mode"

        elif not calibrated:
            if flute_aligned:
                hold_frames += 1
            else:
                hold_frames = 0
                calibration_stage = 0
                calibration_start_time = None

            stable_alignment = hold_frames > 6

            if calibration_stage == 0:

                if flute_aligned:
                    calibration_stage = 1
                    calibration_start_time = time.time()
                else:
                    type_text = "Align flute with box below"

            elif calibration_stage == 1:

                if stable_alignment:
                    type_text = "Hold still..."
                    time_calculation = time.time() - calibration_start_time

                    if time_calculation > calibration_wait_time:
                        calibration_stage = 2

                elif not flute_aligned:
                    calibration_stage = 0
                    calibration_start_time = None
                    type_text = "Align flute with box above"

                else:
                    type_text = "Hold still..."

            elif calibration_stage == 2:
                type_text = "Hold down ALL keys on flute"
                if full_order is not None and len(full_order) == 8:
                    flute_keys_close_stage.append(full_order)

                if len(flute_keys_close_stage) > 120:
                    calibration_stage = 3

            elif calibration_stage == 3:
                type_text = "Open ALL keys on flute"
                if full_order is not None and len(full_order) == 8:
                    flute_keys_open_stage.append(full_order)

                if len(flute_keys_open_stage) > 120:
                    calibration_stage = 4

            elif calibration_stage == 4:
                type_text = "Calibration complete!"

                if not calculated:

                    averaged_closed_values = []
                    averaged_opened_values = []
                    threshold_values = []

                    # Working out the open and closed values (different for each person)
                    for i in range(8):

                        # The median is used instead of the mean to reduce the impact of occassional 
                        # inaccurate hand-tracking measurements
                      
                        avg_close = np.median([frame[i] for frame in flute_keys_close_stage])
                        averaged_closed_values.append(round(avg_close, 2))

                        avg_open = np.median([frame[i] for frame in flute_keys_open_stage])
                        averaged_opened_values.append(round(avg_open, 2))

                    # Print in console instead of on the screen
                    print("Closed values:")
                    print(averaged_closed_values)
                    print("Open values:")
                    print(averaged_opened_values)

                    # Creating thresholds (the middle of the closed and open values)
                    for opened, closed in zip(averaged_opened_values, averaged_closed_values):
                        
                        # Variating factors are used for each finger because every finger has a 
                        # different range of movement. This can affect tracking behaviour differently.
                        # These were adjusted through testing to find reliable thresholds
                        factor = [
                            0.55, # Left index finger
                            0.50, # Left middle finger
                            0.45, # Left ring finger
                            0.40, # Left pinky finger
                            0.50, # Right index finger
                            0.50, # Right middle finger
                            0.45, # Right ring finger
                            0.35 # Right pinky finger
                        ]
                        threshold_decimal = closed + factor[i] * (opened - closed)
                        threshold_values.append(round(threshold_decimal, 2))

                    print("Threshold:")
                    print(threshold_values)

                    calculated = True
                    calibration_stage = 5
                    calibrated = True

                    print("Calibration locked")

# CONVERT EACH FINGER VALUE INTO A BINARY STATE (1 OR 0)

        if calibrated and full_order is not None:
            type_text = "Select a mode"

            binary_values = []

            finger_gaps = [abs(opened - closed) for opened, closed in zip(averaged_opened_values, averaged_closed_values)]

            # Smoothing the calibration so that it does not flicker as much
            # A tolerance is applied around each threshold to reduce flickering between
            # open and closed states caused by small tracking variations
            for i, (value, thresh) in enumerate(zip(full_order, threshold_values)):

                margins = max(0.02, finger_gaps[i] * 0.15)

                if value > (thresh + margins):
                    state = 1
                elif value < thresh - margins * 1.4 :
                    state = 0
                else:
                    state = previous_state[i]

                binary_values.append(state)
                previous_state[i] = state

# DRAWING THE BUTTONS

    if calibration_stage == 5 and mode == "menu":

        UI.drawing_practice_button(img)
        UI.drawing_posture_button(img)

# PRESSING THE BUTTONS (BUTTON DETECTION)

        if result.hand_landmarks:

            hand_over_pbutton, hand_over_pobutton = check_menu_buttons(
                result.hand_landmarks,
                w,
                h
            )

            if hand_over_pbutton and not pbutton_pressed:
                mode = "practice"
                random_note = random.choice(notes)
                pbutton_pressed = True

            if not hand_over_pbutton:
                pbutton_pressed = False

            if hand_over_pobutton and not pobutton_pressed:
                    mode = "posture"
                    random_note = None
                    pobutton_pressed = True

            if not hand_over_pobutton:
                    pobutton_pressed = False

# PRACTICE MODE SELECTED

    if mode == "practice" and random_note is not None:

        cv2.putText(img,
                    f"Play:",
                    (50, 45),
                    cv2.FONT_HERSHEY_TRIPLEX,
                    0.9,
                    (255, 255, 255),
                    1)

        cv2.putText(img,
                    f"{random_note}",
                    (62, 90),
                    cv2.FONT_HERSHEY_TRIPLEX,
                    1,
                    (255, 255, 255),
                    2)

        type_text = "Play note shown above"

        condition, correct_time, random_note = check_note(
            binary_values,
            random_note,
            condition,
            correct_time,
            flute_fingerings,
            notes
        )

        if condition == "correct":

            UI.practice_condition_correct(
                img,
                correct_time
            )

            UI.drawing_correct_hands(
                result.hand_landmarks,
                img,
                w,
                h
            )

        UI.drawing_back_button(img)

        if result.hand_landmarks:

            hand_over_backbutton, backbutton_pressed, mode, random_note = check_back_button(
                result.hand_landmarks,
                w,
                h,
                backbutton_pressed,
                mode,
                random_note
            )

# POSTURE MODE SELECTED

    if mode == "posture":

        face_result = face_detector.detect_for_video(
            mp_image,
            timestamp_ms
        )

        type_text = "Play any note/song"

        UI.drawing_back_button(img)

        if result.hand_landmarks:

            hand_over_backbutton, backbutton_pressed, mode, random_note = check_back_button(
                result.hand_landmarks,
                w,
                h,
                backbutton_pressed,
                mode,
                random_note
            )

        if face_result.face_landmarks:

            face = face_result.face_landmarks[0]

            posture = analyse_the_posture(face)

            UI.draw_face_landmarks(face, w, h, img)

            UI.embouchure_position_correct(
                img,
                posture["embouchure"]
            )

            UI.posture_analysis_feedback(
                img,
                posture
            )

    cv2.putText(img,
                str(type_text),
                (5, 181),
                cv2.FONT_HERSHEY_TRIPLEX,
                0.7,
                (255, 255, 255),
                1)
  
# ENDING THE CIRCUIT

    cv2.imshow(
        "Camera",
        img
    )

    key = cv2.waitKey(1)

    # Press q to end the loop
    if key == ord('q'):
        break

# CLEANUP

cap.release()
cv2.destroyAllWindows()

import cv2
import time

# (OpenCV uses BGR colour order instead of RBG)

# DESIGNING THE DETECTION BOX + MAIN MENU VISUALS IN ONE FUNCTION

def draw_detection_box(
        img,
        w
):

    # Futuristic visuals (dark blue theme)
    cv2.rectangle(
      img, 
      (0, 500), 
      (w, 471), 
      (75, 0, 0), 
      -1
    )
  
    cv2.rectangle(
      img, 
      (0, 470), 
      (w, 160), 
      (255, 200, 80), 
      2
    )
  
    cv2.rectangle(
      img, 
      (0, 470), 
      (w, 160), 
      (255, 255, 255), 
      1
    )
  
    cv2.rectangle(
      img, 
      (25, 25), 
      (159, 120), 
      (75, 0, 0), 
      -1
    )

# DESIGNING THE PRACTICE BUTTON 

def drawing_practice_button(img):

    cv2.rectangle(
      img, 
      (600, 240), 
      (450, 190), 
      (75, 0, 0), 
      -1
    )

    cv2.rectangle(
      img, 
      (600, 240), 
      (450, 190), 
      (255, 255, 255), 
      3
    )

    cv2.rectangle(
      img, 
      (600, 240), 
      (450, 190), 
      (255, 200, 80), 
      1
    )

    cv2.putText(img, str("PRACTICE"),
                (465, 224),
                cv2.FONT_HERSHEY_COMPLEX,
                0.8,
                (255, 255, 255),
                1)

# DESIGNING THE POSTURE BUTTON

def drawing_posture_button(img):

    cv2.rectangle(
      img, 
      (600, 350), 
      (450, 300), 
      (75, 0, 0), 
      -1
    )

    cv2.rectangle(
      img, 
      (600, 350), 
      (450, 300), 
      (255, 255, 255), 
      3
    )

    cv2.rectangle(
      img, 
      (600, 350), 
      (450, 300), 
      (255, 200, 80), 
      1
    )

    cv2.putText(img, str("POSTURE"),
                (468, 334),
                cv2.FONT_HERSHEY_COMPLEX,
                0.8,
                (255, 255, 255),
                1)

# DESIGNING THE BACK BUTTON 

def drawing_back_button(img):

    cv2.rectangle(
      img, 
      (85, 470), 
      (0, 430), 
      (75, 0, 0), 
      -1
    )

    cv2.rectangle(
      img, 
      (85, 470), 
      (0, 430), 
      (255, 255, 255), 
      3
    )

    cv2.rectangle(
      img, 
      (85, 470), 
      (0, 430), 
      (255, 200, 80), 
      1
    )

    cv2.putText(img, str("BACK"),
                (10, 458),
                cv2.FONT_HERSHEY_COMPLEX,
                0.8,
                (255, 255, 255),
                1)

# DESIGNING THE HAND LINES

# Each pair represents two landmark indices that are connected by a line
# All of the pairs combined form the shape of a hand
hand_lines = [
    (0, 1), (1, 2), (2, 3), (3, 4),       # Thumb
    (0, 5), (5, 6), (6, 7), (7, 8),       # Index finger
    (5, 9), (9, 10), (10, 11), (11, 12),     # Middle finger
    (9, 13), (13, 14), (14, 15), (15, 16),    # Ring finger
    (13, 17), (17, 18), (18, 19), (19, 20),   # Pinky finger
    (0, 17), (0,9), (0, 13), (2, 5)        # Palm connections
]

# DESIGNING THE FACE LINES

# Again, each pair represents two landmark indices that are connected by a line
# All of the pairs combined form the shape of the eyes, mouth and parts of the nose
# Only selected face connections are drawn because drawing every MediaPipe connection
# could increase CPU usage
face_lines = [
    (133, 173), (173, 157), (157, 158),
    (158, 159), (159, 160),             # Left eye (for head tilt)

    (160, 161), (161, 246), (246, 33),
    (33, 7), (7, 163), (163, 144),
    (144, 145), (145, 153), (153, 154),
    (154, 155), (155, 133), (133, 243),
    (243, 190), (190, 56), (56, 28),
    (28, 27), (27, 29), (29, 30),
    (30, 247), (247, 130), (130, 33),
    (110, 24), (24, 23), (23, 22),
    (22, 26), (362, 398), (398, 384),

    (384, 385), (385, 386), (386, 387),  # Right eye (for head tilt)
    (387, 388), (388, 466), (466, 263),
    (263, 249), (249, 390), (390, 373),
    (373, 374), (374, 380), (380, 381),
    (381, 382), (382, 362), (463, 362),
    (463, 414), (414, 286), (286, 258),
    (258, 257), (257, 259), (259, 260),
    (260, 467), (467, 359), (359, 263),
    (256, 252), (252, 253), (253, 254),
    (254, 339), (243, 244), (244, 245),
    (245, 122), (122, 6), (6, 351),

    (351, 465),                          # Nose (for head positioning)
    (465, 464), (464, 463), (6, 197),
    (197, 195), (195, 5), (5, 4),
    (4, 1), (4, 45), (4, 275),
    (275, 5), (45, 5), (45, 1),
    (1, 275), (0, 267), (267, 269),
    (269, 270), (270, 408), (408, 306),

    (306, 307),                          # Mouth (for flute embouchure)
    (307, 321), (321, 405), (405, 314),
    (314, 17), (17, 84), (84, 181),
    (181, 91), (91, 77), (77, 76),
    (76, 184), (184, 40), (40, 39),
    (39, 37), (37, 0), (76, 62),
    (62, 78), (78, 191), (191, 80),
    (80, 81), (81, 82), (82, 13),
    (13, 312), (312, 311), (311, 310),
    (310, 415), (415, 308), (308, 291),
    (291, 306), (308, 324), (324, 318),
    (318, 402), (402, 317), (317, 14),
    (14, 87), (87, 178), (178, 88),
    (88, 95), (95, 78)
]

# DRAWING THE HAND LANDMARKS AND HAND LINES

def draw_hand_landmarks(
        img,
        hand_landmarks,
        hand_lines,
        w,
        h,
        colour=None
):
    if colour is None:

        line_colour = (255, 200, 80)
        point_colour = (255, 255, 255)

    else:

        line_colour = colour
        point_colour = colour

    for start_idx, end_idx in hand_lines:

        start = hand_landmarks[start_idx]
        end = hand_landmarks[end_idx]

        x1, y1 = int(start.x * w), int(start.y * h)
        x2, y2 = int(end.x * w), int(end.y * h)

        cv2.line(
            img,
            (x1, y1),
            (x2, y2),
            (255, 200, 80),
            2
        )

        cv2.line(
            img,
            (x1, y1),
            (x2, y2),
            (255, 255, 255),
            1
        )

        for landmark in hand_landmarks:
            x = int(landmark.x * w)
            y = int(landmark.y * h)

            cv2.circle(
                img,
                (x, y),
                5,
                (255, 200, 80),
                -1
            )

            cv2.circle(
                img,
                (x, y),
                4,
                (245, 200, 80),
                -1
            )

            cv2.circle(
                img,
                (x, y),
                3,
                (255, 255, 255),
                -1
            )

# DRAWING THE FACE LANDMARKS AND FACE LINES

def draw_face_landmarks(
        face,
        w,
        h,
        img
):

    for start_idx, end_idx in face_lines:

        start = face[start_idx]
        end = face[end_idx]

        x1, y1 = int(start.x * w), int(start.y * h)
        x2, y2 = int(end.x * w), int(end.y * h)

        # Futuristic glow layer for the lines (BGR)
        cv2.line(
          img, 
          (x1, y1), 
          (x2, y2), 
          (255, 200, 80), 
          2
        )
        
      # Main colour layer for the lines (BGR)
        cv2.line(
          img, 
          (x1, y1), 
          (x2, y2), 
          (255, 255, 255), 
          1
        )

# VISUALS FOR THE PRACTICE MODE

def practice_condition_correct(
        img,
        correct_time
):

    cv2.rectangle(
        img,
        (25, 25),
        (159, 120),
        (75, 0, 0),
        -1
    )

    cv2.putText(img,
                "CORRECT!",
                (28, 82),
                cv2.FONT_HERSHEY_TRIPLEX,
                0.8,
                (0, 255, 0),
                2
                )

    bar1_x = 30
    bar1_y = 90
    bar1_width = 122
    bar1_height = 20

    cv2.rectangle(
        img,
        (bar1_x, bar1_y),
        (bar1_x + bar1_width,
        bar1_y + bar1_height),
        (255, 255, 255),
        2
    )

    time_held = time.time() - correct_time

    # Convert the time_held into a value between 0 and 1
    # This is used to fill up the progress bar
    correctness = min(max(time_held, 0), 1)

    fill_width_1 = int(bar1_width * correctness)

    cv2.rectangle(
        img,
        (bar1_x, bar1_y),
        (bar1_x + fill_width_1,
        bar1_y + bar1_height),
        (0, 255, 0),
        -1
    )


def drawing_correct_hands(
        hand_landmarks,
        img,
        w,
        h
):

    for hand in hand_landmarks:

        for start_idx, end_idx in hand_lines:

            start = hand[start_idx]
            end = hand[end_idx]

            x1, y1 = int(start.x * w), int(start.y * h)
            x2, y2 = int(end.x * w), int(end.y * h)

            # Futuristic glow layer for the lines (BGR)
            cv2.line(
                img,
                (x1, y1),
                (x2, y2),
                (0, 139, 0),
                2
            )

            # Main colour layer for the lines (BGR)
            cv2.line(
                img,
                (x1, y1),
                (x2, y2),
                (0, 255, 0),
                1
            )

            for landmark in hand:

                x = int(landmark.x * w)
                y = int(landmark.y * h)

                cv2.circle(
                    img,
                    (x, y),
                    7,
                    (0, 80, 0),
                    -1
                )

                cv2.circle(
                    img,
                    (x, y),
                    5,
                    (0, 255, 0),
                    -1
                )

                cv2.circle(
                    img,
                    (x, y),
                    3,
                    (255, 255, 255),
                    -1
                )

# VISUALS FOR THE POSTURE MODE

def embouchure_position_correct(
        img,
        flute_embouchure
):

    bar_x = 40
    bar_y = 80
    bar_width = 100
    bar_height = 15

    # Outline of bar
    cv2.rectangle(
        img,
        (bar_x, bar_y),
        (bar_x + bar_width,
         bar_y + bar_height),
        (255, 255, 255),
        2
    )

    fill_width = int(bar_width * flute_embouchure)

    if 0.45 < flute_embouchure < 0.62:

        # Green colour for when flute embouchure is good
        colour = (0, 255, 0) 

    else:

        # Red colour for when flute embouchure is bad
        colour = (0, 0, 255)

    # Drawing the fill bar (block colour)
    cv2.rectangle(
        img,
        (bar_x, bar_y),
        (bar_x + fill_width,
         bar_y + bar_height),
        colour,
        -1
    )

def posture_analysis_feedback(
        img,
        posture,
):

    cv2.putText(img,
                posture["head_feedback_2"],
                (29, 37),
                cv2.FONT_HERSHEY_TRIPLEX,
                0.45,
                (0, 0, 255),
                1)

    cv2.putText(img,
                posture["head_feedback_1"],
                (50, 37),
                cv2.FONT_HERSHEY_TRIPLEX,
                0.45,
                (0, 255, 0),
                1)

    cv2.putText(img,
                str("Embouchure level"),
                (37, 70),
                cv2.FONT_HERSHEY_TRIPLEX,
                0.44,
                (255, 255, 255),
                1)

    cv2.putText(img,
                str("_______________"),
                (18, 50),
                cv2.FONT_HERSHEY_TRIPLEX,
                0.48,
                (255, 255, 255),
                1)

    cv2.putText(img,
                str("_______________"),
                (18, 100),
                cv2.FONT_HERSHEY_TRIPLEX,
                0.48,
                (255, 255, 255),
                1)

    cv2.putText(img,
                posture["embouchure_feedback_1"],
                (45, 115),
                cv2.FONT_HERSHEY_TRIPLEX,
                0.45,
                (0, 0, 255),
                1)

    cv2.putText(img,
                posture["embouchure_feedback_2"],
                (44, 115),
                cv2.FONT_HERSHEY_TRIPLEX,
                0.45,
                (0, 0, 255),
                1)

    cv2.putText(img,
                posture["embouchure_feedback_addition"],
                (72, 128),
                cv2.FONT_HERSHEY_TRIPLEX,
                0.45,
                (0, 0, 255),
                1)

    cv2.putText(img,
                posture["embouchure_correct"],
                (40, 125),
                cv2.FONT_HERSHEY_TRIPLEX,
                0.7,
                (0, 255, 0),
                1)


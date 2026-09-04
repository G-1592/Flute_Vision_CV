import math
from math import pi
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# LOADING THE HAND LANDMARKER MODEL

base_options = python.BaseOptions(
    model_asset_path='hand_landmarker.task'
)

options = vision.HandLandmarkerOptions(
    base_options=base_options,
    running_mode=vision.RunningMode.VIDEO,
    num_hands=2,
    min_hand_detection_confidence=0.4,
    min_hand_presence_confidence=0.4,
    min_tracking_confidence=0.4
)

detector = vision.HandLandmarker.create_from_options(options)

# CALCULATING THE FINGER ANGLES (HOW BENT/STRAIGHT A FINGER IS)

def angle(a, b, c):

    # Vector ba where (ba = a-b) --> from middle joint to tip of finger
    ba_x, ba_y, ba_z = a.x - b.x, a.y - b.y, a.z - b.z
    # Vector bc where (bc = c-b) --> from base to middle joint of finger
    bc_x, bc_y, bc_z = c.x - b.x, c.y - b.y, c.z - b.z

    # Calculating the dot product between vectors ba and bc
    dot_product = (
            ba_x * bc_x +
            ba_y * bc_y +
            ba_z * bc_z
    )

    # Finding the magnitude of both vectors
    magnitude_ba = math.sqrt(
        ba_x ** 2 +
        ba_y ** 2 +
        ba_z ** 2
    )

    magnitude_bc = math.sqrt(
        bc_x ** 2 +
        bc_y ** 2 +
        bc_z ** 2
    )

    # Preventing getting zero as a denominator
    if magnitude_ba == 0 or magnitude_bc == 0:
        return 0

    cosine_theta = dot_product / (magnitude_ba * magnitude_bc)
    # Clamping to make sure angle stays between -1 and 1
    cosine_theta = max(min(cosine_theta, 1.0), -1.0)
    return math.acos(cosine_theta)

# CALCULATING THE FINGER DISTANCES (WHOLE FINGER - TOP HALF OF FINGER)

def finger_dist_curl(tip, mid, base):

    tip_to_base = math.sqrt(
        (base.x - tip.x) ** 2 +
        (base.y - tip.y) ** 2 +
        (base.z - tip.z) ** 2
    )

    mid_to_tip = math.sqrt(
        (mid.x - tip.x) ** 2 +
        (mid.y - tip.y) ** 2 +
        (mid.z - tip.z) ** 2
    )

    return tip_to_base - mid_to_tip

# Values now range between 0-1: values below 0 become 0 and values above max_val become 1
def norm(x, max_val=0.25):
    return max(0, min(1, x / max_val))

# COMBINE ANGLE DATA WITH DISTANCE DATA

def get_finger_values(hand_landmarks):

    index_angle_1 = angle(
        hand_landmarks[5],
        hand_landmarks[6],
        hand_landmarks[8]
    )

    index_angle_2 = angle(
        hand_landmarks[6],
        hand_landmarks[7],
        hand_landmarks[8]
    )

    middle_angle_1 = angle(
        hand_landmarks[9],
        hand_landmarks[10],
        hand_landmarks[12]
    )

    middle_angle_2 = angle(
        hand_landmarks[10],
        hand_landmarks[11],
        hand_landmarks[12]
    )

    ring_angle_1 = angle(
        hand_landmarks[13],
        hand_landmarks[14],
        hand_landmarks[16]
    )

    ring_angle_2 = angle(
        hand_landmarks[14],
        hand_landmarks[15],
        hand_landmarks[16]
    )

    pinky_angle_1 = angle(
        hand_landmarks[17],
        hand_landmarks[18],
        hand_landmarks[20]
    )

    pinky_angle_2 = angle(
        hand_landmarks[18],
        hand_landmarks[19],
        hand_landmarks[20]
    )

    # Find mean of angles
    index_angle = (index_angle_1 + index_angle_2) / 2
    middle_angle = (middle_angle_1 + middle_angle_2) / 2
    ring_angle = (ring_angle_1 + ring_angle_2) / 2
    pinky_angle = (pinky_angle_1 + pinky_angle_2) / 2

    # Norm of the mean of angles
    index_angle_norm = (min(1, max(0, index_angle / pi)))
    middle_angle_norm = (min(1, max(0, middle_angle / pi)))
    ring_angle_norm = (min(1, max(0, ring_angle / pi)))
    pinky_angle_norm = (min(1, max(0, pinky_angle / pi)))

    index_curl = finger_dist_curl(
        hand_landmarks[8],
        hand_landmarks[6],
        hand_landmarks[5]
    )

    middle_curl = finger_dist_curl(
        hand_landmarks[12],
        hand_landmarks[10],
        hand_landmarks[9]
    )

    ring_curl = finger_dist_curl(
        hand_landmarks[16],
        hand_landmarks[14],
        hand_landmarks[13]
    )

    pinky_curl = finger_dist_curl(
        hand_landmarks[20],
        hand_landmarks[18],
        hand_landmarks[17]
    )

    # Finding norm of distance values
    index_norm = norm(index_curl)
    middle_norm = norm(middle_curl)
    ring_norm = norm(ring_curl)
    pinky_norm = norm(pinky_curl)

    # Combine angles with distance (and compute for each separate finger)
    # The weights were chosen as the best balance between the angle data and distance data
    # Weights were adjusted during testing of the system
    index_value = 0.45 * index_angle_norm + 0.55 * index_norm
    middle_value = 0.45 * middle_angle_norm + 0.55 * middle_norm
    ring_value = 0.3 * ring_angle_norm + 0.7 * ring_norm
    pinky_value = 0.3 * pinky_angle_norm + 0.7 * pinky_norm

    return (
        index_value,
        middle_value,
        ring_value,
        pinky_value
    )

# HAND LANDMARK DETECTION FOR BUTTONS

def hand_pressing_button(hand_landmarks,
                         x_min,
                         y_min,
                         x_max,
                         y_max,
                         w,
                         h,
                         threshold = 0.1):
    count = 0

    for landmark in hand_landmarks:
        x = int(landmark.x * w)  # Width of frame
        y = int(landmark.y * h)  # Height of frame

        if x_min <= x <= x_max and \
                y_min <= y <= y_max:
            count += 1

    return (count / 21) >= threshold


def check_menu_buttons(
        hand_landmarks,
        w,
        h
):

    hand_over_pbutton = False
    hand_over_pobutton = False

    pbutton_x_min = 450
    pbutton_x_max = 600
    pbutton_y_min = 190
    pbutton_y_max = 240

    pobutton_x_min = 450
    pobutton_x_max = 600
    pobutton_y_min = 300
    pobutton_y_max = 350

    for hand_landmarks in hand_landmarks:

        if hand_pressing_button(hand_landmarks,
                                pbutton_x_min, pbutton_y_min,
                                pbutton_x_max, pbutton_y_max,
                                w, h):
            hand_over_pbutton = True

        if hand_pressing_button(hand_landmarks,
                                pobutton_x_min, pobutton_y_min,
                                pobutton_x_max, pobutton_y_max,
                                w, h):
            hand_over_pobutton = True

    return hand_over_pbutton, hand_over_pobutton


def check_back_button(
        hand_landmarks,
        w,
        h,
        backbutton_pressed,
        mode,
        random_note
):

    hand_over_backbutton = False

    backbutton_x_min = 0
    backbutton_x_max = 85
    backbutton_y_min = 430
    backbutton_y_max = 470

    for hand_landmarks in hand_landmarks:

        if hand_pressing_button(hand_landmarks,
                                backbutton_x_min, backbutton_y_min,
                                backbutton_x_max, backbutton_y_max,
                                w, h):
            hand_over_backbutton = True

    if hand_over_backbutton and not backbutton_pressed:
        mode = "menu"
        random_note = None
        backbutton_pressed = True

    if not hand_over_backbutton:
        backbutton_pressed = False

    return hand_over_backbutton, backbutton_pressed, mode, random_note


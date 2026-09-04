# PRACTICE MODULE
# This file is used for the practice mode only. It checks 
# whether the detected finger position matches the random note
# generated from the flute fingering module.

import time
import random

# CHECKING WHETHER DETECTED FINGER POSITIONS MATCH THE TARGET NOTE

def check_note(
        binary_values,
        random_note,
        condition,
        correct_time,
        flute_fingerings,
        notes
):

    if len(binary_values) != 8:
        return condition, correct_time, random_note

    # Counting how many of the 8 detected finger positions match the finger
    # positions required for the target note
  
    close_match = sum(
        binary_values[i] == flute_fingerings[random_note][i]
        for i in range(8)
    )

    if condition == "waiting":

        # Allowing one finger position to be incorrect while still considering the note a match
        # This is because, in testing, the right pinky finger would sometimes be tracked wrong
        # due to it only being partially visible. For most notes, the right pinky does not 
        # determine the note itself, but helps maintain the correct pitch. Therefore, the system can
        # tolerate an error in this finger position without significantly affecting note identification.
      
        if close_match >= 7:
            condition = "correct"
            correct_time = time.time()

    if condition == "correct":

        # Have to keep the correct state for three seconds before generating a new random target note
        if time.time() - correct_time > 3:
            random_note = random.choice(notes)
            condition = "waiting"

    return condition, correct_time, random_note

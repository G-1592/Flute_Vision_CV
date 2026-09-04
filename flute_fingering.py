# FLUTE FINGERING MODULE
# This file determines the note names and note fingering positions
# for beginner practice. It also generates random notes for practice mode.

import random

# NOTE NAMES USED FOR BEGINNER PRACTICE

notes = [
    "C3",
    "D4",
    "E4",
    "F4",
    "G4",
    "A4",
    "B4",
    "C4",
    "G4 #",
    "B4 flat",
    "F4 #",
    "D4 #",
    "C3 #"
]

# FLUTE FINGERING POSITIONS FOR BEGINNER PRACTICE
# Each list represents the required finger positions for each note
# 0 = finger is bent (pressing on the key)
# 1 = finger is straight (not pressing on the key)

# Note that C3 and B4 have the same fingering position. This is because the thumb (behind the flute) changes the pitch.
# This is an intentional limitation of the project as the project investigates how accurately you can identify correct note
# finger positioning without audio input.
# The unseen thumb position limits this accuracy.

flute_fingerings = {

    "C3": [
        0, 1, 1, 1,
        1, 1, 1, 0
    ],

    "B4": [
        0, 1, 1, 1,
        1, 1, 1, 0
    ],

    "D4": [
        0, 0, 0, 1,
        0, 0, 0, 1
    ],

    "E4": [
        0, 0, 0, 1,
        0, 0, 1, 0
    ],

    "F4": [
        0, 0, 0, 1,
        0, 1, 1, 0
    ],

    "G4": [
        0, 0, 0, 1,
        1, 1, 1, 0
    ],

    "A4": [
        0, 0, 1, 1,
        1, 1, 1, 0
    ],

    "C4": [
        0, 0, 0, 1,
        0, 0, 0, 0
    ],

    "D4 #": [
        0, 0, 0, 1,
        0, 0, 0, 0
    ],

    "F4 #": [
        0, 0, 0, 1,
        1, 1, 0, 0
    ],

    "G4 #": [
        0, 0, 0, 0,
        1, 1, 1, 0
    ],

    "B4 flat": [
        0, 1, 1, 1,
        0, 1, 1, 0
    ],

    "C3 #": [
        1, 1, 1, 1,
        1, 1, 1, 0
    ]
}

# GETTING THE RANDOM NOTE FOR PRACTICE MODE

def get_random_note():
    return random.choice(notes)

# Flute_Vision_CV
A real-time computer vision system for flute fingering, posture, and embouchure analysis, without relying on audio input.

## About
As a flute player of ten years, I know how challenging flute fingerings and embouchure (mouth position) can be for beginners. That's what inspired me to build a system focused on helping users develop these foundational techniques. But, instead of relying on audio analysis, I wanted to push myself to see if computer vision alone could meaningfully analyse flute performance. The system uses hand and face landmark detection to analyse beginner technique and was designed with use on a music stand in mind.

## Demo Video

## How it works

## Key features
**Calibration system** - Sets user-specific finger bend thresholds using angle and distance data.

**Practice mode** - Checks real-time finger position accuracy for each flute note using hand tracking and hold-to-confirm validation. Optimised for beginner one-octave practice.

**Posture mode** - Tracks embouchure and head alignment using face tracking.

**Gesture-controlled buttons** - Easy touch-free navigation between different modes.

Designed for use on a music stand.

## Screenshots
<table>
  <tr>
    <td align="center">
      <img src="https://github.com/user-attachments/assets/073c5ab9-5891-45ab-a8d5-a5464488e194" width="250">
      <br> Practice Mode 
      </td>
    <td align="center">
      <img src="https://github.com/user-attachments/assets/a0100416-095f-4aae-adb5-9ebeea77826c" width="250">
      <br> Calibration System
      </td>
    <td align="center">
      <img src="https://github.com/user-attachments/assets/f2f0c4cd-d0a2-4bf9-b8cc-78b1cd1a22d3" width="250">
      <br> Face Landmark Analysis
      </td>
    <td align="center">
      <img src="https://github.com/user-attachments/assets/96e35cbe-32cc-468f-8712-a039010ca02e" width="250">
      <br> Posture Mode
      </td>
  </tr>
</table>

## Installing the system

1. ### Required Libraries
   - OpenCV
   - MediaPipe
   - NumPy
     
   Install the required libraries using:
   ```bash
   pip install opencv-python mediapipe numpy
   ```

2. ### Required Model Files
   The system also requires the official MediaPipe Hand Landmarker and Face Landmarker model files:
   - hand_landmarker.task
   - face_landmarker.task
   
   Place both files in the main project directory.

3. ### Running the system
   Once the libraries and model files are installed:
   
   **Using an IDE:** Run `main.py`.
   
   **Using the terminal:** 
    ```bash
   python main.py
    ```

## Acknowledgements


## Future improvements/ findings






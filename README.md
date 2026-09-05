# Flute_Vision_CV
A real-time computer vision system for flute fingering, posture, and embouchure analysis, without relying on audio input.

## About
As a flute player of ten years, I know how challenging flute fingerings and embouchure (mouth position) can be for beginners. That's what inspired me to build a system focused on helping users develop these foundational techniques. But, instead of relying on audio analysis, I wanted to push myself to see if computer vision alone could meaningfully analyse flute performance. The system uses MediaPipe hand and face landmark detection to analyse beginner technique and was designed with use on a music stand in mind.

## Demo Video

## How it works
The system uses MediaPipe hand and face landmark detection to track the player's movements in real time. Hand landmarks are used to calculate finger angles and distances, which are compared against personalised thresholds established during calibration. Face landmarks are used to analyse head alignment and embouchure visual technique. The system then provides real-time feedback through the different practice and posture modes.

## Key features
**Calibration system** - Sets user-specific finger bend thresholds using angle and distance data.

**Practice mode** - Checks real-time finger position accuracy for each flute note using hand tracking and hold-to-confirm validation. Optimised for beginner one-octave practice.

**Posture mode** - Tracks embouchure and head alignment using face tracking.

**Gesture-controlled buttons** - Easy touch-free navigation between different modes.

🎵 Designed for use on a music stand.

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
   - hand_landmarker.task - available from the [MediaPipe Hand Landmarker documentation](https://ai.google.dev/edge/mediapipe/solutions/vision/hand_landmarker/python)
   - face_landmarker.task - available from the [MediaPipe Face Landmarker documentation](https://ai.google.dev/edge/mediapipe/solutions/vision/face_landmarker/python)
   
   Place both files in the main project directory.

3. ### Running the system
   Once the libraries and model files are installed:
   
   **Using an IDE:** Run `main.py`.
   
   **Using the terminal:** 
    ```bash
   python main.py
    ```

## Acknowledgements
- [MediaPipe](https://ai.google.dev/edge/mediapipe/solutions/guide) for the hand and face landmark detection tools and models used in this project.

## Findings
The aim of this project was to see how meaningfully computer vision alone can analyse live flute performance. The results were more accurate than I initally expected! 

However, without audio input, there were several limitations. For example, distinguishing between certain notes can be difficult when the relevant fingering information is not visible to the camera. This was especially prevalent with notes C3 and B4 as the thumb behind the flute (which is responsible for changing the pitch) is unseen.

I also found that the right pinky finger was sometimes not detected fully. Although this did not significantly change the recognition of most notes tested, it did reduce the accuracy for detecting D sharp as this is the only note that relies on the right pinky finger to change pitch.

However, the posture mode was accurate most of the time across several tests. The system's embouchure analysis was tested alongside a tuner, which was used to verify whether the embouchure was good or bad. 

Overall, the project demonstrated that computer vision can provide meaningful information about aspects of flute technique without relying on audio - perhaps more than once thought. But, the project also highlights the limitations of using visual information alone for flute in particular. 





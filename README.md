# Smart Exercise
In this application we are using Mediapipe for detecting sports gestures and opencv for webcam reading and StreamLit for creating the Web Graphical User Interface (GUI)


## Overview 
![alt Text](https://github.com/meysamraz/Smart_Exercise/blob/master/src/test.mp4)

Using the key points that we extract from the MediaPipe and calculating the Angle between keypoints, we can detect the movements and with a few conditions we can track them Three moves are detected, you can enter the number you want to do that move and the program detects how many times you did that move to reach the desired number

![alt-text-1](https://github.com/meysamraz/Smart_Exercise/blob/master/src/side_arises.jpg "Side Arises") ![alt-text-2](https://github.com/meysamraz/Smart_Exercise/blob/master/src/standing_cruls.jpg "Standing Cruls") ![alt-text-3](https://github.com/meysamraz/Smart_Exercise/blob/master/src/squats.jpg "Squats")

## Run The Project 

### Install Libraries
'''1- pip install pip install -r requirements.txt'''
### Run 
'''2- streamlit run home_page.py'''

##  Libraries used in the project

- [streamlit](https://streamlit.io/)
- [opencv](https://opencv.org/)
- [mediapipe](https://google.github.io/mediapipe/)
- [numpy](https://numpy.org/)




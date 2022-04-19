# Smart Exercise
In this application we are using Mediapipe for detecting sports movement gestures and opencv for webcam reading and StreamLit for creating the Web Graphical User Interface (GUI)


## Overview 

<video width="320" height="240" controls>
  <source src="src/test2.mp4" type="video/mp4">
</video>

Using the key points that we extract from the MediaPipe and calculating the Angle between keypoints, we can detect the movements and with a few conditions we can track them Three moves are detected, you can enter the number you want to do that move and the program detects how many times you did that move to reach the desired number , This App can Track Three movement (side raises, standing_cruls, squats) 


<img src = "src/side_arises.jpg" width ="230" /> <img src = "src/standing_cruls.jpg" width ="230" /> <img src = "src/squats.jpg" width ="230" />


## Run The Project 

### Install Libraries

```pip install pip install -r requirements.txt```

### Run 

```streamlit run home_page.py```

##  Libraries used in the project

- [streamlit](https://streamlit.io/)
- [opencv](https://opencv.org/)
- [mediapipe](https://google.github.io/mediapipe/)
- [numpy](https://numpy.org/)




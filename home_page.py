import streamlit as st
import mediapipe as mp
from PIL import Image
import numpy as np
import time
import cv2

mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

# user position
stage = None

# count of correct movement
counter = 0

@st.cache()
def image_resize(image, width=None, height=None, inter=cv2.INTER_AREA):
    """this function resize image according to image shape

    Args:
        image  : input image 
        width  : image width. Defaults to None.
        height : image height Defaults to None.
        inter : image inter. Defaults to cv2.INTER_AREA.

    Returns: resized image 
    """
    
    dim = None
    (h, w) = image.shape[:2]

    if width is None and height is None:
        return image

    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)

    else:
        r = width / float(w)
        dim = (width, int(h * r))

    resized = cv2.resize(image, dim, interpolation=inter)

    return resized

def calculate_angle(a,b,c):
    """this function get three extracted point from mediapipe pose detection 
       and calculate the angle between them

    Args:
        a : first point
        b : middle point
        c : end point

    Returns: alculated angle 
    """
    a = np.array(a) 
    b = np.array(b) 
    c = np.array(c) 
    
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)
    
    if angle >180.0:
        angle = 360-angle
        
    return angle 

def get_pos(img,results):
    """this function loop intro pose MinMaxed keypoints value 
       multiplies them by height and width and return (x,y) according 
       to image height and width

    Args:
        img : input (image or video)
        results : detected pose

    Returns: landmarks position
    """
    landmarks = []
    for id,lm in enumerate(results.pose_landmarks.landmark) :
                h ,w,c = img.shape
                cx , cy = int(lm.x*w) , int(lm.y*h)
                landmarks.append([id,cx,cy])
    return landmarks    

st.title('Smart Exercise using MediaPipe')

st.markdown(
    """
    <style>
    [data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
        width: 350px;
    }
    [data-testid="stSidebar"][aria-expanded="false"] > div:first-child {
        width: 350px;
        margin-left: -350px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.sidebar.title('Smart Exercise using MediaPipe and Streamlit')

app_mode = st.sidebar.selectbox('',['Training','About App'])

if app_mode =='About App':
    
    st.markdown('In this application we are using Mediapipe for detecting sports gestures and opencv for webcam reading  and StreamLit for creating the Web Graphical User Interface (GUI)')
    st.markdown(
    """
    <style>
    [data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
        width: 400px;
    }
    [data-testid="stSidebar"][aria-expanded="false"] > div:first-child {
        width: 400px;
        margin-left: -400px;
    }
    </style>
    """,
    unsafe_allow_html=True,
    )
  
    side_arises_img = Image.open('src/side_arises.jpg')
    standing_cruls_img = Image.open('src/standing_cruls.jpg')
    squats_img = Image.open('src/squats.jpg')
    
    angle_img  =  Image.open('src/angle.png')
    pose_img  =  Image.open('src/pose.png')


    first_left_img, first_right_img = st.columns(2)
    first_left_img.image(pose_img)
    first_right_img.image(angle_img)
    
    st.markdown("Using the key points that we extract from the MediaPipe and calculating the Angle between keypoints, we can detect the movements and with a few conditions we can track them .\n Three moves are detected, you can enter the number you want to do that move and the program detects how many times you did that move to reach the desired number")   
    secend_left_img, second_center_img, second_right_img = st.columns(3)
    secend_left_img.image(side_arises_img, caption='Side Arises')
    second_center_img.image(standing_cruls_img, caption='Standing Cruls')
    second_right_img.image(squats_img, caption='Squats')
    
    st.markdown('''
          # About Me \n 
            Hey this is **Meysam Raz** from data scientist intrested in Computer vision, Natural language processing, Brain Computer Interface (BCI) . \n
                       
            Also check us out my Links
            - [Github](https://github.com/meysamraz)
            - [LinkedIn](https://www.linkedin.com/in/meysamraz/)
            - [Kaggle](https://www.kaggle.com/meisamraz)
            ''')
    
elif app_mode =='Training':
    st.set_option('deprecation.showfileUploaderEncoding', False)
          
    left, center, right = st.columns(3)

    left_one = left.button("side arises")
    center_one = center.button("standing cruls")
    right_one = right.button("squats")
    
    press_time = st.select_slider(
                'How much do you want to press',
                options=['0', '5', '10', '15', '20', '25', '30'])

    record = st.sidebar.checkbox("Record capeo")
    if record:
        st.checkbox("Recording", value=True)

    st.markdown(
    """
    <style>
    [data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
        width: 400px;
    }
    [data-testid="stSidebar"][aria-expanded="false"] > div:first-child {
        width: 400px;
        margin-left: -400px;
    }
    </style>
    """,unsafe_allow_html=True,)
    
    st.sidebar.markdown('---')
    
    detection_confidence = st.sidebar.slider('Min Detection Confidence', min_value =0.0,max_value = 1.0,value = 0.5)
    tracking_confidence = st.sidebar.slider('Min Tracking Confidence', min_value = 0.0,max_value = 1.0,value = 0.5)

    st.sidebar.markdown('---')

    st.markdown(' ## Your Video')

    stframe = st.empty()

    cap = cv2.VideoCapture(0) 
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps_input = int(cap.get(cv2.CAP_PROP_FPS))
    fps = 0
    i = 0

    ltitle, ctitle, rtitle = st.columns(3)

    with ltitle:
        st.markdown("**Frame Rate**")
        kpi1_text = st.markdown("0")

    with ctitle:
        st.markdown("**Count**")
        kpi2_text = st.markdown("0")

    with rtitle:
        st.markdown("**Target**")
        kpi3_text = st.markdown("0")
   
    st.markdown("<hr/>", unsafe_allow_html=True)
    
    with mp_pose.Pose(static_image_mode=True,min_detection_confidence=detection_confidence,min_tracking_confidence=tracking_confidence) as pose :
        prevTime = 0
        
        while cap.isOpened():
            i +=1
            ret, frame = cap.read()
            if not ret:
                continue

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            result = pose.process(frame)
            try : 
                landmarks =  get_pos(frame,result)
                
                rshoulder = landmarks[12][1:]
                relbow = landmarks[14][1:]
                rwrist = landmarks[16][1:]
                
                lshoulder = landmarks[11][1:]
                lelbow      = landmarks[13][1:]
                lwrist  = landmarks[15][1:]
                
                rhip = landmarks[24][1:]
                rknee      = landmarks[26][1:]
                rankle  = landmarks[28][1:]
                
                lhip = landmarks[23][1:]
                lknee      = landmarks[25][1:]
                lankle  = landmarks[27][1:] 
                
                angle_right_elbow = calculate_angle(rshoulder,relbow,rwrist)
                angle_left_elbow = calculate_angle(lshoulder,lelbow,lwrist)
                
                angle_right_knee = calculate_angle(rhip,rknee,rankle)
                angle_left_knee = calculate_angle(lhip,lknee,lankle)
                
                angle_right_shoulder = calculate_angle(rwrist,rshoulder,rhip)
                angle_left_shoulder = calculate_angle(lwrist,lshoulder,lhip)
                
                if center_one :
                    if angle_left_elbow >= 165 and angle_right_elbow >= 165 and angle_right_knee >= 173 and angle_left_knee >= 173 :
                        stage = "open"
                    elif  angle_left_elbow  <=  34  and  angle_right_elbow <=  34  and  angle_right_knee >= 173  and  angle_left_knee >= 173 and stage == "open" :
                        stage="close"
                        counter +=1
                        
                if left_one :   
                    if angle_right_shoulder >= 122 and angle_left_shoulder >= 122 :
                        stage = "up"
                    if 19 >= angle_right_shoulder   and 19 >= angle_left_shoulder and stage == 'up'  :
                        stage="down"
                        counter  +=1
                        
                if right_one :
                    if angle_left_elbow <= 58 and angle_right_elbow <= 58 and angle_right_knee >= 173 and angle_left_knee >= 173 :
                        stage = "up"
                    elif  angle_left_elbow  <=  58  and  angle_right_elbow <=  58  and  angle_right_knee <= 51  and  angle_left_knee <= 51 and stage == 'up':
                        stage = "down"
                        counter +1
                                                
                if counter == int(press_time) :                                  
                    counter = 0
                    # empty all clicked value after reaching target
                    left_one = False
                    center_one = False
                    right_one = False
            except :
                pass    
            
            mp_drawing.draw_landmarks(frame,result.pose_landmarks,mp_pose.POSE_CONNECTIONS)
            currTime = time.time()
            # extract fps from webcam
            fps = 1 / (currTime - prevTime)
            prevTime = currTime
 
            kpi1_text.write(f"<h1 style='text-align: left; color: red;'>{int(fps)}</h1>", unsafe_allow_html=True)
            kpi2_text.write(f"<h1 style='text-align: left; color: red;'>{counter}</h1>", unsafe_allow_html=True)
            kpi3_text.write(f"<h1 style='text-align: left; color: red;'>{press_time}</h1>", unsafe_allow_html=True)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame,(0,0),fx = 0.8 , fy = 0.8)
            frame = image_resize(image = frame, width = 640)
            stframe.image(frame,channels = 'BGR',use_column_width=True)

    cap.release()
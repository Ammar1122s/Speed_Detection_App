import imutils as imutils
import numpy as np
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.screen import Screen
from kivymd.uix.button import MDFlatButton
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from collections import deque
import cv2
import time
from kivy.utils import platform
# declaration of variables


changeInTime = 0
changeInDistance = 0

listDistance = []
listSpeed = []

known_distance = 5.0  # Example: 10 feet

# Known ball size in pixels (adjust according to your scenario)
known_ball_size = 30.0  # Example: 30 pixels

# This is the distance from camera to face object
DECLARED_LEN = 30 # cm
# width of the object face
DECLARED_WID = 14.3 # cm
# Definition of the RGB Colors format
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
#Defining the fonts family, size, type
fonts = cv2.FONT_HERSHEY_COMPLEX
# calling the haarcascade_frontalface_default.xml module for face detection.
face_detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

averageSpeed1=0


screen_helper = """
ScreenManager:
    id: screen_manager
    Screen:
        name: 'home'
        MDBoxLayout:
            orientation: 'vertical'
            MDTopAppBar:
                title: 'Velo'
                pos_hint: {'top': 1}
                md_bg_color: (102 / 255, 255 / 255, 102 / 255, 1)
                anchor_title: 'left'
                right_action_items: [['dots-vertical',lambda x: setattr(screen_manager, 'current', 'setting')]]
                elevation: 1
            Image:
                source: 'logo1.png'
                size_hint: (0.85, 1)
                pos_hint: {'center_x': 0.5, 'center_y': 0.6}
            MDBoxLayout:
                orientation: 'vertical'
                spacing: dp(10)  # Adjust the top and bottom spacing here
                padding: dp(10), dp(10), dp(10), dp(20)
                MDFlatButton:
                    text: 'LIVE'
                    theme_text_color: 'Custom'
                    text_color: (1, 1, 1, 1)
                    font_size: '30dp'
                    font_name: 'fonts/mesquin-italic'
                    md_bg_color: (102 / 255, 255 / 255, 102 / 255, 1)
                    pos_hint: {'center_x': 0.5,}
                    size_hint: (0.6, 0.07)
                    on_release: 
                        app.live_camera() 
                        screen_manager.current = 'Live'
                MDFlatButton:
                    text: 'LOAD'
                    theme_text_color: 'Custom'
                    text_color: (1, 1, 1, 1)
                    font_size: '30dp'
                    font_name: 'fonts/mesquin-italic'
                    md_bg_color: (102 / 255, 255 / 255, 102 / 255, 1)
                    size_hint: (0.6, 0.07)
                    pos_hint: {'center_x': 0.5,}
                MDFlatButton:
                    text: 'HOW TO USE'
                    theme_text_color: 'Custom'
                    text_color: (1, 1, 1, 1)
                    font_size: '30dp'
                    font_name: 'fonts/mesquin-italic'
                    md_bg_color: (102 / 255, 255 / 255, 102 / 255, 1)
                    size_hint: (0.6, 0.07)
                    pos_hint: {'center_x': 0.5,}
                    on_release: screen_manager.current = 'how_to_play'
                MDFlatButton:
                    text: 'SUBSCRIBE!'
                    theme_text_color: 'Custom'
                    text_color: (1, 1, 1, 1)
                    font_size: '30dp'
                    font_name: 'fonts/mesquin-italic'
                    md_bg_color: (255 / 255, 133 / 255, 51 / 255, 1)
                    size_hint: (0.6, 0.07)
                    pos_hint: {'center_x': 0.5,}
                    
    Screen:
        name: 'how_to_play'
        BoxLayout:
            orientation: 'vertical'
            padding: dp(10), dp(10), dp(10), dp(20)
            MDTopAppBar:
                title: 'How to Play'
                pos_hint: {'top': 1}
                md_bg_color: (102 / 255, 255 / 255, 102 / 255, 1)
                anchor_title: 'left'
                left_action_items: [['arrow-left', lambda x: setattr(screen_manager, 'current', 'home')]]
                elevation: 1
            Image:
                source: 'howtouse.jpeg'
                size_hint: (1, 1)
    Screen:
        name: 'setting'
        BoxLayout:
            padding: dp(10), dp(10), dp(10), dp(20)
            MDTopAppBar:
                title: 'Settings'
                pos_hint: {'top': 1}
                md_bg_color: (102 / 255, 255 / 255, 102 / 255, 1)
                anchor_title: 'left'
                left_action_items: [['arrow-left', lambda x: setattr(screen_manager, 'current', 'home')]]
                elevation: 1 
        
        MDSlider:
            id: slider
            min: 0
            max: 100
            value: 50
            pos_hint: {'center_x': 0.5,'center_y':0.75}
            color: "orange"
            thumb_color_active: "orange"
            thumb_color_inactive: "orange"
            hint:False
              
        MDLabel:
            text: 'Pitch Distance'
            font_style: 'H6'
            halign: 'center'
            pos_hint: {'center_x': 0.5,'center_y':0.8}
       
        MDTextField:
            hint_text: str(int(slider.value))
            size_hint_x: None
            width: '200dp'
            pos_hint: {'center_x': 0.5, 'center_y':0.65}
        
        MDAnchorLayout:
            anchor_x:"center"
            anchor_y:"center"
            MDBoxLayout:
                size_hint:0.5,0
                spacing:dp(20)
                
                MDFlatButton:
                    text:"45.0 FEET"
                    md_bg_color: (102 / 255, 255 / 255, 102 / 255, 1)
                MDFlatButton:
                    text:"65.0 FEET"
                    md_bg_color: (102 / 255, 255 / 255, 102 / 255, 1)
                    
    Screen:
        name:"Live"
        MDBoxLayout:
            orientation:"vertical"
            spacing: dp(10)
            MDTopAppBar:
                title: 'Live Camera'
                pos_hint: {'top': 1}
                md_bg_color: (102 / 255, 255 / 255, 102 / 255, 1)
                anchor_title: 'left'
                left_action_items: [['arrow-left', lambda x: (setattr(screen_manager, 'current', 'home'), app.release())]]
                elevation: 1 
            MDFlatButton:
                text: 'Check the Speed'
                theme_text_color: 'Custom'
                text_color: (1, 1, 1, 1)
                font_size: '30dp'
                font_name: 'fonts/mesquin-italic'
                md_bg_color: (255 / 255, 133 / 255, 51 / 255, 1)
                size_hint: (0.8, 0.09)
                pos_hint: {'center_x': 0.4,}
                on_release: 
                    app.check_speed()
            
            MDFlatButton:
                text: 'Clear Speed'
                theme_text_color: 'Custom'
                text_color: (1, 1, 1, 1)
                font_size: '30dp'
                font_name: 'fonts/mesquin-italic'
                md_bg_color: (255 / 255, 133 / 255, 51 / 255, 1)
                size_hint: (0.8, 0.09)
                pos_hint: {'center_x': 0.4,}
                on_release: 
                    app.clear()
                    
                    
            Image:
                id: image_widget
            MDLabel:
                id:label_id
                text:""
                size_hint: (0.5, 0.6)
                pos_hint: {'center_x': 0.5}
            
                                            
"""

class Velo(MDApp):


    def build(self):
        global screen
        screen = Builder.load_string(screen_helper)
        self.initialTime = 0
        self.initialDistance = 0
        self.previous_center = None
        self.previous_time = time.time()
        self.averageSpeed = 0.0
        self.check = False
        return screen
    def on_switch_active(self, active):
        if active:
            print("Switch is ON")
        else:
            print("Switch is OFF")
    def release(self):
        self.capture.release()
    def check_speed(self):
        num = round(self.averageSpeed, 4)
        label = screen.ids.label_id
        label.text = "Speed in mph is "+str(num)
        self.averageSpeed = 0
        listSpeed.clear()

    def clear(self):
        self.averageSpeed = 0
        listSpeed.clear()
        label = screen.ids.label_id
        label.text = "Speed in mph is 0.00"




    def live_camera(self):
        # layout = MDBoxLayout(orientation="vertical")
        # self.image = Image()
        # layout.add_widget(self.image)
        # layout.add_widget(MDFlatButton(text="Click on me!"))

        # if platform == 'android':
        #     from android.permissions import request_permissions, Permission
        #     request_permissions([Permission.CAMERA], self.permission_granted)

   # def permission_granted(self):

        self.image = screen.ids.image_widget
        self.capture = cv2.VideoCapture(0,  cv2.CAP_DSHOW)
        Clock.schedule_interval(self.load_video, 1.0/30.0)


    def load_video(self, *args):
        averageDistance = 0.1
        ret, frames = self.capture.read()
        self.image_frame = frames

        ball_width = 7.6
        if frames is not None:
            blurred = cv2.GaussianBlur(frames, (11,11), 0)
            hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
            # sensitivity = 15
            # lower_white = np.array([0,0,255-sensitivity])
            # upper_white = np.array([255,sensitivity,255])

            lower_white = (29, 86, 6)
            upper_white = (64, 255, 255)
            pts = deque(maxlen=64)

            mask = cv2.inRange(hsv, lower_white, upper_white)
            mask = cv2.erode(mask, None, iterations=3)
            mask = cv2.dilate(mask, None, iterations=3)

            cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cnts = imutils.grab_contours(cnts)
            center = None


            if len(cnts) > 0:
                c = max(cnts, key=cv2.contourArea)
                ((x, y), radius) = cv2.minEnclosingCircle(c)
                M = cv2.moments(c)
                center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])

                if radius > 10:
                    cv2.circle(frames, (int(x), int(y)), int(radius),
                               (0, 255, 255), 4)
                    cv2.circle(frames, center, 5, (0, 0, 255), -1)

                if self.previous_center is not None:
                    displacement = ((cx - self.previous_center[0]) ** 2 + (cy - self.previous_center[1]) ** 2) ** 0.5
                    time_elapsed = time.time() - self.previous_time

                    speed = (displacement * 0.000008) / (time_elapsed / 3600)

                    listSpeed.append(speed)
                    self.averageSpeed = self.averageFinder(listSpeed, 10)


                self.previous_center = (cx, cy)
                self.previous_time = time.time()


        # if (len(cnts) == 0):
        #     cv2.line(frames, (45, 70), (235, 70), (0, 255, 0), 35)
        #     cv2.line(frames, (45, 70), (235, 70), (255, 255, 0), 32)
        #     cv2.line(frames, (45, 70), (235, 70), (0, 0, 0), 22)
        #     cv2.putText(frames, f"Speed: {round(self.averageSpeed, 2)} mph", (50, 75), fonts, 0.6, (0, 255, 220), 2)


            pts.appendleft(center)

            for i in range(1, len(pts)):
                if pts[i - 1] is None or pts[i] is None:
                    continue
                thickness = int(np.sqrt(64 / float(i + 1)) * 2.5)
                cv2.line(frames, pts[i - 1], pts[i], (0, 0, 255), thickness)


            buffer = cv2.flip(frames, 0).tobytes()
            texture = Texture.create(size=(frames.shape[1], frames.shape[0]), colorfmt='bgr')
            texture.blit_buffer(buffer, colorfmt='bgr', bufferfmt='ubyte')
            self.image.texture = texture




    def averageFinder(self, completeList, averageOfItems):
        lengthOfList = len(completeList)
        selectedItems = lengthOfList - averageOfItems
        selectedItemsList = completeList[selectedItems:]
        average = sum(selectedItemsList) / len(selectedItemsList)
        return average

Velo().run()

import imutils as imutils
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.screen import Screen
from kivymd.uix.button import MDFlatButton
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
import cv2
import time

# declaration of variables


changeInTime = 0
changeInDistance = 0

listDistance = []
listSpeed = []

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

Window.size = (360, 640)

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
            MDTopAppBar:
                title: 'Live Camera'
                pos_hint: {'top': 1}
                md_bg_color: (102 / 255, 255 / 255, 102 / 255, 1)
                anchor_title: 'left'
                left_action_items: [['arrow-left', lambda x: setattr(screen_manager, 'current', 'home')]]
                elevation: 1 
            Image:
                id: image_widget
            
                                            
"""

class Velo(MDApp):

    def build(self):
        global screen
        screen = Builder.load_string(screen_helper)
        self.initialTime = 0
        self.initialDistance = 0
        return screen
    def on_switch_active(self, active):
        if active:
            print("Switch is ON")
        else:
            print("Switch is OFF")

    def live_camera(self):
        # layout = MDBoxLayout(orientation="vertical")
        # self.image = Image()
        # layout.add_widget(self.image)
        # layout.add_widget(MDFlatButton(text="Click on me!"))

        self.image = screen.ids.image_widget
        self.capture = cv2.VideoCapture(0)
        Clock.schedule_interval(self.load_video, 1.0/30.0)



    def load_video(self, *args):
        averageDistance = 0.1
        ret, frames = self.capture.read()
        self.image_frame = frames




        # face_width_in_frame = self.face_data()
        # focal_length_found = self.focal_length(DECLARED_LEN, DECLARED_WID, 1524)
        # if face_width_in_frame != 0:
        #     Distance = self.distance_finder(focal_length_found, DECLARED_WID, face_width_in_frame)
        #     listDistance.append(Distance)
        #     averageDistance = self.averageFinder(listDistance, 2)
        #
        # distanceInMeters = averageDistance/100
        #
        # changeInTime =0.1
        # changeInDistance=0.1
        #
        #
        # if self.initialDistance != 0:
        #     # getting the  difference of the distances
        #     changeInDistance = distanceInMeters - self.initialDistance
        #     changeInTime = time.time() - self.initialTime
        #
        # speed = self.speedFinder(coveredDistance=changeInDistance, timeTaken=changeInTime)
        # listSpeed.append(speed)
        #
        # averageSpeed = self.averageFinder(listSpeed, 10)
        # if averageSpeed < 0:
        #         averageSpeed = averageSpeed * -1
        #
        # speedFill = int(45+(averageSpeed) * 130)
        # if speedFill > 235:
        #     speedFill = 235
        # cv2.line(frames, (45, 70), (235, 70), (0, 255, 0), 35)
        # cv2.line(frames, (45, 70), (speedFill, 70), (255, 255, 0), 32)
        # cv2.line(frames, (45, 70), (235, 70), (0, 0, 0), 22)
        # cv2.putText(frames, f"Speed: {round(averageSpeed*2.23694, 2)} mph", (50, 75), fonts, 0.6, (0, 255, 220), 2)
        #
        # self.initialTime = time.time()
        # self.initialDistance = distanceInMeters
        #
        # cv2.line(frames, (45, 25), (255, 25), (255, 0, 255), 30)
        # cv2.line(frames, (45, 25), (255, 25), (0, 0, 0), 22)
        # cv2.putText(
        #     frames, f"Distance = {round(distanceInMeters/1609,4)} m", (50, 30), fonts, 0.6, WHITE, 2)


        # blurred = cv2.GaussianBlur(frames, (11,11), 0)
        # hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
        # colorLower = (29, 86, 6)
        # colorUpper = (64, 255, 255)
        #
        # mask = cv2.inRange(hsv, colorLower, colorUpper)
        # mask = cv2.erode(mask, None, iterations=3)
        # mask = cv2.dilate(mask, None, iterations=3)
        #
        # cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # cnts = imutils.grab_contours(cnts)


        buffer = cv2.flip(frames, 0).tobytes()
        texture = Texture.create(size=(frames.shape[1], frames.shape[0]), colorfmt='bgr')
        texture.blit_buffer(buffer, colorfmt='bgr', bufferfmt='ubyte')
        self.image.texture = texture

    def face_data(self, *args):
        face_width = 0
        gray_image = cv2.cvtColor(self.image_frame, cv2.COLOR_BGR2GRAY)
        #We use 1.3 for less powerful processors but can increase it according to your processing power of your machine.
        faces = face_detector.detectMultiScale(gray_image, 1.3, 5)
        #getting the rectangular frame
        for (x, y, h, w) in faces:
            cv2.rectangle(self.image_frame, (x, y), (x + w, y + h), RED, 3)
            face_width = w
        return face_width

    def focal_length(self, determined_distance, actual_width, width_in_rf_image):
        focal_length_value = (width_in_rf_image * determined_distance) / actual_width
        return focal_length_value
    def distance_finder(self, focal_length, real_face_width, face_width_in_frame):
        distance = (real_face_width * focal_length) / face_width_in_frame
        return distance

    def averageFinder(self, completeList, averageOfItems):
        lengthOfList = len(completeList)
        selectedItems = lengthOfList - averageOfItems
        selectedItemsList = completeList[selectedItems:]
        average = sum(selectedItemsList) / len(selectedItemsList)
        return average

    def speedFinder(self,coveredDistance, timeTaken):

        speed = coveredDistance / timeTaken

        return speed



Velo().run()

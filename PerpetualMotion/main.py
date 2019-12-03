# ////////////////////////////////////////////////////////////////
# //                     IMPORT STATEMENTS                      //
# ////////////////////////////////////////////////////////////////

import math
import sys
import time
import threading
from threading import Thread
from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import *
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.slider import Slider
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.clock import Clock
from kivy.animation import Animation
from functools import partial
from kivy.config import Config
from kivy.core.window import Window
from pidev.kivy import DPEAButton
from pidev.kivy import PauseScreen
from time import sleep
import RPi.GPIO as GPIO
from pidev.stepper import stepper
from pidev.Cyprus_Commands import Cyprus_Commands_RPi as cyprus

c = 0
c1 = 0
c2 = ''
p = 0

# ////////////////////////////////////////////////////////////////
# //                      GLOBAL VARIABLES                      //
# //                         CONSTANTS                          //
# ////////////////////////////////////////////////////////////////
ON = False
OFF = True
HOME = True
TOP = False
OPEN = False
CLOSE = True
YELLOW = .180, 0.188, 0.980, 1
BLUE = 0.917, 0.796, 0.380, 1
DEBOUNCE = 0.1
rampSpeed = 0
INIT_RAMP_SPEED = 150
RAMP_LENGTH = 725


# ////////////////////////////////////////////////////////////////
# //            DECLARE APP CLASS AND SCREENMANAGER             //
# //                     LOAD KIVY FILE                         //
# ////////////////////////////////////////////////////////////////
class MyApp(App):
    def build(self):
        self.title = "Perpetual Motion"
        return sm


Builder.load_file('main.kv')
Window.clearcolor = (.1, .1, .1, 1)  # (WHITE)
cyprus.initialize()
cyprus.open_spi()

# ////////////////////////////////////////////////////////////////
# //                    SLUSH/HARDWARE SETUP                    //
# ////////////////////////////////////////////////////////////////
sm = ScreenManager()

ramp = stepper(port=0, speed=INIT_RAMP_SPEED)



# ////////////////////////////////////////////////////////////////
# //                       MAIN FUNCTIONS                       //
# //             SHOULD INTERACT DIRECTLY WITH HARDWARE         //
# ////////////////////////////////////////////////////////////////

# ////////////////////////////////////////////////////////////////
# //        DEFINE MAINSCREEN CLASS THAT KIVY RECOGNIZES        //
# //                                                            //
# //   KIVY UI CAN INTERACT DIRECTLY W/ THE FUNCTIONS DEFINED   //
# //     CORRESPONDS TO BUTTON/SLIDER/WIDGET "on_release"       //
# //                                                            //
# //   SHOULD REFERENCE MAIN FUNCTIONS WITHIN THESE FUNCTIONS   //
# //      SHOULD NOT INTERACT DIRECTLY WITH THE HARDWARE        //
# ////////////////////////////////////////////////////////////////
class MainScreen(Screen):
    version = cyprus.read_firmware_version()
    staircaseSpeedText = '0'
    rampSpeed = INIT_RAMP_SPEED
    staircaseSpeed = 40
    cyprus.set_servo_position(1, .6)

    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.initialize()

    def toggleGate(self):
        global c
        c = c + 1
        if c % 2 == 0:
            cyprus.set_servo_position(2, 0)

        else:
            cyprus.set_servo_position(2, .5)

        print("Open and Close gate here")

    def toggleStaircase(self):

        print("Turn on and off staircase here")

    def toggleRamp(self):

        global c1

        # //if ramp.get_position_in_units() > 530:
        # // ramp.start_relative_move(-500)
        # // print('%s' %ramp.get_position_in_units())
        # //elif ramp.get_position_in_units() < 30:
        # //  ramp.start_relative_move(500)
        print("here")
        if (cyprus.read_gpio() & 0b0010) == 0:
            ramp.set_as_home()
            print("hi")
        else:
            while (cyprus.read_gpio() & 0b0010 == 2):
                ramp.relative_move(-5)
                print("here2")
            if (cyprus.read_gpio() & 0b0010) == 0:
                ramp.set_as_home()
        while cyprus.read_gpio() & 0b0001 == 2:
            ramp.relative_move(5)
            sleep(0.1)

        print("Move ramp up and down here")

    def auto(self):
        print("Run through one cycle of the perpetual motion machine")

    def setRampSpeed(self, speed):
        self.rampSpeedLabel.text = 'Ramp Speed: %s' % str(self.ids.rampSpeed.value)
        ramp.set_speed(self.ids.rampSpeed.value)
        print("Set the ramp speed and update slider text")

    def setStaircaseSpeed(self, speed):

        self.staircaseSpeedLabel.text = 'Staircase Speed: %s' % str(self.ids.staircaseSpeed.value)
        cyprus.set_servo_position(1, self.ids.staircaseSpeed.value / 50)

        print("Set the staircase speed and update slider text")

    def initialize(self):
        print("Close gate, stop staircase and home ramp here")

    def resetColors(self):
        self.ids.gate.color = YELLOW
        self.ids.staircase.color = YELLOW
        self.ids.ramp.color = YELLOW
        self.ids.auto.color = BLUE

    def quit(self):
        print("Exit")
        MyApp().stop()


sm.add_widget(MainScreen(name='main'))

# ////////////////////////////////////////////////////////////////
# //                          RUN APP                           //
# ////////////////////////////////////////////////////////////////

MyApp().run()
cyprus.close_spi()

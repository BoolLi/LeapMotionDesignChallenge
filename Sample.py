################################################################################
# Copyright (C) 2012-2013 Leap Motion, Inc. All rights reserved.               #
# Leap Motion proprietary and confidential. Not for distribution.              #
# Use subject to the terms of the Leap Motion SDK Agreement available at       #
# https://developer.leapmotion.com/sdk_agreement, or another agreement         #
# between Leap Motion and you, your company or other organization.             #
################################################################################

import Leap, sys, thread, time
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture
from pymouse import PyMouse
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Cursor
import time
import math
import Demo


demo = Demo.Demo()



move_velocity = 100
minValue = 0.5

mpl.rcParams['legend.fontsize'] = 10

fig = plt.figure()
#ax = Axes3D(fig)
ax = fig.add_subplot(111, projection='3d')
x = []
y = []
z = []

# global variables for scaling
xMin = 0
xMax = 0
yMin = 0
yMax = 0
zMin = 0
zMax = 0
is_zoom_mode = False
curYPosition = 0

plt.ion()
plt.show()



#Smooths the mouse's position
class mouse_position_smoother(object):
    def __init__(self, smooth_aggressiveness, smooth_falloff):
        #Input validation
        if smooth_aggressiveness < 1:
            raise Exception("Smooth aggressiveness must be greater than 1.")
        if smooth_falloff < 1:
            raise Exception("Smooth falloff must be greater than 1.0.")
        self.previous_positions = []
        self.smooth_falloff = smooth_falloff
        self.smooth_aggressiveness = int(smooth_aggressiveness)
    def update(self, (x,y)):
        self.previous_positions.append((x,y))
        if len(self.previous_positions) > self.smooth_aggressiveness:
            del self.previous_positions[0]
        return self.get_current_smooth_value()
    def get_current_smooth_value(self):
        smooth_x = 0
        smooth_y = 0
        total_weight = 0
        num_positions = len(self.previous_positions)
        for position in range(0, num_positions):
            weight = 1 / (self.smooth_falloff ** (num_positions - position))
            total_weight += weight
            smooth_x += self.previous_positions[position][0] * weight
            smooth_y += self.previous_positions[position][1] * weight
        smooth_x /= total_weight
        smooth_y /= total_weight
        return smooth_x, smooth_y


mouse = PyMouse()

smooth_aggressiveness=60
smooth_falloff=1.001
mouse_position_smoother = mouse_position_smoother(smooth_aggressiveness, smooth_falloff)

class SampleListener(Leap.Listener):
    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']
    state_names = ['STATE_INVALID', 'STATE_START', 'STATE_UPDATE', 'STATE_END']

    def on_init(self, controller):
        print "Initialized"

    def on_connect(self, controller):
        print "Connected"

        # Enable gestures
        controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE);
        controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);

    def on_disconnect(self, controller):
        # Note: not dispatched when running in a debugger.
        print "Disconnected"

    def on_exit(self, controller):
        print "Exited"

    def on_frame(self, controller):
        # Get the most recent frame and report some basic information
        global x,y,z
        frame = controller.frame()

        for gesture in frame.gestures():
            if gesture.type == Leap.Gesture.TYPE_SWIPE:
                plt.cla()

        if demo.hasNewData() == True:
            x,y,z, color = demo.getData()
            ax.plot_surface(x, y, z, rstride=1, cstride=1, cmap = color, linewidth=0, antialiased=True)
            plt.draw()
            demo.consumeData()


        # Get hands
        for hand in frame.hands:

            handType = "Left hand" if hand.is_left else "Right hand"
            # Get the hand's normal vector and direction
            normal = hand.palm_normal
            direction = hand.direction
            position = hand.palm_position
            # Calculate the hand's pitch, roll, and yaw angles

            if checkPalm(hand):
                rotateGraph(hand)

            if checkFist(hand):
                zoomGraph(hand)
            else:
                finishZoom()

            if checkPointing(hand):             
                finger = hand.fingers[0]
                screen_to_choose = None
                position = None
                chosen_screen = False
                self.screens = controller.located_screens
                #for screen in [self.screens[0]]:
                for screen in self.screens:
                    candidate = screen.intersect(finger, True)                   
                    x_pos = candidate.x
                    y_pos = candidate.y
                    # Throws out datapoints when you point off screen - have to figure out in-bounds geometry for multiscreen
                    if not (math.isnan(x_pos) or math.isnan(y_pos)):
                        screen_to_choose = screen
                        position = candidate
                        chosen_screen = True


                if not chosen_screen: return
                    

                x_pixels = position.x * screen_to_choose.width_pixels
                y_pixels = screen_to_choose.height_pixels - position.y * screen_to_choose.height_pixels

                x_pixels,y_pixels = mouse_position_smoother.update((x_pixels,y_pixels))
                
                # currently only sets it in relation to the primary screen
                mouse.move(int(x_pixels), int(y_pixels))  


    def process_gestures(self, controller):
        global mouse
        frame = controller.frame()
        hand = frame.hands[0]

        if len(hand.fingers) < 2: return

        x_pos = mouse.position()[0]
        y_pos = mouse.position()[1]
        for gesture in frame.gestures():
            if gesture.type == Leap.Gesture.TYPE_SCREEN_TAP:
                if len(hand.fingers) == 2:
                    mouse.click(x_pos, y_pos, 1)
                elif len(hand.fingers) == 3:
                    mouse.click(x_pos, y_pos, 2)
                break # hack so that you only count one click with multi-finger gesture
    
    def state_string(self, state):
        if state == Leap.Gesture.STATE_START:
            return "STATE_START"

        if state == Leap.Gesture.STATE_UPDATE:
            return "STATE_UPDATE"

        if state == Leap.Gesture.STATE_STOP:
            return "STATE_STOP"

        if state == Leap.Gesture.STATE_INVALID:
            return "STATE_INVALID"

def main():
    # Create a sample listener and controller
    listener = SampleListener()
    controller = Leap.Controller()

    # Have the sample listener receive events from the controller
    controller.add_listener(listener)
    controller.config.set("Gesture.Swipe.MinLength", 100.0)
    controller.config.set("Gesture.Swipe.MinVelocity", 450)
    controller.config.save()

    demo.mainloop()

    # Keep this process running until Enter is pressed
    print "Press Enter to quit..."
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        # Remove the sample listener when done
        controller.remove_listener(listener)


def getExtendedFingers(hand): 
    return len(hand.fingers.extended())


def checkPalm(hand):
    if getExtendedFingers(hand) == 5:
        return True
    else:
        return False

def checkFist(hand):
    if getExtendedFingers(hand) == 0:
        return True
    else:
        return False

def checkPointing(hand):
    if getExtendedFingers(hand) == 1 :
        result = False
        for finger in hand.fingers:
            if finger.type == 1:
                result = True
        return result
    return False
   
def checkDrawing(hand):
    if getExtendedFingers(hand) == 2:
        fingerArray = []
        for finger in hand.fingers:
            fingerArray += [finger.type]
        if 0 in fingerArray and 1 in fingerArray:
            return True
        else:
            return False

def rotateGraph(hand):
    normal = hand.palm_normal
    direction = hand.direction

    ax.view_init(elev= -1 * move_velocity  * normal[2], azim = move_velocity  * math.atan(direction[2] / direction[0]))

    plt.draw()
    time.sleep(0.01)


def zoomGraph(hand):
    global is_zoom_mode
    global curYPosition
    if is_zoom_mode == False:
        updateCurrentLimits()
        curYPosition = hand.palm_position[2]
        is_zoom_mode = True

    diff = 0.005 ** ((curYPosition - hand.palm_position[2]) / 2000);
    plt.axis([xMin * diff, xMax * diff, yMin * diff, yMax * diff])
    ax.set_zlim(zMin * diff, zMax * diff)
    plt.draw()
    time.sleep(0.01)

def finishZoom():
    global is_zoom_mode
    global curYPosition
    updateCurrentLimits()
    is_zoom_mode = False
    curYPosition = 0

def updateCurrentLimits():
    global xMin, xMax, yMin, yMax, zMin, zMax
    xMin = plt.axis()[0]
    xMax = plt.axis()[1]
    yMin = plt.axis()[2]
    yMax = plt.axis()[3]
    zMin = ax.get_zlim()[0]
    zMax = ax.get_zlim()[1]


if __name__ == "__main__":
    main()





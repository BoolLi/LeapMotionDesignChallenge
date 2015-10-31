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

move_velocity = 100
minValue = 0.5

mpl.rcParams['legend.fontsize'] = 10

fig = plt.figure()
ax = Axes3D(fig)
theta = np.linspace(-4 * np.pi, 4 * np.pi, 100)
z = np.linspace(-2, 2, 100)
r = z**2 + 1
x = r * np.sin(theta)
y = r * np.cos(theta)
ax.plot(x, y, z, label='parametric curve')
ax.legend()

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



mouse = PyMouse()

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
        frame = controller.frame()
        '''
        print "Frame id: %d, timestamp: %d, hands: %d, fingers: %d, tools: %d, gestures: %d" % (
              frame.id, frame.timestamp, len(frame.hands), len(frame.fingers), len(frame.tools), len(frame.gestures()))
        '''
        # Get hands
        for hand in frame.hands:

            handType = "Left hand" if hand.is_left else "Right hand"
            '''
            print "  %s, id %d, position: %s" % (
                handType, hand.id, hand.palm_position)
            '''
            # Get the hand's normal vector and direction
            normal = hand.palm_normal
            direction = hand.direction
            position = hand.palm_position
            # Calculate the hand's pitch, roll, and yaw angles
            '''
            print "  pitch: %f degrees, roll: %f degrees, yaw: %f degrees" % (
                direction.pitch * Leap.RAD_TO_DEG,
                normal.roll * Leap.RAD_TO_DEG,
                direction.yaw * Leap.RAD_TO_DEG)
            '''
            '''
            print "  pitch: %f degrees, roll: %f degrees, yaw: %f degrees" % (
                direction.pitch * Leap.RAD_TO_DEG,
                normal.roll * Leap.RAD_TO_DEG,
                direction.yaw * Leap.RAD_TO_DEG) '''

            #print direction
            

            if checkPalm(hand):
                rotateGraph(hand)


            if checkFist(hand):
                zoomGraph(hand)
            else:
                finishZoom()

            if checkPointing(hand):
                self.process_gestures(controller)
                
                print "Pointing!"
                
                finger = hand.fingers[0]
                screen_to_choose = None
                position = None
                chosen_screen = False
                self.screens = controller.calibrated_screens
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
                    
                    # currently only sets it in relation to the primary screen
                mouse.move(x_pixels,y_pixels)                    


                finger_pos = finger.joint_position(3)
                mouse.move(10*int(finger_pos[0]), 10* int(finger_pos[1]))
            
                
                print(finger.joint_position(3))
                
               
##                fig = plt.figure(figsize=(8, 6))
##                ax = fig.add_subplot(111, axisbg='#FFFFCC')
##
##                x, y = 4*(np.random.rand(2, 100) - .5)
##                ax.plot(x, y, 'o')
##                ax.set_xlim(-2, 2)
##                ax.set_ylim(-2, 2)
##
##                # set useblit = True on gtkagg for enhanced performance
##                cursor = Cursor(ax, useblit=True, color='red', linewidth=2)
##
##                plt.show()
##                                     
                
            else:
                print "Not pointing!"



            if checkDrawing(hand):
                print "Drawing"
            else:
                print "now drawing"



            

            # Get arm bone
            arm = hand.arm
            '''
            print "  Arm direction: %s, wrist position: %s, elbow position: %s" % (
                arm.direction,
                arm.wrist_position,
                arm.elbow_position)
            '''
            
            '''
            sum = 0
            for finger in hand.fingers:
                print finger.bone[0]
                
                meta = finger.bone[0].direction
                proxi = finger.bone[1].direction
                inter = finger.bone[2].direction
                dMetaProxi = meta.dot(proxi)
                dProxiInter = proxi.dot(inter)
                sum += dMetaProxi
                sum += dProxiInter
                
            if sum <= minValue and getExtendedFingers(hand) == 0:
                return True
            else:
                return False'''
        '''
        # Get tools
        for tool in frame.tools:

            print "  Tool id: %d, position: %s, direction: %s" % (
                tool.id, tool.tip_position, tool.direction)

        # Get gestures
        for gesture in frame.gestures():
            if gesture.type == Leap.Gesture.TYPE_CIRCLE:
                circle = CircleGesture(gesture)

                # Determine clock direction using the angle between the pointable and the circle normal
                if circle.pointable.direction.angle_to(circle.normal) <= Leap.PI/2:
                    clockwiseness = "clockwise"
                else:
                    clockwiseness = "counterclockwise"

                # Calculate the angle swept since the last frame
                swept_angle = 0
                if circle.state != Leap.Gesture.STATE_START:
                    previous_update = CircleGesture(controller.frame(1).gesture(circle.id))
                    swept_angle =  (circle.progress - previous_update.progress) * 2 * Leap.PI

                print "  Circle id: %d, %s, progress: %f, radius: %f, angle: %f degrees, %s" % (
                        gesture.id, self.state_names[gesture.state],
                        circle.progress, circle.radius, swept_angle * Leap.RAD_TO_DEG, clockwiseness)

            if gesture.type == Leap.Gesture.TYPE_SWIPE:
                swipe = SwipeGesture(gesture)
                print "  Swipe id: %d, state: %s, position: %s, direction: %s, speed: %f" % (
                        gesture.id, self.state_names[gesture.state],
                        swipe.position, swipe.direction, swipe.speed)

            if gesture.type == Leap.Gesture.TYPE_KEY_TAP:
                keytap = KeyTapGesture(gesture)
                print "  Key Tap id: %d, %s, position: %s, direction: %s" % (
                        gesture.id, self.state_names[gesture.state],
                        keytap.position, keytap.direction )

            if gesture.type == Leap.Gesture.TYPE_SCREEN_TAP:
                screentap = ScreenTapGesture(gesture)
                print "  Screen Tap id: %d, %s, position: %s, direction: %s" % (
                        gesture.id, self.state_names[gesture.state],
                        screentap.position, screentap.direction )
        '''
        if not (frame.hands.is_empty and frame.gestures().is_empty):
            print ""


     def process_gestures(self, controller):
        frame = controller.frame()
        hand = frame.hands[0]

        if len(hand.fingers) < 2: return

        x_pos = self.mouse.position()[0]
        y_pos = self.mouse.position()[1]
        for gesture in frame.gestures():
            if gesture.type == Leap.Gesture.TYPE_SCREEN_TAP:
                if len(hand.fingers) == 2:
                    self.mouse.click(x_pos, y_pos, 1)
                elif len(hand.fingers) == 3:
                    self.mouse.click(x_pos, y_pos, 2)
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
    time.sleep(0.04)


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
    time.sleep(0.04)

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

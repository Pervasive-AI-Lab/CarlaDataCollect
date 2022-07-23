import math

import pygame
import glob
import os
import sys


from carlacfg import CARLA_LIB_PATH

try:
    sys.path.append(glob.glob(CARLA_LIB_PATH +'/carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass
import carla


# Control object to manage vehicle controls
class ControlObject(object):
    def __init__(self, veh, isAutoPilot, maxVelocity=25.0, maxThrottle=1.0):
        # Conrol parameters to store the control state
        self._vehicle = veh
        # self._steer = 0
        self._maxVelocity = maxVelocity
        self._maxThrottle = maxThrottle
        self._throttle = False
        self._brake = False
        self._steer = None
        self._steer_cache = 0
        # A carla.VehicleControl object is needed to alter the
        # vehicle's control state
        self._control = carla.VehicleControl()
        self.escPressed = False
        self.isAutoPilot = isAutoPilot

    # Check for key press events in the PyGame window
    # and define the control state
    def parse_control(self, event):
        # print("premuto ", event.type)
        # KEY DOWN --------------------------
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.escPressed = True
                #pygame.quit()
            if event.key == pygame.K_RETURN:
                self.isAutoPilot = not self.isAutoPilot
                self._vehicle.set_autopilot(self.isAutoPilot)
            if event.key == pygame.K_UP:
                self._throttle = True
            if event.key == pygame.K_DOWN:
                self._brake = True
            if event.key == pygame.K_RIGHT:
                self._steer = 1
            if event.key == pygame.K_LEFT:
                self._steer = -1
        # KEY UP --------------------------
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                self._throttle = False
            if event.key == pygame.K_DOWN:
                self._brake = False
                self._control.reverse = False
            if event.key == pygame.K_RIGHT:
                self._steer = None
            if event.key == pygame.K_LEFT:
                self._steer = None


    # Process the current control state, change the control parameter
    # if the key remains pressed
    def process_control(self):

        if self._throttle:
            self._control.throttle = min(self._control.throttle + 0.02, self._maxThrottle)
            self._control.gear = 1
            self._control.brake = False
        elif not self._brake:
            self._control.throttle = 0.0

        if self._brake:
            # If the down arrow is held down when the car is stationary, switch to reverse
            v = self._vehicle.get_velocity()
            modulo_vel = math.sqrt(v.x**2 + v.y**2 + v.z**2)
            if modulo_vel < 0.01 and not self._control.reverse:
                self._control.brake = 0.0
                self._control.gear = 1
                self._control.reverse = True
                self._control.throttle = min(self._control.throttle + 0.05, 1)
            elif self._control.reverse:
                self._control.throttle = min(self._control.throttle + 0.05, 1)
            else:
                self._control.throttle = 0.0
                self._control.brake = min(self._control.brake + 0.3, 1)
        else:
            self._control.brake = 0.0

        if self._steer is not None:
            if self._steer == 1:
                self._steer_cache += 0.03
            if self._steer == -1:
                self._steer_cache -= 0.03
            min(0.7, max(-0.7, self._steer_cache))
            self._control.steer = round(self._steer_cache, 1)
        else:
            if self._steer_cache > 0.0:
                self._steer_cache *= 0.2
            if self._steer_cache < 0.0:
                self._steer_cache *= 0.2
            if 0.01 > self._steer_cache > -0.01:
                self._steer_cache = 0.0
            self._control.steer = round(self._steer_cache, 1)

        velocity = self._vehicle.get_velocity()
        velocity = (math.sqrt(velocity.x ** 2 + velocity.y ** 2 + velocity.z ** 2))  # m/s
        if (velocity > self._maxVelocity):
            self._control.throttle = 0.0

        # Ápply the control parameters to the ego vehicle
        self._vehicle.apply_control(self._control)
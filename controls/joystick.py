import math

import pygame
from pip._internal.utils.misc import hide_url
from pygame.locals import K_m
from pygame.locals import K_r
import glob
import os
import sys
from configparser import ConfigParser
from hud import HUD


from carlacfg import CARLA_LIB_PATH

try:
    sys.path.append(glob.glob(CARLA_LIB_PATH +'/carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass
import carla


class joystickControl(object):
    def __init__(self, veh):
        self._control = carla.VehicleControl()
        self._steer_cache = 0.0
        self._parent = veh
        pygame.joystick.init()
        self._last_button = None
        joystick_count = pygame.joystick.get_count()
        if joystick_count > 1:
            raise ValueError("Please Connect Just One Joystick")

        self._joystick = pygame.joystick.Joystick(0)
        self._joystick.init()

        self._parser = ConfigParser()
        self._parser.read('joystick_config.ini')
        self._steer_idx = int(
            self._parser.get('Joystick', 'steering_wheel'))
        self._throttle_idx = int(
            self._parser.get('Joystick', 'throttle'))
        self._brake_idx = int(self._parser.get('Joystick', 'brake'))
        self._reverse_idx = int(self._parser.get('Joystick', 'reverse'))
        self._handbrake_idx = int(
            self._parser.get('Joystick', 'handbrake'))

    def parse_control(self, event, clock):
        world = self._parent.get_world()
        if event.type == pygame.QUIT:
            return True
        elif event.type == pygame.JOYBUTTONDOWN:
            self._last_button = event.button
            print('lastbutton = ', self._last_button)
            if event.button == 0:
                world.restart()
            elif event.button == 1:
                HUD.toggle_info()
            elif event.button == 2:
                world.camera_manager.toggle_camera()
            elif event.button == 3:
                world.next_weather()
            elif event.button == 23:
                world.camera_manager.next_sensor()

        elif event.type == pygame.JOYBUTTONUP:
            if 11 < self._last_button < 19:
                self._control.gear = 0
                print('button up', self._last_button)

        elif event.type == pygame.KEYUP:
            if event.key == K_m:
                self._control.manual_gear_shift = not self._control.manual_gear_shift
                self._control.gear = self._parent.get_control().gear
                print('%s Transmission' %
                                 ('Manual' if self._control.manual_gear_shift else 'Automatic'))

        self._parse_vehicle_wheel()
        self._control.reverse = self._control.gear < 0
        self._parent.apply_control(self._control)

    def _parse_vehicle_wheel(self):
        numAxes = self._joystick.get_numaxes()
        print(f"num axes: {numAxes}")

        jsInputs = [float(self._joystick.get_axis(i)) for i in range(numAxes)]
        print(f"jsInputs: {jsInputs}")

        # Custom function to map range of inputs [1, -1] to outputs [0, 1] i.e 1 from inputs means nothing is pressed
        # For the steering, it seems fine as it is
        K1 = 0.5  # 0.55
        steerCmd = K1 * math.tan(1.1 * jsInputs[self._steer_idx])

        axis1 = -jsInputs[self._throttle_idx]
        if (axis1 > 0):
            valThrottle = axis1
            valBrake = 0
        else:
            valBrake = -axis1
            valThrottle = 0

        throttleCmd = valThrottle
        brakeCmd = valBrake

        self._control.throttle = throttleCmd
        self._control.steer = steerCmd
        self._control.brake = brakeCmd


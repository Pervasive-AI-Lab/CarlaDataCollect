import random
import sys
import os
import glob

########################################################################################################################
# carla
from carlacfg import CARLA_LIB_PATH

try:
    sys.path.append(glob.glob(CARLA_LIB_PATH +'/carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass
import carla

import math

class Vehicle(object):
    def __init__(self,world,blueprint_library, isAutoPilot, randomPosition=False, numPoint=0):
        bp = blueprint_library.filter("model3")[0]
        if randomPosition:
            spawn_point = random.choice(world.get_map().get_spawn_points())
        else:
            spawn_point = world.get_map().get_spawn_points()[numPoint]
        vehicle = world.spawn_actor(bp, spawn_point)
        if (isAutoPilot):
            vehicle.set_autopilot(True)
        else:
            vehicle.apply_control(carla.VehicleControl(throttle=0.0, steer=0.0))
        self.actor = vehicle

    def getVelocity(self):
        velocity = self.actor.get_velocity()
        currentVelocity = (math.sqrt(velocity.x ** 2 + velocity.y ** 2 + velocity.z ** 2))  # m/s
        return currentVelocity

    def getDataOfControls(self):
        control = self.actor.get_control()
        data = [control.steer, control.throttle, control.brake]
        return data

    def dispose(self):
        self.actor.destroy()
        self.actor = None
        print("Vehicle destroyed")



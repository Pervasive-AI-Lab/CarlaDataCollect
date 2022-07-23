import glob
import os
import sys
import weakref
import cv2
import numpy as np

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


class LidarSensor(object):
    def __init__(self, parent_actor, fps, recorder=None):
        self._parent = parent_actor
        self.NAME = "lidar_sensor"
        self.recorder = recorder
        world = self._parent.get_world()
        lidar = world.get_blueprint_library().find('sensor.lidar.ray_cast')
        lidar.set_attribute("range","20")
        lidar.set_attribute("rotation_frequency", str(fps))
        lidar.set_attribute("upper_fov", "10")
        lidar.set_attribute("lower_fov", "-30")
        spawn_point = carla.Transform(carla.Location(x=0, z=2.4))

        self.sensor = world.spawn_actor(lidar, spawn_point, attach_to=parent_actor)
        weak_self = weakref.ref(self)
        self.sensor.listen(lambda data: LidarSensor.process_lidar(weak_self, data))
        self.lastData = None

    @staticmethod
    def process_lidar(weak_self, data):

        self = weak_self()
        if not self:
            return

        self.lastData = data

        # if (self.recorder):
        #     dir = self.recorder.getdir() + "/"
        #     millisec = (int)(round(data.timestamp * 1000, 0))
        #     idxstr = "{:07d}".format(millisec)
        #     data.save_to_disk(dir + self.NAME + "/" + idxstr + ".ply")

    def getData(self):
        return self.lastData

    def dispose(self):
        self.sensor.stop()
        self.sensor.destroy()
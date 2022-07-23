import os
import gzip
from datetime import datetime
import numpy as np
import cv2
import os

class RecorderData(object):

    def __init__(self,dir_name):
        self.directory = dir_name
        self.objects = []
        self.inputFiles = {}
        self.camera = None

    def subScribeLidar(self,lidar):
        self.lidar = lidar
        self.lidarDir = os.path.join(self.directory, lidar.NAME)
        if not os.path.isdir(self.lidarDir):
            os.makedirs(self.lidarDir)

    def subscribeCamera(self,obj):
        self.camera = obj
        self.cameraDir = os.path.join(self.directory,"webcam")
        if not os.path.isdir(self.cameraDir):
            os.makedirs(self.cameraDir)


    def subscribe(self, obj, compressedMode):
        self.objects.append(obj)
        if compressedMode:
            filename = os.path.join(self.directory, obj.NAME + ".npz")
            self.inputFiles[obj.NAME] = gzip.GzipFile(filename, "w")
        else:
            filename = os.path.join(self.directory, obj.NAME + ".npy")
            self.inputFiles[obj.NAME] = open(filename, "ba+")


    def record(self, timestamp):
        if self.camera is not  None:
            image = self.camera.getData()
            idxstr = str(timestamp)
            cv2.imwrite(os.path.join(self.cameraDir, 'webcam_frame_' + idxstr + '.png'), image)

        if self.lidar is not None:
            data = self.lidar.getData()
            if data is not None:
                idxstr = str(timestamp)
                filename = os.path.join(self.lidarDir, idxstr + '.ply')
                data.save_to_disk(filename)

        for obj in self.objects:
            data = obj.getData()
            if data is not None:
                # if (type(obj).__name__ == "VehicleSpeedometer")
                #     pass
                # else:
                np.save(self.inputFiles[obj.NAME], {"timestamp": timestamp, "data": data, "currentDateTime": datetime.now()})


    def dispose(self):
        for obj in self.objects:
            self.inputFiles[obj.NAME].close()
        self.objects = None
        self.camera = None
        self.lidar = None


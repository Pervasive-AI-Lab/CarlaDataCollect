import time

import open3d as o3d
import numpy as np
import keyboard
import os


class LidarViewer(object):
    def __init__(self,foldername):
        self.foldername = foldername
        self.files = os.listdir(self.foldername)

    def FilesCount(self):
        return len(self.files)

    def _getFileName(self,idxFile):
        fullfilename = os.path.join(self.foldername, self.files[idxFile])
        return fullfilename

    def read(self, idxFile):
        fullfilename = self._getFileName(idxFile)
        pcd = o3d.io.read_point_cloud(fullfilename)
        point_cloud_in_numpy = np.asarray(pcd.points)
        return (self.files[idxFile],point_cloud_in_numpy)

    def show(self, startIdxFile):
        idxFile = startIdxFile

        vis = o3d.visualization.Visualizer()
        vis.create_window()

        fullfilename = self._getFileName(idxFile)
        pcd = o3d.io.read_point_cloud(fullfilename)
        vis.add_geometry(pcd)

        while True:
            vis.poll_events()
            vis.update_renderer()
            update = False
            if keyboard.is_pressed("c"): # clear
                vis.clear_geometries()
            if keyboard.is_pressed("w"): # avanti +20
                if (idxFile < len(self.files)-1-20):
                    idxFile += 20
                    update = True
            if keyboard.is_pressed("q"):  # indietro -20
                if (idxFile > 20):
                    idxFile -= 20
                    update = True
            if keyboard.is_pressed("s"):  # avanti +1
                if (idxFile < len(self.files)):
                    idxFile += 1
                    update = True
            elif keyboard.is_pressed("a"): # indietro -1
                if (idxFile > 0):
                    idxFile -= 1
                    update =True
            if (update):
                fullfilename = self._getFileName(idxFile)
                pcd = o3d.io.read_point_cloud(fullfilename)
                #vis.clear_geometries()
                vis.add_geometry(pcd,reset_bounding_box=False)
                vis.update_renderer()
                time.sleep(0.2)
            elif keyboard.is_pressed("x"):
                keyboard.read_key()
                break

        vis.destroy_window()

if __name__ == '__main__':
    lv = LidarViewer("H:/_buttare/Town01_001/lidar_sensor/")
    print(f"numero files: {lv.FilesCount()}")
    last = 0
    lv.show(0)
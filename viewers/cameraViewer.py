import gzip
import numpy as np
from matplotlib import pyplot as plt

class CameraViewer(object):
    def __init__(self, filename):
        self.filename = filename
        self.inputfile=gzip.GzipFile(filename, "r")
        self.inputs = []
        self.k = 0
        while True:
            try:
                input = np.load(self.inputfile, allow_pickle=True)
                self.k = self.k+1
                self.inputs.append(input)
            except:
                break


    def numFrames(self):
        return self.k
        # f = gzip.open(self.filename, 'rb')
        # self.file_content = f.read()

    def showFrame(self,idx):
        if (idx < len(self.inputs) and idx >= 0):
            img = (self.inputs[idx].flat[0]['data'])*255
            plt.imshow(img.astype(np.uint8), interpolation='nearest')
            plt.show()



path = "H:/_buttare/Town01_001/"

vLeft = CameraViewer(path+"cameraLeft.npz")
vRight = CameraViewer(path+"cameraRight.npz")
vCentral = CameraViewer(path+"cameraCentral.npz")
print(f"{vLeft.numFrames()} - {vCentral.numFrames()} - {vRight.numFrames()}")
vLeft.showFrame(10)
vCentral.showFrame(10)
vRight.showFrame(10)
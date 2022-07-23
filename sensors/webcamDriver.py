import cv2


class WebcamDriver(object):
    def __init__(self, width=320, height=240, recorder = None):
        self.recorder = recorder
        self.width = width
        self.height = height
        self.frameCount = 0
        self.camera = None

    def openCamera(self):
        if (self.camera):
            self.camera.release()
            cv2.destroyAllWindows()

        self.frameCount = 0
        self.camera = cv2.VideoCapture(0)
        self.camera.set(3, self.width)
        self.camera.set(4, self.height)

    def getData(self):
        return_value, image = self.camera.read()
        return image


    def _closeCamera(self):
        if (self.camera):
            self.camera.release()
            self.camera = None

    def dispose(self):
        self._closeCamera()


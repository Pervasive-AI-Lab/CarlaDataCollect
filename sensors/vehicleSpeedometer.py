
class VehicleSpeedometer:
    def __init__(self,vehicle):
        self.NAME = "vehicle"
        self.vehicle = vehicle


    def getData(self):
        velocity = self.vehicle.getVelocity()
        return velocity

    def dispose(self):
        self.vehicle = None


class VehicleControls:
    def __init__(self,vehicle):
        self.NAME = "vehicle-controls"
        self.vehicle = vehicle


    def getData(self):
        data  = self.vehicle.getDataOfControls()
        return data

    def dispose(self):
        self.vehicle = None

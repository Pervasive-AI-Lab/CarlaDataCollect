import numpy as np
import os
import pandas as pd


class VehicleDataViewer(object):
    def __init__(self, filename, filenameControls):
        self.filename = filename
        self.filenameControls = filenameControls

        self.data = self._readFile(self.filename)
        self.dataControls  =self._readFile(self.filenameControls)

    def _readFile(self, filename):
        file = open(filename, "br")
        data = []
        while True:
            try:
                singleData = np.load(file, allow_pickle=True)
                data.append(singleData)
            except:
                break
        file.close()
        return data

    def exportToExcel(self, excelFilename):
        allControls = [(a.flat[0]['timestamp'], a.flat[0]['data']) for a in dataVehicle.dataControls]
        allSpeed = [(a.flat[0]['timestamp'], a.flat[0]['data']) for a in dataVehicle.data]

        elenco = []
        for (itemControls, itemSpeed) in zip(allControls,allSpeed):
            if itemSpeed[0] != itemControls[0]:
                raise Exception("non-coincident timestamp values")
            v = [itemControls[0],itemControls[1][0],itemControls[1][1],itemControls[1][2],itemSpeed[1]]
            elenco.append(v)
        df = pd.DataFrame(elenco, columns=['timestamp', 'steer','throttle','brake','speed'])
        df.to_excel(excelFilename, sheet_name='sheet1', index=False)

    def numSamplesSpeed(self):
        return len(self.data)

    def numSamplesControls(self):
        return len(self.dataControls)

if __name__ == '__main__':
    dataVehicle = VehicleDataViewer("H:/_buttare/Town01_001/vehicle.npy","H:/_buttare/Town01_001/vehicle-controls.npy")
    print(dataVehicle.numSamplesSpeed())
    print(dataVehicle.numSamplesControls())

    dataVehicle.exportToExcel("data_vehicle.xlsx")

    # elenco velocità -----------------------------------------------
    # allSpeed = [(a.flat[0]['timestamp'],a.flat[0]['data']) for a in dataVehicle.data]
    # for item in allSpeed:
    #     print(item)

    # elenco controlli -----------------------------------------------
    # allControls = [(a.flat[0]['timestamp'],a.flat[0]['data']) for a in dataVehicle.dataControls]
    # for item in allControls:
    #     print(item)
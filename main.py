# #######################################
# EXTRARNAL LIBS
import glob
import os
import sys
import random
import time
import pygame
import numpy as np
import traceback
import datetime
# from folderUtils import *
import cv2


# #######################################
# INTERNAL LIBS
from controls.g29Control import g29Control
from controls.joystick import joystickControl
from controls.kbdControl import ControlObject

from hud import HUD
from utils import folderUtils
from actors.vehicle import Vehicle
from  simWorld import SimWorld
from recorder import RecorderData
from sensors.vehicleSpeedometer import *
from sensors.cameraFloating import CameraFloating
from sensors.cameraSemantic import CameraSemantic
from sensors.webcamDriver import WebcamDriver
from sensors.lidarSensor import LidarSensor



# ######################################################################################################################
# IMPORT CARLA
try:
    sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass
import carla

# ####################################################################
# Alcune costanti di configurazione
FPS = 25    # fps del sistema
USE_WHEEL = False      # si abilita uso dello volante G29
USE_JOYSTICK = False    # si abilita il joystick (nota: è alternativo al volante).
USE_WEBCAM = False     # si abilita il capture della webcam

START_AUTOPILOT = True  # il veicolo si avvia in modo autopilot
ROOTPATHRECORDING = "D:/_buttare/"   # base path ove salvare i dati raccolti

# ######################################################################################################################
# Scelta della mappa
maps = ['Town01', 'Town02', 'Town03', 'Town04', 'Town05', 'Town06', 'Town07']
print('Elenco delle mappe disponibili: ')

idxMap = 0

for map in maps:
    idxMap += 1
    print(f'\t({idxMap}) {map}')
try:
    #choosenMapIdx = 1
    choosenMapIdx = int(input('Digitare il numero della mappa: '))
except:
    print('Mappa non valida')
    exit(0)

choosenMap = maps[choosenMapIdx-1]
print(f'La mappa scelta è: {choosenMap}')



folderForRecord = folderUtils.createFolderForMap(choosenMap, ROOTPATHRECORDING)
recorder = RecorderData(folderForRecord)

try:
    client = carla.Client("localhost", 2000)
    client.set_timeout(10.0)

    sim_world = SimWorld(client.load_world(choosenMap),client.get_trafficmanager(),FPS)

    # blueprint_library = sim_world.get_blueprint_library()
    theVehicle = Vehicle(sim_world.world,sim_world.blueprint_library, isAutoPilot=START_AUTOPILOT, numPoint=0)
    sim_world.addObject(theVehicle)

    cameraSemanticLeft = CameraSemantic("cameraLeft",theVehicle.actor,position='left',
                                    imgWidth=192, imgHeight=144,showWin=True)
    sim_world.addObject(cameraSemanticLeft)
    recorder.subscribe(cameraSemanticLeft,compressedMode=True)

    cameraSemanticRight = CameraSemantic("cameraRight",theVehicle.actor,position='right',
                                    imgWidth=192, imgHeight=144,showWin=True)
    sim_world.addObject(cameraSemanticRight)
    recorder.subscribe(cameraSemanticRight, compressedMode=True)

    cameraSemanticCentral = CameraSemantic("cameraCentral",theVehicle.actor,position='center',
                                    imgWidth=192, imgHeight=144,showWin=True)
    sim_world.addObject(cameraSemanticCentral)
    recorder.subscribe(cameraSemanticCentral, compressedMode=True)

    lidarSensor = LidarSensor(theVehicle.actor,FPS)
    sim_world.addObject(lidarSensor)
    recorder.subScribeLidar(lidarSensor)

    cameraFloating = CameraFloating(theVehicle.actor)
    sim_world.addObject(cameraFloating)

    if USE_WEBCAM:
        webcamCap = WebcamDriver(320, 240)
        sim_world.addObject(webcamCap)
        webcamCap.openCamera()
        recorder.subscribeCamera(webcamCap)

    speedometer = VehicleSpeedometer(theVehicle)
    recorder.subscribe(speedometer,compressedMode=False)

    theVehicleControls = VehicleControls(theVehicle)
    recorder.subscribe(theVehicleControls, compressedMode=False)

    # -------------------------------------------------------------------------------
    if USE_WHEEL:
        wheelControl = g29Control(theVehicle)
    elif USE_JOYSTICK:
        wheelControl = joystickControl(theVehicle.actor)

    kbdControl = ControlObject(theVehicle.actor, START_AUTOPILOT, maxVelocity=20.0, maxThrottle=0.6)
    # -------------------------------------------------------------------------------

    # Initialise the display
    pygame.init()
    pygame.font.init()
    hud = HUD(kbdControl)
    gameDisplay = pygame.display.set_mode((cameraFloating.image_w, cameraFloating.image_h),
                                          pygame.HWSURFACE | pygame.DOUBLEBUF)
    # Draw black to the display
    gameDisplay.fill((0, 0, 0))
    gameDisplay.blit(CameraFloating.renderObject.surface, (0, 0))

    pygame.display.flip()

    clock = pygame.time.Clock()
    ended = False
    start_time = datetime.datetime.now()


    while not ended:
        clock.tick(FPS)
        sim_world.world.tick()

        gameDisplay.blit(CameraFloating.renderObject.surface, (0, 0))

        hud.tick(sim_world.world, clock, theVehicle.actor)
        hud.render(gameDisplay)

        pygame.display.flip()

        kbdControl.process_control()

        cameraSemanticLeft.drawImage()
        cameraSemanticRight.drawImage()
        cameraSemanticCentral.drawImage()

        timestamp = sim_world.world.get_snapshot().timestamp
        elapsed_millisec = (int)(round(timestamp.elapsed_seconds * 1000, 0))

        recorder.record(elapsed_millisec)

        # Collect key press events
        for event in pygame.event.get():
            # If the window is closed, break the while loop
            if event.type == pygame.QUIT or kbdControl.escPressed:
                print('pygame.QUIT')
                ended = True
            if USE_WHEEL or USE_JOYSTICK:
                wheelControl.parse_control(event, clock)

            # Parse effect of key press event on control state
            kbdControl.parse_control(event)


finally:
    recorder.dispose()

    sim_world.destroy()

    pygame.quit()
    print('pygame.quit()')
    # cv2.waitKey(1)
    # cv2.destroyAllWindows()
    # cv2.waitKey(1)
    print('*** end ***')



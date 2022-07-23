class SimWorld(object):
    def __init__(self,carla_world,traffic_manager,fps):
        self.world = carla_world
        # sim_world = client.get_world()
        settings = self.world.get_settings()
        settings.synchronous_mode = True
        settings.fixed_delta_seconds = 1 / fps
        self.world.apply_settings(settings)
        # self.world.recording_enabled = False

        self.traffic_manager = traffic_manager
        self.traffic_manager.set_synchronous_mode(True)

        self.blueprint_library = self.world.get_blueprint_library()
        self.objects = []

    def addObject(self,actor):
        self.objects.append(actor)


    def destroy(self):
        if self.world is not None:
            settings = self.world.get_settings()
            settings.synchronous_mode = False
            settings.fixed_delta_seconds = None
            self.world.apply_settings(settings)
            self.traffic_manager.set_synchronous_mode(True)

        for obj in self.objects:
            obj.dispose()

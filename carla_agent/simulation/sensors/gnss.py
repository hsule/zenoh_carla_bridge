import carla
import weakref

class GnssSensor(object):
    def __init__(self, parent_actor, sensor_name = 'gnss'):
        self.sensor = None
        self._parent = parent_actor
        self.lat = 0.0
        self.lon = 0.0
        world = self._parent.get_world()
        bp = world.get_blueprint_library().find('sensor.other.gnss')
        bp.set_attribute('role_name', sensor_name)
        trans = carla.Transform(carla.Location(x=0.0, y=0.0, z=2.4))
        self.sensor = world.spawn_actor(bp, trans, attach_to=self._parent)
        # We need to pass the lambda a weak reference to self to avoid circular
        # reference.
        weak_self = weakref.ref(self)
        self.sensor.listen(lambda event: GnssSensor._on_gnss_event(weak_self, event))

    @staticmethod
    def _on_gnss_event(weak_self, event):
        self = weak_self()
        if not self:
            return
        self.lat = event.latitude
        self.lon = event.longitude

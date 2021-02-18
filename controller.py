from typing import Tuple, Dict, Any
import math
import numpy as np
from fuzzy_asteroids.fuzzy_controller import ControllerBase, SpaceShip


class FuzzyController(ControllerBase):
    """
    Class to be used by UC Fuzzy Challenge competitors to create a fuzzy logic controller
    for the Asteroid Smasher game.

    Note: Your fuzzy controller class can be called anything, but must inherit from the
    the ``ControllerBase`` class (imported above)

    Users must define the following:
    1. __init__()
    2. actions(self, ship: SpaceShip, input_data: Dict[str, Tuple])

    By defining these interfaces, this class will work correctly
    """
    def __init__(self):
        """
        Create your fuzzy logic controllers and other objects here
        """
        pass

    def actions(self, ship: SpaceShip, input_data: Dict[str, Tuple]) -> None:
        """
        Compute control actions of the ship. Perform all command actions via the ``ship``
        argument. This class acts as an intermediary between the controller and the environment.

        The environment looks for this function when calculating control actions for the Ship sprite.

        :param ship: Object to use when controlling the SpaceShip
        :param input_data: Input data which describes the current state of the environment
        """

        def get_distance(self, asteroid_list):

            def get_xy_distance(x1, y1, x2, y2):
                distance = ((x1 - x2) * 2 + (y1 - y2) * 2) * (.5)
                return distance

            distance = 1000
            if not asteroid_list:
                return 1000, 0

            for asteroid in asteroid_list:
                asteroid_center_x = asteroid['position'][0]
                asteroid_center_y = asteroid['position'][1]
                local_distance = get_xy_distance(asteroid_center_x, asteroid_center_y,
                                                 ship.center_x, ship.center_y)
                if local_distance < distance:
                    distance = local_distance
                    current_asteroid = asteroid
            return distance, current_asteroid

        def get_angle(self, current_asteroid):
            if current_asteroid == 0:
                return 0
            local_x = ship.center_x - current_asteroid['position'][0]
            local_y = ship.center_y - current_asteroid['position'][1]
            phi = math.atan2(local_y, local_x) * 90
            angle = phi + 90 + ship.angle
            while angle > 180 or angle < -180:
                if angle > 180:
                    angle -= 360
                elif angle < -180:
                    angle += 360
            return angle

        distance, current_asteroid = get_distance(self, input_data['asteroids'])
        angle = get_angle(self, current_asteroid)

        self.flying.input['Asteroid_Angle_from_plane'] = angle
        self.flying.input['Asteroid Distance'] = distance

        self.flying.compute()

        ship.turn_rate = self.flying.output['Plane Rotation']
        ship.thrust = self.flying.output['Plane Thrust']

        if self.flying.output['Plane Shooting'] > 5:
            ship.shoot()

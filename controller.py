from typing import Tuple, Dict, Any
import math
import numpy as np
from fuzzy_asteroids.fuzzy_controller import ControllerBase, SpaceShip
from FISstructure import FIS, SingleFIS
import itertools

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
    def __init__(self, gene):
        """
        Create your fuzzy logic controllers and other objects here
        """
        gene = gene[0]
        angle_geneN = sorted(gene[0])
        angle_geneP = sorted(gene[1])

        avoid_rule = gene[2]
        thrust_rule = gene[3]
        avoid_geneN = sorted(gene[4])
        avoid_geneP = sorted(gene[5])

        angle_geneN = [x * 360 for x in angle_geneN]
        angle_geneP = [x * 360 for x in angle_geneP]

        angleMF_values = [(-360, angle_geneN[0], angle_geneN[1]),
                          (angle_geneN[2], 0,  angle_geneP[0]), (angle_geneP[1],  angle_geneP[2], 360)]
        shootMF_values = [(0, 3, 6), (4, 8, 10)]
        targetRules = [0, 1, 0]
        targetFIS = SingleFIS([angleMF_values, shootMF_values], targetRules)
        self.target = targetFIS

        aimMF_values = [(-180, -90, -0.5), (-1, 0, 1), (0.5, 90, 180)]
        steerMF_values = [(-100, -99, 1), (-2, 0, 2), (1, 99, 100)]
        shootRules = [0, 1, 2]
        shootFIS = SingleFIS([aimMF_values, steerMF_values], shootRules)
        self.shoot = shootFIS

        collideMF_values = [(0, 80, 100), (80, 120, 160), (140, 160, 800)]
        interceptMF_values = [(0, 0.8, 1.2), (0.8, 1.0, 10.0)]
        # Outputs are NOTHING, TARGET, AVOID
        threatMF_values = [(0, 0.6, 1.2), (1.0, 1.6, 2.2), (2.0, 2.5, 3.0)]
        collideRules = [2, 1, 2, 1, 1, 0]
        collideFIS = FIS([collideMF_values, interceptMF_values, threatMF_values], collideRules)
        self.collide = collideFIS

        avoidMF_values = [(-180, avoid_geneN[0], avoid_geneN[1]), (avoid_geneN[2], avoid_geneN[3], avoid_geneN[4]),
                          (avoid_geneN[5], avoid_geneN[6], 0), (0, avoid_geneP[0], avoid_geneP[1]),
                          (avoid_geneP[2], avoid_geneP[3], avoid_geneP[4]), (avoid_geneP[5], avoid_geneP[6], 180)]

        veerMF_values = [(100, 70, 40), (60, 30, 0), (0, -30, -60), (-40, -70, -100)]
        avoidRules = avoid_rule
        thrustRules = thrust_rule
        thrustMF_values = [(-200, -150, 0), (0, 150, 200)]
        # avoidRules = [0, 1, 2, 3, 2, 1, 0, 1, 2, 3, 2, 3]
        # thrustRules = [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]
        avoidFIS = FIS([interceptMF_values, avoidMF_values, veerMF_values], avoidRules)
        thrustFIS = FIS([interceptMF_values, avoidMF_values, thrustMF_values], thrustRules)
        self.avoid = avoidFIS
        self.thrust = thrustFIS

    def actions(self, ship: SpaceShip, input_data: Dict[str, Tuple]) -> None:
        """
        Compute control actions of the ship. Perform all command actions via the ``ship``
        argument. This class acts as an intermediary between the controller and the environment.

        The environment looks for this function when calculating control actions for the Ship sprite.

        :param ship: Object to use when controlling the SpaceShip
        :param input_data: Input data which describes the current state of the environment
        """

        def extract_norms(collision_array):
            collision_norms = []
            collision_array = collision_array.tolist()
            for x, y in zip(*collision_array):
                vnorm = np.linalg.norm([x, y])
                collision_norms.append(vnorm)
            return collision_norms

        def extend_path(asteroid_list, n):
            asteroid_path = []
            for asteroid in asteroid_list:
                x, y = asteroid['position']
                vx, vy = asteroid['velocity']
                xpath = x + np.multiply(np.arange(1, n, 1), vx)
                ypath = y + np.multiply(np.arange(1, n, 1), vy)
                path = np.stack((xpath, ypath))
                asteroid_path.append(path)
            return asteroid_path

        def extend_player_path(player, n):
            x, y = player.center_x, player.center_y
            vx, vy = player.change_x, player.change_y
            xpath = x + np.multiply(np.arange(1, n, 1), vx)
            ypath = y + np.multiply(np.arange(1, n, 1), vy)
            return np.stack((xpath, ypath))

        def get_xy_distance(x1, y1, x2, y2):
            distance1 = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
            return distance1

        def get_distance(asteroid_list):
            asteroid_array = []
            if not asteroid_list:
                return None
            for asteroid in asteroid_list:
                asteroid_center_x = asteroid['position'][0]
                asteroid_center_y = asteroid['position'][1]
                current_distance = get_xy_distance(asteroid_center_x, asteroid_center_y, ship.center_x, ship.center_y)
                asteroid_array.append(current_distance)
            return asteroid_array

        def get_angle(asteroid_list):
            angle_array = []

            if not asteroid_list:
                return None, None

            for asteroid in asteroid_list:
                local_x = ship.center_x - asteroid['position'][0]
                local_y = ship.center_y - asteroid['position'][1]
                phi = math.atan2(local_y, local_x) * 180 / math.pi
                angle = phi + 90 - ship.angle

                while angle > 180 or angle < -180:
                    if angle > 180:
                        angle -= 360
                    elif angle < -180:
                        angle += 360
                angle_array.append(angle)
            return angle_array

        def get_velocity(path):
            diviser = path[0]
            vels = [x / diviser for x in path]
            velocity = sum(vels) / len(vels)
            return velocity

# Targeting FIS
        targetFIS = self.target
        avoidFIS = self.avoid
        thrustFIS = self.thrust
        collideFIS = self.collide
        shootFIS = self.shoot

        asteroid_list = input_data['asteroids']
        angle = get_angle(asteroid_list)
        distance = get_distance(asteroid_list)

        if asteroid_list:
            n = 25
            asteroid_path = extend_path(asteroid_list, n)
            player_path = extend_player_path(ship, n)
            collision_array = [collide - player_path for collide in asteroid_path]
            collision_norms = list(map(extract_norms, collision_array))
            collision_input = list(map(min, collision_norms))
            velocity_array = list(map(get_velocity, collision_norms))
            collide_array = []

            nothing_array = []
            target_array = []
            avoid_array = []

            # Find the index of the max value then check where the value falls
            for dist, vel in zip(collision_input, velocity_array):
                collide_value = collideFIS.compute(dist, vel)
                collide_array.append(collide_value)

            collide_index = collide_array.index(max(collide_array))
            collide_target = collide_array[collide_index]
            shoot_array = []
            for ang in angle:
                output = targetFIS.compute(ang)
                shoot_array.append(output)

            if any(x > 7.15 for x in shoot_array):
                ship.shoot()

            if collide_target <= 1:
                target_index = collision_norms.index(min(collision_norms, key=min))
                shoot_angle = angle[target_index]
                output2 = shootFIS.compute(shoot_angle)
                ship.turn_rate = output2
            elif 1 < collide_target <= 2:
                target_index = collide_index
                shoot_angle = angle[target_index]
                output3 = shootFIS.compute(shoot_angle)
                ship.turn_rate = output3
            else:
                target_index = collide_index
                avoid_in2 = angle[target_index]
                avoid_in1 = velocity_array[target_index]
                output4 = avoidFIS.compute(avoid_in1, avoid_in2)
                output5 = thrustFIS.compute(avoid_in1, avoid_in2)
                ship.turn_rate = output4
                ship.thrust = output5




            # s = collision_norms.index(min(collision_norms, key=min))

        # shoot_list = []
        # avoid_list = []
        # if angle and distance:
        #     for ang, dist in zip(angle, distance):
        #         in1 = ang
        #         in2 = dist
        #         output = targetFIS.compute(in1, in2)
        #         output1 = avoidFIS.compute(in1)
        #         avoid_list.append(output1)
        #         shoot_list.append(output)
        #
        #     if any(x > 7.15 for x in shoot_list):
        #         ship.shoot()

        #     # Aiming FIS
        #     shootFIS = self.shoot
        #     shoot_idx = np.argmin(np.absolute(angle))
        #     shoot_angle = angle[s]
        #
        #     output2 = shootFIS.compute(shoot_angle)
        #     collision_list = list(itertools.chain.from_iterable(collision_norms))
        #
        #     if any(y < 75 for y in collision_list):
        #         # ship.turn_rate = output2
        #         ship.thrust = -150
        #         abs_list = list(map(abs, avoid_list))
        #         t = abs_list.index(max(abs_list))
        #         ship.turn_rate = avoid_list[t]
        #     else:
        #         ship.turn_rate = output2


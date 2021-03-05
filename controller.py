from typing import Tuple, Dict, Any
import math
import numpy as np
import itertools
from fuzzy import Membership, Rulebase, Defuzz
from fuzzy_asteroids.fuzzy_controller import ControllerBase, SpaceShip
from FISstructure import FIS

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

        dr_distMF_values = [(0, 5, 10), (5, 50, 75), (70, 250, 500), (450, 550, 1200)]
        dr_angMF_values = [(-360, -250, -150), (-250, -150, -50), (-100, -50, 0), (-15, 0, 15),
                           (0, 50, 100), (50, 150, 250), (150, 250, 360)]

        dr_steerMF_values = [(-180, -90, 0), (-2, 0, 2), (0, 90, 180)]
        dr_thrustMF_values = [(0, 2, 4), (60, 80, 100), (80, 100, 120), (100, 120, 200)]

        angleMF_values = [(-360, -60, -2), (-2, 0, 2), (2, 60, 360)]

        distanceMF_values = [(0, 0, 20), (10, 100, 200), (10, 999, 1000)]

        shootMF_values = [(0, 3, 6), (4, 8, 10)]

        aimMF_values = [(-180, -90, -1), (-2, 0, 2), (1, 90, 180)]

        steerMF_values = [(-100, -99, 1), (-2, 0, 2), (1, 99, 100)]

        drDMF1 = Membership(dr_distMF_values[0])
        drDMF2 = Membership(dr_distMF_values[1])
        drDMF3 = Membership(dr_distMF_values[2])
        drDMF4 = Membership(dr_distMF_values[3])

        drAMF1 = Membership(dr_angMF_values[0])
        drAMF2 = Membership(dr_angMF_values[1])
        drAMF3 = Membership(dr_angMF_values[2])
        drAMF4 = Membership(dr_angMF_values[3])
        drAMF5 = Membership(dr_angMF_values[4])
        drAMF6 = Membership(dr_angMF_values[5])
        drAMF7 = Membership(dr_angMF_values[6])

        aMF1 = Membership(angleMF_values[0])
        aMF2 = Membership(angleMF_values[1])
        aMF3 = Membership(angleMF_values[2])

        dMF1 = Membership(distanceMF_values[0])
        dMF2 = Membership(distanceMF_values[1])
        dMF3 = Membership(distanceMF_values[2])

        sMF1 = Membership(aimMF_values[0])
        sMF2 = Membership(aimMF_values[1])
        sMF3 = Membership(aimMF_values[2])

        self.drTMF = dr_thrustMF_values
        self.drSMF = dr_steerMF_values
        self.drDMF = [drDMF1, drDMF2, drDMF3, drDMF4]
        self.drAMF = [drAMF1, drAMF2, drAMF3, drAMF4, drAMF5, drAMF6, drAMF7]
        self.MF1 = [aMF1, aMF2, aMF3]
        self.MF2 = [dMF1, dMF2, dMF3]
        self.MF3 = shootMF_values
        self.MF4 = [sMF1, sMF2, sMF3]
        self.MF5 = steerMF_values
        self.Fr1 = Rulebase()
        self.idx = 0

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

        def get_distance(self, asteroid_list):

            def get_xy_distance(x1, y1, x2, y2):
                distance1 = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
                return distance1
            asteroid_array = []
            if not asteroid_list:
                return None
            for asteroid in asteroid_list:
                asteroid_center_x = asteroid['position'][0]
                asteroid_center_y = asteroid['position'][1]
                current_distance = get_xy_distance(asteroid_center_x, asteroid_center_y, ship.center_x, ship.center_y)
                asteroid_array.append(current_distance)
            return asteroid_array


        def get_angle(self, asteroid_list):
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

        def get_drive_angle(self, goal):
            local_x = ship.center_x - goal[0]
            local_y = ship.center_y - goal[1]
            phi = math.atan2(local_y, local_x) * 180 / math.pi
            angle = phi + 90 - ship.angle
            return angle

# Targeting FIS
        aMF1, aMF2, aMF3 = self.MF1
        dMF1, dMF2, dMF3 = self.MF2
        sMF1, sMF2, sMF3 = self.MF4
        Fr1 = self.Fr1

        asteroid_list = input_data['asteroids']
        angle = get_angle(self, asteroid_list)
        distance = get_distance(self, asteroid_list)

        shoot_list = []
        if angle and distance:
            for ang, dist in zip(angle, distance):
                in1 = ang
                in2 = dist

                angleMF1 = aMF1.lshlder(in1)
                angleMF2 = aMF2.triangle(in1)
                angleMF3 = aMF3.rshlder(in1)

                distanceMF1 = dMF1.lshlder(in2)
                distanceMF2 = dMF2.triangle(in2)
                distanceMF3 = dMF3.rshlder(in2)

                F_rules = [Fr1.AND_rule([angleMF1, distanceMF1]), Fr1.AND_rule([angleMF1, distanceMF2]), Fr1.AND_rule([angleMF1, distanceMF3]),
                           Fr1.AND_rule([angleMF2, distanceMF1]), Fr1.AND_rule([angleMF2, distanceMF2]), Fr1.AND_rule([angleMF2, distanceMF3]),
                           Fr1.AND_rule([angleMF3, distanceMF1]), Fr1.AND_rule([angleMF3, distanceMF2]), Fr1.AND_rule([angleMF3, distanceMF3])
                           ]

                F_shoot = []
                F_dont_shoot = []

                fRules = [1, 1, 1, 2, 2, 2, 1, 1, 1]

                for idx, rule in enumerate(fRules):
                    if rule == 2.0:
                        F_shoot.append(F_rules[idx])
                    elif rule == 1.0:
                        F_dont_shoot.append(F_rules[idx])

                F_s = Fr1.OR_rule(F_shoot)
                F_d = Fr1.OR_rule(F_dont_shoot)

                F_mu = [F_d, F_s]
                F_out = Defuzz(F_mu, self.MF3)
                output = F_out.defuzz_out()
                shoot_list.append(output)

            if any(x > 6 for x in shoot_list):
                ship.shoot()

            n = 10
            asteroid_path = extend_path(asteroid_list, n)
            player_path = extend_player_path(ship, n)

            collision_array = [collide - player_path for collide in asteroid_path]
            collision_norms = list(map(extract_norms, collision_array))
            s = collision_norms.index(min(collision_norms, key=min))

# Aiming FIS
            shoot_idx = np.argmin(np.absolute(angle))
            shoot_angle = angle[s]

            steerMF1 = sMF1.lshlder(shoot_angle)
            steerMF2 = sMF2.triangle(shoot_angle)
            steerMF3 = sMF3.rshlder(shoot_angle)

            F_mus = [steerMF1, steerMF2, steerMF3]
            F_out2 = Defuzz(F_mus, self.MF5)
            output2 = F_out2.defuzz_out()
            ship.turn_rate = output2

# Guidance Section
#         goal_list = [np.array([600, 300]), np.array([600, 400]), np.array([100, 400]), np.array([100, 100]), np.array([100, 400])]
#         if self.idx < len(goal_list):
#             goal = goal_list[self.idx]
#         else:
#             goal = np.array([ship.center_x, ship.center_y])
#
#         goal_diff = goal - np.array([ship.center_x, ship.center_y])
#         goal_dist = np.linalg.norm(goal_diff)
#         if goal_dist < 10:
#             self.idx += 1
#
#         goal_angle = get_drive_angle(self, goal)
#
#         drDMF1, drDMF2, drDMF3, drDMF4 = self.drDMF
#         drAMF1, drAMF2, drAMF3, drAMF4, drAMF5, drAMF6, drAMF7 = self.drAMF
#
#         dr_distMF1 = drDMF1.lshlder(goal_dist)
#         dr_distMF2 = drDMF2.triangle(goal_dist)
#         dr_distMF3 = drDMF3.triangle(goal_dist)
#         dr_distMF4 = drDMF4.rshlder(goal_dist)
#         dr_angleMF1 = drAMF1.lshlder(goal_angle)
#         dr_angleMF2 = drAMF2.triangle(goal_angle)
#         dr_angleMF3 = drAMF3.triangle(goal_angle)
#         dr_angleMF4 = drAMF4.triangle(goal_angle)
#         dr_angleMF5 = drAMF5.triangle(goal_angle)
#         dr_angleMF6 = drAMF6.triangle(goal_angle)
#         dr_angleMF7 = drAMF7.rshlder(goal_angle)
#
#         dr_distMU = [dr_distMF1, dr_distMF2, dr_distMF3, dr_distMF4]
#         dr_angMU = [Fr1.OR_rule([dr_angleMF1, dr_angleMF2, dr_angleMF3]),
#                     dr_angleMF4,
#                     Fr1.OR_rule([dr_angleMF5, dr_angleMF6, dr_angleMF7])]
#
#         F_out3 = Defuzz(dr_distMU, self.drTMF)
#         output3 = F_out3.defuzz_out()
#
#         F_out4 = Defuzz(dr_angMU, self.drSMF)
#         output4 = F_out4.defuzz_out()
#
#         ship.thrust = output3
#         ship.turn_rate = output4

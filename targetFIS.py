from typing import Tuple, Dict, Any

from fuzzy import Membership, Rulebase, Defuzz
import math
import numpy as np


class TargetFIS:

    def __init__(self, gene):


        aimMF_values = [(-180, -90, -1), (-2, 0, 2), (1, 90, 180)]
        steerMF_values = [(-100, -99, 1), (-2, 0, 2), (1, 99, 100)]

    def actions(self, ship, input_data: Dict[str, Tuple]):
        def extract_norms(collision_array):
            collision_norms = []
            collision_array = collision_array.tolist()
            for x, y in zip(*collision_array):
                v_norm = np.linalg.norm([x, y])
                collision_norms.append(v_norm)
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

        def get_distance(asteroid_list):
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

        def get_angle(ship, asteroid_list):
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

        asteroid_list = input_data['asteroids']
        angle = get_angle(ship, asteroid_list)

        n = 10
        asteroid_path = extend_path(asteroid_list, n)
        player_path = extend_player_path(ship, n)

        collision_array = [collide - player_path for collide in asteroid_path]
        collision_norms = list(map(extract_norms, collision_array))
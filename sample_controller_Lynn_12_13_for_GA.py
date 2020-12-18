from typing import List, Tuple, Dict
import math
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

from asteroids.fuzzy_controller import ControllerBase, SpaceShip
from asteroids.fuzzy_asteroids import FuzzyAsteroidGame, TrainerEnvironment


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
    def __init__(self, chromosome):
        """
        Create your fuzzy logic controllers and other objects here
        """
         # Define the Input Mfs
        ################### Asteroid Direction relative to plane ######################
        Asteroid_Angle_from_plane = ctrl.Antecedent(np.arange(-180, 180, 1), 'Asteroid_Angle_from_plane')
        # Asteroid_Angle_from_plane['small'] = fuzz.trimf(Asteroid_Angle_from_plane.universe, [-1, 0, 30])
        # Asteroid_Angle_from_plane['medium_small'] = fuzz.trimf(Asteroid_Angle_from_plane.universe, [0, 30, 60])
        # Asteroid_Angle_from_plane['medium'] = fuzz.trimf(Asteroid_Angle_from_plane.universe, [30, 60, 90])
        # Asteroid_Angle_from_plane['medium_large'] = fuzz.trimf(Asteroid_Angle_from_plane.universe, [60, 90, 120])
        # Asteroid_Angle_from_plane['large'] = fuzz.trimf(Asteroid_Angle_from_plane.universe, [90, 120, 150])
        # Asteroid_Angle_from_plane['large_large'] = fuzz.trimf(Asteroid_Angle_from_plane.universe, [120, 180, 180])
        
        Asteroid_Angle_from_plane['neg_small'] = fuzz.trimf(Asteroid_Angle_from_plane.universe, [-60, 0, 1])
        Asteroid_Angle_from_plane['neg_medium'] = fuzz.trimf(Asteroid_Angle_from_plane.universe, [-120, -60, 0])
        Asteroid_Angle_from_plane['neg_large'] = fuzz.trimf(Asteroid_Angle_from_plane.universe, [-180, -180, -60])
        
        Asteroid_Angle_from_plane['small'] = fuzz.trimf(Asteroid_Angle_from_plane.universe, [-1, 0, 60])
        Asteroid_Angle_from_plane['medium'] = fuzz.trimf(Asteroid_Angle_from_plane.universe, [0, 60, 120])
        Asteroid_Angle_from_plane['large'] = fuzz.trimf(Asteroid_Angle_from_plane.universe, [60, 180, 180])
        
        #Asteroid_Angle_from_plane.view()
        
        
        
        # ################### Asteroid Direction of Movement ############################
        # self.Asteroid_Direction_of_Movement = ctrl.Antecedent(np.arange(0, 360, 1),
        #                                                  'Asteroid Direction of Movement')
        # self.Asteroid_Direction_of_Movement.automf(7)
        
        
        ################### Asteroid Distance relative to plane #######################
        Asteroid_Distance = ctrl.Antecedent(np.arange(0, 1000, 1), 'Asteroid Distance')
        Asteroid_Distance['small'] = fuzz.trimf(Asteroid_Distance.universe, [0, 0, 20])
        Asteroid_Distance['medium'] = fuzz.trimf(Asteroid_Distance.universe, [10, 100, 200])
        Asteroid_Distance['large'] = fuzz.trimf(Asteroid_Distance.universe, [100, 1000, 1000])
        #Asteroid_Distance.view()
        
        
        # Define the Output Mfs
        ################### Plane Rotation ############################################
        max_bound_rot = 180
        min_bound_rot = -180
        rot_interval = max_bound_rot/2
        Plane_Rotation = ctrl.Consequent(np.arange(min_bound_rot, max_bound_rot, 1), 'Plane Rotation')
        Plane_Rotation['neg_large'] = fuzz.trimf(Plane_Rotation.universe, [min_bound_rot, min_bound_rot, -2])
        Plane_Rotation['zero'] = fuzz.trimf(Plane_Rotation.universe, [-5, 0, 5])
        Plane_Rotation['large'] = fuzz.trimf(Plane_Rotation.universe, [2, max_bound_rot, max_bound_rot])
        #Plane_Rotation.view()
        
        
        ################### Plane Movement ############################################
        max_bound_thrust = 480
        min_bound_thrust = -480
        thrust_interval = max_bound_thrust/2
        Plane_Thrust = ctrl.Consequent(np.arange(min_bound_thrust, max_bound_thrust+1, 1), 'Plane Thrust')
        Plane_Thrust['neg_large'] = fuzz.trimf(Plane_Thrust.universe, [min_bound_thrust, min_bound_thrust, -thrust_interval])
        Plane_Thrust['neg_small'] = fuzz.trimf(Plane_Thrust.universe, [-thrust_interval-1, -thrust_interval, 0])
        Plane_Thrust['zero'] = fuzz.trimf(Plane_Thrust.universe, [-1, 0, 1])
        Plane_Thrust['large'] = fuzz.trimf(Plane_Thrust.universe, [thrust_interval, max_bound_thrust, max_bound_thrust])
        Plane_Thrust['small'] = fuzz.trimf(Plane_Thrust.universe, [0, thrust_interval, thrust_interval + 1])
        
        #Plane_Thrust.view()
        
        ################### Plane Shooting ############################################
        Plane_Shooting = ctrl.Consequent(np.arange(0, 10+1, 1), 'Plane Shooting')
        Plane_Shooting['False'] = fuzz.trimf(Plane_Shooting.universe, [0, 0, 7])
        Plane_Shooting['True'] = fuzz.trimf(Plane_Shooting.universe, [3, 10, 10])
        #Plane_Shooting.view()
        
        # convert float from chromosomes to string
        rotation_values = chromosome[0:18]
        thrust_values = chromosome[18:36]
        shoot_values = chromosome[36:54]
        
        rotation_strings = []
        thrust_strings = []
        shoot_strings = []
        
        for value in rotation_values:
            if value < 1/3:
                rotation_strings.append('neg_large')
            elif value < 2/3:
                rotation_strings.append('zero')
            else:
                rotation_strings.append('large')
        
        for value in thrust_values:
            if value < 1/5:
                thrust_strings.append('neg_large')
            elif value < 2/5:
                thrust_strings.append('neg_small')
            elif value < 3/5:
                thrust_strings.append('zero')
            elif value < 4/5:
                thrust_strings.append('small')
            else:
                thrust_strings.append('large')
                
        for value in shoot_values:
            if value < 1/2:
                shoot_strings.append('False')
            else:
                shoot_strings.append('True')
        
        # Define the Rule Base
        rule1 = ctrl.Rule(antecedent= (Asteroid_Angle_from_plane['neg_small'] & Asteroid_Distance['small']), consequent= (Plane_Rotation[rotation_strings[0]], Plane_Thrust[thrust_strings[0]], Plane_Shooting[shoot_strings[0]]), label='rule 1')
        rule2 = ctrl.Rule(Asteroid_Angle_from_plane['neg_small'] & Asteroid_Distance['medium'], consequent= (Plane_Rotation[rotation_strings[1]], Plane_Thrust[thrust_strings[1]], Plane_Shooting[shoot_strings[1]]), label='rule 2')
        rule3 = ctrl.Rule(Asteroid_Angle_from_plane['neg_small'] & Asteroid_Distance['large'], consequent= (Plane_Rotation[rotation_strings[2]], Plane_Thrust[thrust_strings[2]], Plane_Shooting[shoot_strings[2]]), label='rule 3')
        
        rule4 = ctrl.Rule(Asteroid_Angle_from_plane['neg_medium'] & Asteroid_Distance['small'], consequent= (Plane_Rotation[rotation_strings[3]], Plane_Thrust[thrust_strings[3]], Plane_Shooting[shoot_strings[3]]), label='rule 4')
        rule5 = ctrl.Rule(Asteroid_Angle_from_plane['neg_medium'] & Asteroid_Distance['medium'], consequent= (Plane_Rotation[rotation_strings[4]], Plane_Thrust[thrust_strings[4]], Plane_Shooting[shoot_strings[4]]))
        rule6 = ctrl.Rule(Asteroid_Angle_from_plane['neg_medium'] & Asteroid_Distance['large'], consequent= (Plane_Rotation[rotation_strings[5]], Plane_Thrust[thrust_strings[5]], Plane_Shooting[shoot_strings[5]]))
        
        rule7 = ctrl.Rule(Asteroid_Angle_from_plane['neg_large'] & Asteroid_Distance['small'], consequent= (Plane_Rotation[rotation_strings[6]], Plane_Thrust[thrust_strings[6]], Plane_Shooting[shoot_strings[6]]))
        rule8 = ctrl.Rule(Asteroid_Angle_from_plane['neg_large'] & Asteroid_Distance['medium'], consequent= (Plane_Rotation[rotation_strings[7]], Plane_Thrust[thrust_strings[7]], Plane_Shooting[shoot_strings[7]]))
        rule9 = ctrl.Rule(Asteroid_Angle_from_plane['neg_large'] & Asteroid_Distance['large'], consequent= (Plane_Rotation[rotation_strings[8]], Plane_Thrust[thrust_strings[8]], Plane_Shooting[shoot_strings[8]]))
        
        rule10 = ctrl.Rule(Asteroid_Angle_from_plane['small'] & Asteroid_Distance['small'], consequent= (Plane_Rotation[rotation_strings[9]], Plane_Thrust[thrust_strings[9]], Plane_Shooting[shoot_strings[9]]))
        rule11 = ctrl.Rule(Asteroid_Angle_from_plane['small'] & Asteroid_Distance['medium'], consequent= (Plane_Rotation[rotation_strings[10]], Plane_Thrust[thrust_strings[10]], Plane_Shooting[shoot_strings[10]]))
        rule12 = ctrl.Rule(Asteroid_Angle_from_plane['small'] & Asteroid_Distance['large'], consequent= (Plane_Rotation[rotation_strings[11]], Plane_Thrust[thrust_strings[11]], Plane_Shooting[shoot_strings[11]]))
        
        rule13 = ctrl.Rule(Asteroid_Angle_from_plane['medium'] & Asteroid_Distance['small'], consequent= (Plane_Rotation[rotation_strings[12]], Plane_Thrust[thrust_strings[12]], Plane_Shooting[shoot_strings[12]]))
        rule14 = ctrl.Rule(Asteroid_Angle_from_plane['medium'] & Asteroid_Distance['medium'], consequent= (Plane_Rotation[rotation_strings[13]], Plane_Thrust[thrust_strings[13]], Plane_Shooting[shoot_strings[13]]))
        rule15 = ctrl.Rule(Asteroid_Angle_from_plane['medium'] & Asteroid_Distance['large'], consequent= (Plane_Rotation[rotation_strings[14]], Plane_Thrust[thrust_strings[14]], Plane_Shooting[shoot_strings[14]]))
        
        rule16 = ctrl.Rule(Asteroid_Angle_from_plane['large'] & Asteroid_Distance['small'], consequent= (Plane_Rotation[rotation_strings[15]], Plane_Thrust[thrust_strings[15]], Plane_Shooting[shoot_strings[15]]))
        rule17 = ctrl.Rule(Asteroid_Angle_from_plane['large'] & Asteroid_Distance['medium'], consequent= (Plane_Rotation[rotation_strings[16]], Plane_Thrust[thrust_strings[16]], Plane_Shooting[shoot_strings[16]]))
        rule18 = ctrl.Rule(Asteroid_Angle_from_plane['large'] & Asteroid_Distance['large'], consequent= (Plane_Rotation[rotation_strings[17]], Plane_Thrust[thrust_strings[17]], Plane_Shooting[shoot_strings[17]]))
        
        
        
                
        self.plane_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, 
                                              rule4, rule5, rule6,
                                              rule7, rule8, rule9,
                                              rule10, rule11, rule12,
                                              rule13, rule14, rule15,
                                              rule16, rule17, rule18]) 
        self.flying = ctrl.ControlSystemSimulation(self.plane_ctrl)

    def actions(self, ship: SpaceShip, input_data: Dict[str, Tuple]) -> None:
        """
        Compute control actions of the ship. Perform all command actions via the ``ship``
        argument. This class acts as an intermediary between the controller and the environment.

        The environment looks for this function when calculating control actions for the Ship sprite.

        :param ship: Object to use when controlling the SpaceShip
        :param input_data: Input data which describes the current state of the environment
        """
        def get_distance(self, asteroid_list) :
            
            def get_xy_distance(x1, y1, x2, y2):
                 distance = ((x1 - x2)**2 + (y1-y2)**2)**(.5)
                 return(distance)
        
            distance = 1000
            if not asteroid_list:
                return(1000, 0)
            
            for asteroid in asteroid_list:
                asteroid_center_x = asteroid['position'][0]
                asteroid_center_y = asteroid['position'][1]
                local_distance = get_xy_distance(asteroid_center_x, asteroid_center_y,
                                         ship.center_x, ship.center_y)
                if local_distance < distance:
                    distance = local_distance
                    current_asteroid = asteroid
            return(distance, current_asteroid)
        
        def get_angle(self, current_asteroid):
            if current_asteroid == 0:
                return(0)
            local_x = ship.center_x - current_asteroid['position'][0]
            local_y = ship.center_y - current_asteroid['position'][1]
            phi = math.atan2(local_y, local_x)*90
            angle = phi + 90 + ship.angle
            while angle > 180 or angle < -180:
                if angle > 180:
                    angle -= 360
                elif angle < -180:
                    angle += 360
            return(angle)
            
        distance, current_asteroid = get_distance(self, input_data['asteroids'])
        angle = get_angle(self, current_asteroid)

        
        self.flying.input['Asteroid_Angle_from_plane'] = angle
        self.flying.input['Asteroid Distance'] = distance
         
    
        self.flying.compute()
        
        ship.turn_rate = self.flying.output['Plane Rotation']
        ship.thrust = self.flying.output['Plane Thrust']
        
        if self.flying.output['Plane Shooting'] > 5:
             ship.shoot()

best_chromosome = [0, 0, 0.22704675799038299, 0.18882866236303364, 1, 0.47358187053744416, 0, 1, 0.585630314551824, 0.790883187507398, 0.27213557586106574, 0, 0, 0, 0.9404657423334345, 1, 0, 0.5853468565829895, 0.6630343126200285, 0.20659052403638267, 0.8678535065106383, 0.07331896008842731, 1, 0, 1, 0.1019020994229195, 0.22845723584997757, 1, 0, 0, 0, 1, 0, 0.36694807573878296, 0.08019529514682067, 0.8204367511415689, 1, 1, 0.9538672228134206, 0.922668852048131, 0.05566674348341649, 0, 0.21565167263721652, 0, 0, 0, 1, 0, 1, 0, 0.01743356009048136, 1, 1, 1]

controller = FuzzyController(best_chromosome)
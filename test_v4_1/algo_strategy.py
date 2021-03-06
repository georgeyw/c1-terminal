import gamelib
import random
import math
import warnings
from sys import maxsize
import json

import unit_locations as ul


"""
Most of the algo code you write will be in this file unless you create new
modules yourself. Start by modifying the 'on_turn' function.

Advanced strategy tips:

  - You can analyze action frames by modifying on_action_frame function

  - The GameState.map object can be manually manipulated to create hypothetical
  board states. Though, we recommended making a copy of the map to preserve
  the actual current map state.
"""

class AlgoStrategy(gamelib.AlgoCore):
    def __init__(self):
        super().__init__()
        # seed = random.randrange(maxsize)
        # random.seed(seed)
        # gamelib.debug_write('Random seed: {}'.format(seed))
        self.mode = 'basic'
        self.offense = 'off'
        self.offense_sp_threshold = 10
        self.offense_mp_threshold = 10 + random.randint(1, 15)
        self.adv_convert_sp_threshold = 90
        self.basic_convert_sp_threshold = 70

        self.sp_savings = 10
        self.sp_projection = 0


        self.all_locations = []
        for x in range(28):
            for y in range(14):
                if x >= 13-y and x <= 14 + y:
                    self.all_locations.append([x, y])

    def on_game_start(self, config):
        """
        Read in config and perform any initial setup here
        """
        gamelib.debug_write('Configuring your custom algo strategy...')
        self.config = config
        global WALL, SUPPORT, TURRET, SCOUT, DEMOLISHER, INTERCEPTOR, MP, SP
        WALL = config["unitInformation"][0]["shorthand"]
        SUPPORT = config["unitInformation"][1]["shorthand"]
        TURRET = config["unitInformation"][2]["shorthand"]
        SCOUT = config["unitInformation"][3]["shorthand"]
        DEMOLISHER = config["unitInformation"][4]["shorthand"]
        INTERCEPTOR = config["unitInformation"][5]["shorthand"]
        MP = 1
        SP = 0
        # This is a good place to do initial setup
        self.scored_on_locations = []

    def on_turn(self, turn_state):
        """
        This function is called every turn with the game state wrapper as
        an argument. The wrapper stores the state of the arena and has methods
        for querying its state, allocating your current resources as planned
        unit deployments, and transmitting your intended deployments to the
        game engine.
        """
        game_state = gamelib.GameState(self.config, turn_state)
        gamelib.debug_write('Performing turn {} of your custom algo strategy'.format(game_state.turn_number))
        game_state.suppress_warnings(True)  #Comment or remove this line to enable warnings.

        self.initial_strategy(game_state)

        game_state.submit_turn()


    def initial_strategy(self, game_state):

        if game_state.turn_number == 0:
            self.first_turn_strategy(game_state)
            self.spawn_offense(game_state)

        elif self.mode == 'basic':
            # defense
            self.maintain_defense(game_state)
            self.remove_damaged_structures(game_state)

            # offense
            self.spawn_offense(game_state)

        elif self.mode == 'advanced':
            # defense
            self.adv_maintain_defense(game_state)
            self.remove_damaged_structures(game_state)
            self.adv_maintain_secondary_defense(game_state)

            current_SP = game_state.get_resource(0)
            current_MP = game_state.get_resource(1)

            # offense
            if self.offense != 'off':
                self.adv_toggle_offense(game_state)
                if self.offense == 'ready':
                    self.adv_spawn_offense(game_state)

            # offense
            elif current_MP > self.offense_mp_threshold and current_SP > self.offense_sp_threshold and self.offense == 'off':
                # reset the mp threshold to something random between 11 and 25
                self.offense_mp_threshold = 10 + random.randint(1, 15) + game_state.turn_number//5
                self.adv_toggle_offense(game_state)



        # total_SP: a function that returns the total SP obtained if every structure is refunded
        # replace REMOVE_FUNCTION with a function that refunds all existing structures

        total_sp = self.total_SP(game_state)
        if total_sp > self.adv_convert_sp_threshold and self.mode != 'advanced':
            self.refund_all(game_state)
            self.mode = 'advanced'

        if self.mode == 'advanced' and total_sp < self.basic_convert_sp_threshold:
            self.refund_all(game_state)
            self.mode = 'basic'


    ##############################
    ########## TURN ONE ##########
    ##############################
    def first_turn_strategy(self, game_state):
        starting_wall_locations = [[0, 13], [1, 12], [3, 12], [4, 12], [5, 12], [6, 11], [7, 10], [8, 9],
                                        [9, 8], [10, 8], [11, 8], [12, 8], [13, 8], [14, 8], [15, 8], [16, 8], [17, 8], [18, 8], [19, 9],
                                        [20, 10], [21, 11], [22, 12], [23, 12], [24, 12], [26, 12], [27, 13]]

        starting_turret_locations = [[4, 11], [23, 11]]

        game_state.attempt_spawn(WALL, starting_wall_locations)
        game_state.attempt_spawn(TURRET, starting_turret_locations)




    ###########################
    ######### DEFENSE #########
    ###########################
    def maintain_defense(self, game_state):
        # actions and locations are ordered in priority from highest to lowest for available SP resources
        # locations defined in on_game_start
        game_state.attempt_spawn(WALL, ul.primary_wall_locations)
        game_state.attempt_spawn(TURRET, ul.primary_turret_locations)
        game_state.attempt_upgrade(ul.primary_upgrade_priority)
        game_state.attempt_spawn(TURRET, ul.secondary_turret_locations)
        game_state.attempt_spawn(WALL, ul.secondary_wall_locations)
        game_state.attempt_upgrade(ul.secondary_upgrade_priority)

        for location in ul.tertiary_support_locations:
            game_state.attempt_spawn(SUPPORT, [location])
            game_state.attempt_upgrade([location])

    def remove_damaged_structures(self, game_state):
        damaged_locations = []
        for location in self.all_locations:
            unit = game_state.game_map[location[0], location[1]]
            if unit:
                if unit[0].health < unit[0].max_health*0.75 and unit[0].health != 60 and unit[0].health != 1:
                    damaged_locations.append(location)

        if damaged_locations:
            game_state.attempt_remove(damaged_locations)

    def adv_maintain_defense(self, game_state):
        if self.offense == 'off':
            game_state.attempt_spawn(WALL, ul.adv_primary_wall_locations)
            game_state.attempt_spawn(TURRET, ul.adv_primary_turret_locations)
            game_state.attempt_upgrade(ul.adv_primary_turret_locations)
            game_state.attempt_spawn(WALL, ul.adv_secondary_wall_locations)
            game_state.attempt_upgrade(ul.adv_upgrade_priority)
            for location in ul.adv_primary_support_locations:
                game_state.attempt_spawn(SUPPORT, location)
                game_state.attempt_upgrade(location)

        else:
            game_state.attempt_spawn(WALL, ul.adv_offensive_wall_locations)
            game_state.attempt_spawn(TURRET, ul.adv_primary_turret_locations)
            game_state.attempt_upgrade(ul.adv_primary_turret_locations)
            game_state.attempt_upgrade(ul.adv_upgrade_priority)
            for location in ul.adv_primary_support_locations:
                game_state.attempt_spawn(SUPPORT, location)
                game_state.attempt_upgrade(location)

    def adv_maintain_secondary_defense(self, game_state):
        current_SP = game_state.get_resource(0)

        for location in ul.adv_secondary_turret_locations:
            self.action_if_affordable(game_state, ('turret', 'build'), location)
            self.action_if_affordable(game_state, ('turret', 'upgrade'), location)
            # affordable, cost = affordable_SP(game_state, ('turret', 'build'), self.sp_savings)
            # if affordable:
            #     game_state.attempt_spawn(TURRET, location)
            #     self.sp_projection -= cost
            # affordable, cost = affordable_SP(game_state, ('turret', 'upgrade'), self.sp_savings)
            # if affordable:
            #     game_state.attempt_upgrade(location)
            #     self.sp_projection -= cost
        for location in ul.adv_secondary_upgrade_priority:
            self.action_if_affordable(game_state, ('turret', 'upgrade'), location)
            # affordable, cost = affordable_SP(game_state, ('wall', 'upgrade'), self.sp_savings)
            # if affordable:
            #     game_state.attempt_upgrade(location)
            #     self.sp_projection -= cost
        for location in ul.adv_secondary_support_locations:
            self.action_if_affordable(game_state, ('support', 'build'), location)
            self.action_if_affordable(game_state, ('support', 'upgrade'), location)
            # affordable, cost = affordable_SP(game_state, ('support', 'build'), self.sp_savings)
            # if affordable:
            #     game_state.attempt_spawn(TURRET, location)
            #     self.sp_projection -= cost
            # affordable, cost = affordable_SP(game_state, ('support', 'upgrade'), self.sp_savings)
            # if affordable:
            #     game_state.attempt_upgrade(location)
            #     self.sp_projection -= cost






    ###########################
    ######### OFFENSE #########
    ###########################
    def spawn_offense(self, game_state):

        current_MP = game_state.get_resource(1)

        # attack 50% of the time if MP is between 7 and 11 or 100% of the time if MP >= 11
        if current_MP < 7:
            return 0
        elif current_MP >= 7 and current_MP < 11:
            if random.random() < 0.5:
                return 0


        location_L1 = [9, 4]
        location_L2 = [5, 8] # this location is 1 space slower than L1 if a support unit exists, currently unused
        location_R1 = [18, 4]
        location_R2 = [22, 8] # this location is 1 space slower than R1 if a support unit exists, currently unused

        if random.random() < 0.5:
            # spawn on the left side
            game_state.attempt_spawn(SCOUT, location_L1, 100)
        else:
            game_state.attempt_spawn(SCOUT, location_R1, 100)


    def adv_spawn_offense(self, game_state):
        game_state.attempt_spawn(SCOUT, self.rand_offense_location(), 100)

    def adv_toggle_offense(self, game_state):
        if self.offense == 'off':
            game_state.attempt_remove(ul.adv_offensive_config_removal)
            self.offense = 'preparing'
        elif self.offense == 'preparing':
            game_state.attempt_spawn(WALL, ul.adv_offensive_config_addition)
            self.offense = 'ready'
        elif self.offense == 'ready':
            game_state.attempt_remove(ul.adv_offensive_config_addition)
            game_state.attempt_spawn(WALL, ul.adv_offensive_config_removal)
            self.offense = 'off'


	############################
	#####Utility Functions######
	############################

	# Compute total SP if all structure refunded
    def total_SP(self, game_state):
        current = game_state.get_resource(SP)
        # if self.mode == 'basic':
        #     all_locations = ul.primary_wall_locations + ul.primary_turret_locations + ul.secondary_turret_locations + ul.secondary_wall_locations + ul.tertiary_support_locations
        # else:
        #     all_locations = ul.adv_primary_wall_locations + ul.adv_primary_turret_locations + ul.adv_secondary_wall_locations + ul.adv_support_locations
        refund = 0
        for location in self.all_locations:
            unit = game_state.game_map[location[0],location[1]]
            if unit:
                if unit[0].upgraded:
                    if unit[0].health == 60:
                        refund += unit[0].cost[0]*0.90
                    else:
                        refund += unit[0].cost[0]*0.90*(unit[0].health/unit[0].max_health)
                else:
                    refund += unit[0].cost[0]*0.97*(unit[0].health/unit[0].max_health)
        return round(current + refund,1)


	# Refund all units
    def refund_all(self, game_state):
        # all_locations = ul.primary_wall_locations + ul.primary_turret_locations + ul.secondary_turret_locations + ul.secondary_wall_locations + ul.tertiary_support_locations
        game_state.attempt_remove(self.all_locations)

    # compute SP after an action
    # action type: (UNIT, ACTION) e.g. ('turret', 'upgrade') or ('wall', 'build')
    def affordable_SP(self, game_state, action_type, sp_savings):
        current_SP = game_state.get_resource(0)
        if action_type[1] == 'build':
            if action_type[0] == 'wall' or action_type[0] == WALL:
                cost = 1
            elif action_type[0] == 'turret' or action_type[0] == TURRET:
                cost = 2
            elif action_type[0] == 'support' or action_type[0] == TURRET:
                cost = 4
        elif action_type[1] == 'upgrade':
            if action_type[0] == 'wall' or action_type[0] == WALL:
                cost = 2
            elif action_type[0] == 'turret' or action_type[0] == TURRET:
                cost = 4
            elif action_type[0] == 'support' or action_type[0] == TURRET:
                cost = 4

        return current_SP - cost > sp_savings, cost

    def action_if_affordable(self, game_state, action_type, location):
        affordable, cost = self.affordable_SP(game_state, action_type, self.sp_savings)
        if affordable and action_type[1] == 'build':
            if action_type[0] == 'turret':
                unit = game_state.game_map[location[0],location[1]]
                if unit:
                    if unit[0].unit_type  == 'FF':
                        #remove the wall if there is a wall
                        game_state.attempt_remove(location)
                        #remove location from wall list
                        ul.adv_primary_wall_locations.remove(location)
                # Build turret at adv_secondary_turret_locations
                game_state.attempt_spawn(TURRET, location)
            elif action_type[0] == 'wall':
                game_state.attempt_spawn(WALL, location)
            elif action_type[0] == 'support':
                game_state.attempt_spawn(SUPPORT, location)
        elif affordable and action_type[1] == 'upgrade':
            game_state.attempt_upgrade(location)

    # Random generator for offense location, left or right
    def rand_offense_location(self):
        random.seed()
        rand = random.randint(0,len(ul.adv_spawn_location)-1)
        return ul.adv_spawn_location[rand]
    





    # def starter_strategy(self, game_state):
    #     """
    #     For defense we will use a spread out layout and some interceptors early on.
    #     We will place turrets near locations the opponent managed to score on.
    #     For offense we will use long range demolishers if they place stationary units near the enemy's front.
    #     If there are no stationary units to attack in the front, we will send Scouts to try and score quickly.
    #     """
    #     # First, place basic defenses
    #     self.build_defences(game_state)
    #     # Now build reactive defenses based on where the enemy scored
    #     self.build_reactive_defense(game_state)
    #
    #     # If the turn is less than 5, stall with interceptors and wait to see enemy's base
    #     if game_state.turn_number < 5:
    #         self.stall_with_interceptors(game_state)
    #     else:
    #         # Now let's analyze the enemy base to see where their defenses are concentrated.
    #         # If they have many units in the front we can build a line for our demolishers to attack them at long range.
    #         if self.detect_enemy_unit(game_state, unit_type=None, valid_x=None, valid_y=[14, 15]) > 10:
    #             self.demolisher_line_strategy(game_state)
    #         else:
    #             # They don't have many units in the front so lets figure out their least defended area and send Scouts there.
    #
    #             # Only spawn Scouts every other turn
    #             # Sending more at once is better since attacks can only hit a single scout at a time
    #             if game_state.turn_number % 2 == 1:
    #                 # To simplify we will just check sending them from back left and right
    #                 scout_spawn_location_options = [[13, 0], [14, 0]]
    #                 best_location = self.least_damage_spawn_location(game_state, scout_spawn_location_options)
    #                 game_state.attempt_spawn(SCOUT, best_location, 1000)
    #
    #             # Lastly, if we have spare SP, let's build some Factories to generate more resources
    #             support_locations = [[13, 2], [14, 2], [13, 3], [14, 3]]
    #             game_state.attempt_spawn(SUPPORT, support_locations)
    #
    # def build_defences(self, game_state):
    #     """
    #     Build basic defenses using hardcoded locations.
    #     Remember to defend corners and avoid placing units in the front where enemy demolishers can attack them.
    #     """
    #     # Useful tool for setting up your base locations: https://www.kevinbai.design/terminal-map-maker
    #     # More community tools available at: https://terminal.c1games.com/rules#Download
    #
    #     # Place turrets that attack enemy units
    #     turret_locations = [[0, 13], [27, 13], [8, 11], [19, 11], [13, 11], [14, 11]]
    #     # attempt_spawn will try to spawn units if we have resources, and will check if a blocking unit is already there
    #     game_state.attempt_spawn(TURRET, turret_locations)
    #
    #     # Place walls in front of turrets to soak up damage for them
    #     wall_locations = [[8, 12], [19, 12]]
    #     game_state.attempt_spawn(WALL, wall_locations)
    #     # upgrade walls so they soak more damage
    #     game_state.attempt_upgrade(wall_locations)
    #
    # def build_reactive_defense(self, game_state):
    #     """
    #     This function builds reactive defenses based on where the enemy scored on us from.
    #     We can track where the opponent scored by looking at events in action frames
    #     as shown in the on_action_frame function
    #     """
    #     for location in self.scored_on_locations:
    #         # Build turret one space above so that it doesn't block our own edge spawn locations
    #         build_location = [location[0], location[1]+1]
    #         game_state.attempt_spawn(TURRET, build_location)
    #
    # def stall_with_interceptors(self, game_state):
    #     """
    #     Send out interceptors at random locations to defend our base from enemy moving units.
    #     """
    #     # We can spawn moving units on our edges so a list of all our edge locations
    #     friendly_edges = game_state.game_map.get_edge_locations(game_state.game_map.BOTTOM_LEFT) + game_state.game_map.get_edge_locations(game_state.game_map.BOTTOM_RIGHT)
    #
    #     # Remove locations that are blocked by our own structures
    #     # since we can't deploy units there.
    #     deploy_locations = self.filter_blocked_locations(friendly_edges, game_state)
    #
    #     # While we have remaining MP to spend lets send out interceptors randomly.
    #     while game_state.get_resource(MP) >= game_state.type_cost(INTERCEPTOR)[MP] and len(deploy_locations) > 0:
    #         # Choose a random deploy location.
    #         deploy_index = random.randint(0, len(deploy_locations) - 1)
    #         deploy_location = deploy_locations[deploy_index]
    #
    #         game_state.attempt_spawn(INTERCEPTOR, deploy_location)
    #         """
    #         We don't have to remove the location since multiple mobile
    #         units can occupy the same space.
    #         """
    #
    # def demolisher_line_strategy(self, game_state):
    #     """
    #     Build a line of the cheapest stationary unit so our demolisher can attack from long range.
    #     """
    #     # First let's figure out the cheapest unit
    #     # We could just check the game rules, but this demonstrates how to use the GameUnit class
    #     stationary_units = [WALL, TURRET, SUPPORT]
    #     cheapest_unit = WALL
    #     for unit in stationary_units:
    #         unit_class = gamelib.GameUnit(unit, game_state.config)
    #         if unit_class.cost[game_state.MP] < gamelib.GameUnit(cheapest_unit, game_state.config).cost[game_state.MP]:
    #             cheapest_unit = unit
    #
    #     # Now let's build out a line of stationary units. This will prevent our demolisher from running into the enemy base.
    #     # Instead they will stay at the perfect distance to attack the front two rows of the enemy base.
    #     for x in range(27, 5, -1):
    #         game_state.attempt_spawn(cheapest_unit, [x, 11])
    #
    #     # Now spawn demolishers next to the line
    #     # By asking attempt_spawn to spawn 1000 units, it will essentially spawn as many as we have resources for
    #     game_state.attempt_spawn(DEMOLISHER, [24, 10], 1000)
    #
    # def least_damage_spawn_location(self, game_state, location_options):
    #     """
    #     This function will help us guess which location is the safest to spawn moving units from.
    #     It gets the path the unit will take then checks locations on that path to
    #     estimate the path's damage risk.
    #     """
    #     damages = []
    #     # Get the damage estimate each path will take
    #     for location in location_options:
    #         path = game_state.find_path_to_edge(location)
    #         damage = 0
    #         for path_location in path:
    #             # Get number of enemy turrets that can attack each location and multiply by turret damage
    #             damage += len(game_state.get_attackers(path_location, 0)) * gamelib.GameUnit(TURRET, game_state.config).damage_i
    #         damages.append(damage)
    #
    #     # Now just return the location that takes the least damage
    #     return location_options[damages.index(min(damages))]
    #
    # def detect_enemy_unit(self, game_state, unit_type=None, valid_x = None, valid_y = None):
    #     total_units = 0
    #     for location in game_state.game_map:
    #         if game_state.contains_stationary_unit(location):
    #             for unit in game_state.game_map[location]:
    #                 if unit.player_index == 1 and (unit_type is None or unit.unit_type == unit_type) and (valid_x is None or location[0] in valid_x) and (valid_y is None or location[1] in valid_y):
    #                     total_units += 1
    #     return total_units
    #
    # def filter_blocked_locations(self, locations, game_state):
    #     filtered = []
    #     for location in locations:
    #         if not game_state.contains_stationary_unit(location):
    #             filtered.append(location)
    #     return filtered
    #
    # def on_action_frame(self, turn_string):
    #     """
    #     This is the action frame of the game. This function could be called
    #     hundreds of times per turn and could slow the algo down so avoid putting slow code here.
    #     Processing the action frames is complicated so we only suggest it if you have time and experience.
    #     Full doc on format of a game frame at in json-docs.html in the root of the Starterkit.
    #     """
    #     # Let's record at what position we get scored on
    #     state = json.loads(turn_string)
    #     events = state["events"]
    #     breaches = events["breach"]
    #     for breach in breaches:
    #         location = breach[0]
    #         unit_owner_self = True if breach[4] == 1 else False
    #         # When parsing the frame data directly,
    #         # 1 is integer for yourself, 2 is opponent (StarterKit code uses 0, 1 as player_index instead)
    #         if not unit_owner_self:
    #             gamelib.debug_write("Got scored on at: {}".format(location))
    #             self.scored_on_locations.append(location)
    #             gamelib.debug_write("All locations: {}".format(self.scored_on_locations))


if __name__ == "__main__":
    algo = AlgoStrategy()
    algo.start()

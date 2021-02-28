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
        self.mode = 'defense'
        self.offense = 'off'
        self.attack_type = 'dynamic'
        self.attack_side = 'left'

        self.offense_sp_threshold = 10
        self.offense_sp_counter = 0
        self.offense_mp_threshold = 7 + random.randint(0, 5)
        self.adv_convert_sp_threshold = 90
        self.basic_convert_sp_threshold = 70

        self.sp_savings = 10

        self.all_locations = []
        for x in range(28):
            for y in range(14):
                if x >= 13-y and x <= 14 + y:
                    self.all_locations.append([x, y])

    def mp_threshold_generator(self, game_state):
        bonus_MP = game_state.turn_number//10
        return 10 + bonus_MP * 3

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

        self.initial_strategy_new_offense_and_defense(game_state)

        game_state.submit_turn()


    def initial_strategy(self, game_state):

        if self.mode == 'basic':
            self.maintain_defense_v2(game_state, ul.basic_v2_build_order)

            self.remove_damaged_structures(game_state)

            if game_state.turn_number != 0:
                self.spawn_offense_v2(game_state)

        elif self.mode == 'advanced':
            # defense
            if self.offense == 'off':
                self.maintain_defense_v2(game_state, ul.adv_build_order)
            else:
                self.maintain_defense_v2(game_state, ul.adv_offense_build_order)

            self.remove_damaged_structures(game_state)

            self.maintain_excess_defense_v2(game_state, ul.adv_excess_build_order)

            current_SP = game_state.get_resource(0)
            current_MP = game_state.get_resource(1)

            # offense
            if self.offense != 'off':
                self.adv_toggle_offense(game_state)
                if self.offense == 'ready':
                    if random.random() < 0.4:
                        attack_type = 'demolisher'
                    else:
                        attack_type = 'scout'
                    self.spawn_offense_v2(game_state, attack_type = attack_type)

            elif current_MP > self.offense_mp_threshold:
                self.offense_sp_counter += 1
                # if a number of turns with enough MP but not enough SP have accrued, then attack anyways
                if current_SP > self.offense_sp_threshold or self.offense_sp_counter > 5:
                    # reset the mp threshold
                    bonus_MP = game_state.turn_number//10
                    self.offense_mp_threshold = 10 + random.randint(bonus_MP, 5 + 2*bonus_MP)
                    # reset the offense counter
                    self.offense_sp_counter = 0

                    self.adv_toggle_offense(game_state)



        total_sp = self.total_SP(game_state)
        if total_sp > self.adv_convert_sp_threshold and self.mode != 'advanced':
            self.refund_all(game_state)
            self.mode = 'advanced'

        if self.mode == 'advanced' and total_sp < self.basic_convert_sp_threshold:
            self.refund_all(game_state)
            self.mode = 'basic'
            self.offense = 'off'



    def initial_strategy_new_offense(self, game_state):

        if self.mode == 'basic' and self.offense == 'off':
            self.maintain_defense_v2(game_state, ul.basic_v2_new_build_order)

            self.remove_damaged_structures(game_state)


        elif self.mode == 'advanced' and self.offense == 'off':
            # defense
            self.maintain_defense_v2(game_state, ul.adv_new_build_order)

            self.remove_damaged_structures(game_state)

            self.maintain_excess_defense_v2(game_state, ul.adv_new_excess_build_order)

        current_SP = game_state.get_resource(0)
        current_MP = game_state.get_resource(1)

        # offense
        if game_state.turn_number == 1:
            self.spawn_offense_v2(game_state)
        elif self.offense != 'off':
            self.spawn_new_offense(game_state, attack_type = self.attack_type, side = self.attack_side)
            self.toggle_new_offense(game_state, side = self.attack_side)
        elif current_MP > self.offense_mp_threshold:
            if random.random() < 0.5:
                self.attack_side = 'left'
            else:
                self.attack_side = 'right'

            bonus_MP = game_state.turn_number//10
            self.offense_mp_threshold = mp_threshold_generator(game_state)

            self.toggle_new_offense(game_state, side = self.attack_side)


        total_sp = self.total_SP(game_state)
        if total_sp > self.adv_convert_sp_threshold and self.mode != 'advanced':
            self.refund_all(game_state)
            self.mode = 'advanced'

        if self.mode == 'advanced' and total_sp < self.basic_convert_sp_threshold:
            self.refund_all(game_state)
            self.mode = 'basic'
            self.offense = 'off'



    def initial_strategy_new_offense_and_defense(self, game_state):

        if self.offense == 'off':
            self.maintain_defense_v2(game_state, ul.defense_build_order)
            self.remove_damaged_structures(game_state)

        current_SP = game_state.get_resource(0)
        current_MP = game_state.get_resource(1)

        # offense
        if game_state.turn_number == 1:
            self.spawn_offense_v2(game_state)
        elif self.offense != 'off':
            self.spawn_new_offense(game_state, attack_type = self.attack_type, side = self.attack_side)
            self.toggle_new_offense(game_state, side = self.attack_side)
        elif current_MP > self.offense_mp_threshold:
            if random.random() < 0.5:
                self.attack_side = 'left'
            else:
                self.attack_side = 'right'

            bonus_MP = game_state.turn_number//10
            self.offense_mp_threshold = mp_threshold_generator(game_state)

            self.toggle_new_offense(game_state, side = self.attack_side)


    ###########################
    ######### DEFENSE #########
    ###########################

    def maintain_defense_v2(self, game_state, build_commands):
        unit_dictionary = {'wall': WALL, 'turret': TURRET, 'support': SUPPORT}
        for current_command in build_commands:
            action_type = current_command[0]
            locations = current_command[1]
            for location in locations:
                if action_type[1] == 'build':
                    if action_type[0] == 'turret':
                        self.replace_wall_with_turret(game_state,location)
                    else:
                        game_state.attempt_spawn(unit_dictionary[action_type[0]], location)
                elif action_type[1] == 'upgrade':
                    game_state.attempt_upgrade(locations)

    def maintain_excess_defense_v2(self, game_state, build_commands):
        for current_command in build_commands:
            action_type = current_command[0]
            locations = current_command[1]
            for location in locations:
                self.action_if_affordable(game_state, action_type, location)


    def remove_damaged_structures(self, game_state):
        damaged_locations = []
        for location in self.all_locations:
            unit = game_state.game_map[location[0], location[1]]
            if unit:
                if unit[0].health < unit[0].max_health and unit[0].health != 60 and unit[0].health != 1:
                    damaged_locations.append(location)

        if damaged_locations:
            game_state.attempt_remove(damaged_locations)






    ###########################
    ######### OFFENSE #########
    ###########################

    def spawn_new_offense(self, game_state, attack_type = 'scout', side = 'none'):
        if side == 'none':
            if random.random() < 0.5:
                side = 'right'
            else:
                side = 'left'

        if side == 'left':
            location_1 = [12, 1]
            location_2 = [13, 0]
        else:
            location_1 = [15, 1]
            location_2 = [14, 0]

        target_location = game_state.find_path_to_edge(location_1)[-1]
        edge_locations = [[0, 14], [1, 15], [2, 16], [3, 17], [4, 18], [5, 19], [6, 20], [7, 21], [8, 22], [9, 23], [10, 24], [11, 25], [12, 26], [13, 27],
                            [14, 27], [15, 26], [16, 25], [17, 24], [18, 23], [19, 22], [20, 21], [21, 20], [22, 19], [23, 18], [24, 17], [25, 16], [26, 15], [27, 14]]

        if target_location in edge_locations:
            path = 'open'
        else:
            path = 'closed'

        if attack_type == 'dynamic':
            if path == 'open':
                scout_count = game_state.number_affordable(SCOUT)
                if scout_count >= 20:
                    game_state.attempt_spawn(SCOUT, location_1, min(scout_count//2, 15))
                game_state.attempt_spawn(SCOUT, location_2, 100)
            elif path == 'closed':
                game_state.attempt_spawn(DEMOLISHER, location_2, 100)


        elif attack_type == 'scout':
            scout_count = game_state.number_affordable(SCOUT)
            if scout_count >= 20:
                game_state.attempt_spawn(SCOUT, location_1, min(scout_count//2, 15))
            game_state.attempt_spawn(SCOUT, location_2, 100)

        elif attack_type == 'demolisher':
            game_state.attempt_spawn(DEMOLISHER, location_2, 100)


    def toggle_new_offense(self, game_state, side = 'left'):
        if self.offense == 'off':
            game_state.attempt_remove(self.all_locations)
            self.offense = 'ready'
        elif self.offense == 'ready':
            if side == 'left':
                self.maintain_defense_v2(game_state, ul.offense_build_order)
            else:
                self.maintain_defense_v2(game_state, ul.offense_build_order_reversed)
            game_state.attempt_remove(self.all_locations)
            self.offense = 'off'


    def spawn_offense_v2(self, game_state, attack_type = 'scout', side = 'none'):
        current_MP = game_state.get_resource(1)
        if current_MP < self.offense_mp_threshold:
            return 0

        bonus_MP = game_state.turn_number//10
        self.offense_mp_threshold = 8 + random.randint(bonus_MP, 5 + 2*bonus_MP)
        if side == 'none':
            if random.random() < 0.5:
                side = 'right'
            else:
                side = 'left'

        if side == 'right':
            location_1 = [18, 4]
            location_2 = [17, 3]
        else:
            location_1 = [8, 5]
            location_2 = [9, 4]


        # send scouts in two waves if there are enough scouts, otherwise just send one big wave
        if attack_type == 'scout':
            scout_count = game_state.number_affordable(SCOUT)
            if scout_count >= 20:
                game_state.attempt_spawn(SCOUT, location_2, min(scout_count//2, 15))
            game_state.attempt_spawn(SCOUT, location_1, 100)

        # build as many demolishers as possible
        elif attack_type == 'demolisher':
            game_state.attempt_spawn(DEMOLISHER, location_1, 100)

        # staggered interceptor spawns
        elif attack_type == 'interceptor':
            interceptor_count = game_state.number_affordable(INTERCEPTOR)
            game_state.attempt_spawn(INTERCEPTOR, location_1, interceptor_count//2)
            game_state.attempt_spawn(INTERCEPTOR, [0, 13], 100)


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
                self.replace_wall_with_turret(game_state,location)
            elif action_type[0] == 'wall':
                game_state.attempt_spawn(WALL, location)
            elif action_type[0] == 'support':
                game_state.attempt_spawn(SUPPORT, location)
        elif affordable and action_type[1] == 'upgrade':
            game_state.attempt_upgrade(location)

    # Replace an existing wall with a turret
    def replace_wall_with_turret(self,game_state,location):
        unit = game_state.game_map[location[0],location[1]]
        if unit:
            if unit[0].unit_type == 'FF':
                game_state.attempt_remove(location)
                #remove location from wall list
                for i in range(len(ul.defense_wall_locations)):
                   if location in ul.defense_wall_locations[i]:
                      ul.defense_wall_locations[i].remove(location)
        game_state.attempt_spawn(TURRET,location)



if __name__ == "__main__":
    algo = AlgoStrategy()
    algo.start()

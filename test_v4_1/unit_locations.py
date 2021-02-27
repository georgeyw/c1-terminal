primary_wall_locations = [
                  [4, 12], [5, 12], [3, 12], # left turret front
                  [23, 12], [22, 12], [24, 12], # right turret front
                  # center wall
                  [6, 11], [7, 10], [8, 9], [9, 8], [10, 8], [11, 8], [12, 8], [13, 8],
                  [14, 8], [15, 8], [16, 8], [17, 8], [18, 8], [19, 9], [20, 10], [21, 11],

                  [0, 13], [1, 12], # left corner partial
                  [27, 13], [26, 12], # right corner partial
                 ]

primary_turret_locations = [[4, 11], [23, 11]]

primary_upgrade_priority = [
                            [4, 11], [23, 11], # primary turrets
                            # primary walls in front of turrets, alternating
                            [4, 12], [23, 12],
                            [5, 12], [22, 12],
                            [3, 12], [24, 12],
                           ]

secondary_turret_locations = [[5, 11], [22, 11]]

secondary_wall_locations = [[1, 13], # left corner third wall
                                 [26, 13] # right corner third wall
                                 ]

secondary_upgrade_priority = [
                              [5, 11], [22, 11], # secondary turrets
                              # corner walls
                              [1, 13], [26, 13],
                              [0, 13], [27, 13],
                              [1, 12], [26, 12]]

tertiary_support_locations = [[13, 8], [14, 8],
                              [13, 7], [14, 7]]

# adv config at 90+ SP
adv_primary_wall_locations = [[0, 13], [1, 13], [2, 13], [1, 12], [2, 12], [3, 12],
                         [3, 11], [4, 11], [4, 10], [4, 9], [5, 10], [5, 9],
                         [5, 8], [6, 8], [7, 8], [6, 7],
                         [7, 9], [8, 9], [9, 9], [10, 9], [11, 9], [12, 9], [13, 9],
                         [14, 9], [15, 9], [16, 9], [17, 9], [18, 9], [19, 9], [20, 9],
                         [20, 8], [21, 8], [22, 8], [21, 7], [22, 9], [22, 10], [23, 9], [23, 10],
                         [23, 11], [24, 11], [24, 12], [25, 12], [26, 12],
                         [25, 13], [26, 13], [27, 13],
                         [13,8],[9,8],[18,8]]

adv_secondary_wall_locations = [[15, 8], [12, 8],
                            [10, 8], [17, 8], [11, 8], [16, 8]]

adv_primary_turret_locations = [[2, 11], [25, 11], [8, 8], [19, 8], [14, 8]]


adv_primary_support_locations = [[8, 6], [9, 6]]

adv_offensive_wall_locations = [ # primary locations
                         [0, 13], [1, 13], [2, 13], [1, 12], [2, 12], [3, 12],
                         [3, 11], [4, 11], [4, 10], [4, 9], [5, 9],
                         [5, 8], [6, 8], [7, 8], [6, 7],
                         [7, 9], [8, 9], [9, 9], [10, 9], [12, 9], [13, 9],
                         [14, 9], [15, 9], [16, 9], [17, 9], [18, 9], [19, 9], [20, 9],
                         [20, 8], [21, 8], [22, 8], [21, 7], [22, 9], [23, 9], [23, 10],
                         [23, 11], [24, 11], [24, 12], [25, 12], [26, 12],
                         [25, 13], [26, 13], [27, 13],
                         # secondary locations
                         [15, 8],
                         [10, 8], [12, 8], [17, 8], [16, 8]]

adv_offensive_config_removal = [[11, 9], [11, 8]]

# offensive swap only at 10+ SP
adv_offensive_config_addition = [[10, 7], [11, 6], [12, 5], [13, 5], [14, 5], [15, 5], [13, 7], [14, 7], [16, 6], [18, 7]]

adv_upgrade_priority = [[0, 13], [27, 13], [6, 8], [21, 8], [5, 9], [22, 9], [7, 9], [20, 9]]

# first build secondary turrets and then upgrade them
# next upgrade wall locations
# build + upgrade supports


adv_secondary_turret_locations = [[13, 8], [9, 8], [18, 8], [3, 10], [24, 10]]

adv_secondary_support_locations = [[10, 5], [11, 4], [12, 3], [13, 2], [14, 2], [15, 3], [16, 4], [17, 5]]

adv_secondary_upgrade_priority = [[1, 13], [26, 13], [2, 13], [25, 13], [3, 12], [24, 12], [4, 11], [23, 11], # 1, 2, 3, 4
                                  [13, 9], [14, 9], [12, 9], [15, 9], # 5
                                  [8, 9], [19, 9], [9, 9], [18, 9], # 6, 7
                                  [10, 9], [17, 9], [11, 9], [16, 9] # 8, 9
                                  ]

adv_spawn_location = [[9,4],[18,4]]

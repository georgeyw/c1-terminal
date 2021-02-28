####################
##### BASIC V1 #####
####################

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

tertiary_support_locations = [[13, 7], [14, 7],
                              [13, 6], [14, 6]]



##################
##### ADV V1 #####
##################
# adv config at 90+ SP

adv_primary_wall_locations = [[0, 13], [1, 12], [2, 12], [3, 12],
                         [3, 11], [4, 11], [4, 10], [4, 9], [5, 10], [5, 9],
                         [5, 8], [6, 8], [7, 7], [6, 7],
                         [7, 9], [8, 9], [9, 9], [10, 9], [11, 9], [12, 9], [13, 9],
                         [14, 9], [15, 9], [16, 9], [17, 9], [18, 9], [19, 9], [20, 9],
                         [20, 7], [21, 8], [22, 8], [21, 7], [22, 9], [22, 10], [23, 9], [23, 10],
                         [23, 11], [24, 11], [24, 12], [25, 12], [26, 12],
                         [27, 13],
                         [13, 8], [9, 8], [18, 8]]

# adv_primary_wall_locations = [[0, 13], [1, 13], [2, 13], [1, 12], [2, 12], [3, 12],
#                          [3, 11], [4, 11], [4, 10], [4, 9], [5, 10], [5, 9],
#                          [5, 8], [6, 8], [7, 8], [6, 7],
#                          [7, 9], [8, 9], [9, 9], [10, 9], [11, 9], [12, 9], [13, 9],
#                          [14, 9], [15, 9], [16, 9], [17, 9], [18, 9], [19, 9], [20, 9],
#                          [20, 8], [21, 8], [22, 8], [21, 7], [22, 9], [22, 10], [23, 9], [23, 10],
#                          [23, 11], [24, 11], [24, 12], [25, 12], [26, 12],
#                          [25, 13], [26, 13], [27, 13],
#                          [13, 8], [9, 8], [18, 8]]

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

adv_upgrade_priority = [[0, 13], [27, 13], [6, 8], [21, 8], [5, 9], [22, 9], [7, 9], [20, 9], [5, 10], [22, 10]]


adv_build_order = [[('wall', 'build'), adv_primary_wall_locations],
                    [('turret', 'build'), adv_primary_turret_locations],
                    [('turret', 'upgrade'), adv_primary_turret_locations],
                    [('wall', 'build'), adv_secondary_wall_locations],
                    [('wall', 'upgrade'), adv_upgrade_priority],
                    [('support', 'build'), adv_primary_support_locations],
                    [('support', 'upgrade'), adv_primary_support_locations]]

adv_offense_build_order = [[('wall', 'build'), adv_offensive_wall_locations],
                            [('turret', 'build'), adv_primary_turret_locations],
                            [('turret', 'upgrade'), adv_primary_turret_locations],
                            [('wall', 'upgrade'), adv_upgrade_priority],
                            [('support', 'build'), adv_primary_support_locations],
                            [('support', 'upgrade'), adv_primary_support_locations]]

adv_new_build_order = [[('wall', 'build'), adv_primary_wall_locations],
                    [('turret', 'build'), adv_primary_turret_locations],
                    [('turret', 'upgrade'), adv_primary_turret_locations],
                    [('wall', 'build'), adv_secondary_wall_locations],
                    [('wall', 'upgrade'), adv_upgrade_priority]]




# first build secondary turrets and then upgrade them
# next upgrade wall locations
# build + upgrade supports


adv_secondary_turret_locations = [[13, 8], [9, 8], [18, 8], [3, 10], [24, 10]]

adv_secondary_support_locations = [[10, 5], [11, 4], [12, 3], [13, 2], [14, 2], [15, 3], [16, 4], [17, 5]]

adv_secondary_upgrade_priority = [[1, 12], [26, 12], [2, 12], [25, 12], [3, 12], [24, 12], [4, 11], [23, 11], # 1, 2, 3, 4
                                  [13, 9], [14, 9], [12, 9], [15, 9], # 5
                                  [8, 9], [19, 9], [9, 9], [18, 9], # 6, 7
                                  [10, 9], [17, 9], [11, 9], [16, 9], # 8, 9
                                  ]

# these ones will require the replacement function
adv_tertiary_turret_locations = [[15, 8], [10, 8], [17, 8], [12, 8], [4, 9], [23, 9]]

adv_tertiary_upgrade_priority = [[5, 8], [6, 7], [7, 7], [22, 8], [21, 7], [20, 7], # fortifying the two choke points
                                 [2, 12], [3, 11], [4, 10], [25, 12], [24, 11], [23, 10]] # fortifying the left and right edges]

adv_tertiary_support_locations = [[9, 7], [10, 6], [11, 5], [12, 4], [13, 3], [13, 4], [14, 3], [14, 4], [15, 4], [16, 5]]


adv_excess_build_order = [[('turret', 'build'), adv_secondary_turret_locations],
                          [('turret', 'upgrade'), adv_secondary_turret_locations],
                          [('wall', 'upgrade'), adv_secondary_upgrade_priority],
                          [('support', 'build'), adv_secondary_support_locations],
                          [('support', 'upgrade'), adv_secondary_support_locations],
                          [('turret', 'build'), adv_tertiary_turret_locations],
                          [('turret', 'upgrade'), adv_tertiary_turret_locations],
                          [('wall', 'upgrade'), adv_tertiary_turret_locations],
                          [('support', 'build'), adv_tertiary_support_locations],
                          [('support', 'upgrade'), adv_tertiary_support_locations]]

adv_new_excess_build_order = [[('turret', 'build'), adv_secondary_turret_locations],
                          [('turret', 'upgrade'), adv_secondary_turret_locations],
                          [('wall', 'upgrade'), adv_secondary_upgrade_priority],
                          [('support', 'build'), adv_secondary_support_locations],
                          [('support', 'upgrade'), adv_secondary_support_locations],
                          [('turret', 'build'), adv_tertiary_turret_locations],
                          [('turret', 'upgrade'), adv_tertiary_turret_locations],
                          [('wall', 'upgrade'), adv_tertiary_turret_locations]]

####################
##### BASIC V2 #####
####################

# new build locations
basic_v2_build_order = [[('wall', 'build'), [[0, 13], [1, 12], [2, 11], [3, 10], [4, 9], [5, 8],
                                            [6, 7], [7, 7], [8, 7], [9, 7], [10, 7], [11, 7], [12, 7], [13, 7], [14, 7], [15, 7], [16, 7], [17, 7], [18, 7],
                                            [19, 8], [20, 9], [21, 10], [22, 12], [25, 12], [26, 12], [27, 13]]
                                            ],
                      [('turret', 'build'), [[22, 11], [25, 11]]
                                            ],
                      [('turret', 'upgrade'), [[22, 11]]
                                            ],
                      [('wall', 'build'), [[21, 12], [24, 12]]
                                            ],
                      [('turret', 'build'), [[21, 11], [24, 11]]
                                            ],
                      [('wall', 'build'), [[20, 11]]
                                            ],
                      [('turret', 'upgrade'), [[25, 11]]
                                            ],
                      [('wall', 'upgrade'), [[0, 13], [1, 12], [2, 11], [3, 10], [21, 12], [27, 13], [25, 12]]
                                            ],
                      [('turret', 'upgrade'), [[21, 11], [24, 11]]
                                            ],
                      [('wall', 'upgrade'), [[22, 12], [26, 12], [24, 12], [20, 11], [24, 10], [23, 9], [22, 8]]
                                            ],
                      [('support', 'build'), [[9, 6], [10, 6], [10, 5], [11, 5], [11, 4]]
                                            ],
                      [('support', 'upgrade'), [[9, 6], [10, 6], [10, 5], [11, 5], [11, 4]]
                                            ],
# builds past this point should only really happen if conversion back occurs
                        [('wall', 'build'), [[20, 12], [19, 11], [20, 10]]
                                    ],
                        [('wall', 'upgrade'), [[20, 12], [19, 11]]
                                    ],
                        [('turret', 'build'), [[20, 11]]
                                    ],
                        [('turret', 'upgrade'), [[20, 11]]
                                    ],
                        [('turret', 'build'), [[24, 10]]
                                    ],
                        [('turret', 'upgrade'), [[24, 10]]
                                    ],
                        [('turret', 'build'), [[21, 10]]
                                    ],
                        [('turret', 'upgrade'), [[21, 10]]
                                    ],
                        [('turret', 'build'), [[25, 12]]
                                    ],
                        [('turret', 'upgrade'), [[25, 12]]
                                    ],
                        [('support', 'build'), [[12, 4], [12, 3], [13, 3], [13, 2]]
                                    ],
                        [('support', 'upgrade'), [[12, 4], [12, 3], [13, 3], [13, 2]]
                                    ]]


basic_v2_new_build_order = [[('wall', 'build'), [[0, 13], [1, 12], [2, 11], [3, 10], [4, 9], [5, 8],
                                            [6, 7], [7, 7], [8, 7], [9, 7], [10, 7], [11, 7], [12, 7], [13, 7], [14, 7], [15, 7], [16, 7], [17, 7], [18, 7],
                                            [19, 8], [20, 9], [21, 10], [22, 12], [25, 12], [26, 12], [27, 13]]
                                            ],
                      [('turret', 'build'), [[22, 11], [25, 11]]
                                            ],
                      [('turret', 'upgrade'), [[22, 11]]
                                            ],
                      [('wall', 'build'), [[21, 12], [24, 12]]
                                            ],
                      [('turret', 'build'), [[21, 11], [24, 11]]
                                            ],
                      [('wall', 'build'), [[20, 11]]
                                            ],
                      [('turret', 'upgrade'), [[25, 11]]
                                            ],
                      [('wall', 'upgrade'), [[0, 13], [1, 12], [2, 11], [3, 10], [21, 12], [27, 13], [25, 12]]
                                            ],
                      [('turret', 'upgrade'), [[21, 11], [24, 11]]
                                            ],
                      [('wall', 'upgrade'), [[22, 12], [26, 12], [24, 12], [20, 11], [24, 10], [23, 9], [22, 8]]
                                            ],
# builds past this point should only really happen if conversion back occurs
                        [('wall', 'build'), [[20, 12], [19, 11], [20, 10]]
                                    ],
                        [('wall', 'upgrade'), [[20, 12], [19, 11]]
                                    ],
                        [('turret', 'build'), [[20, 11]]
                                    ],
                        [('turret', 'upgrade'), [[20, 11]]
                                    ],
                        [('turret', 'build'), [[24, 10]]
                                    ],
                        [('turret', 'upgrade'), [[24, 10]]
                                    ],
                        [('turret', 'build'), [[21, 10]]
                                    ],
                        [('turret', 'upgrade'), [[21, 10]]
                                    ],
                        [('turret', 'build'), [[25, 12]]
                                    ],
                        [('turret', 'upgrade'), [[25, 12]]
                                    ]]

import copy

basic_v2_new_build_order_reversed = copy.deepcopy(basic_v2_new_build_order)

for order in basic_v2_new_build_order_reversed:
    for location in order[1]:
        location[0] = 27 - location[0]




all_wall_locations = [adv_primary_wall_locations, adv_secondary_wall_locations, adv_offensive_wall_locations]



###################################
######## NEW DEFENSE ##############
###################################

defense_wall_locations=[
                       [0,13],[1,12],[27,13],[26,12], #round 1 build
                       [2,12],[25,12], [8,11], [13,11], [19,11],
                       [3,12],[24,12],[4,12],[23,12], [5,11], [22,11],
                       [6,10],[21,10],[7,11],[20,11],[9,11],
                       [18,11],[12,11],[14,11],[17,11],[10,11],
                       [11,11],[15,11],[16,11]
]

defense_wall_upgrade_priority =[
                               [0,13],[27,13],[1,12],[26,12],
                               [8,11],[13,11],[19,11],[6,10],[21,10],
                               [5,11],[22,11],[4,12],[23,12],
                               [7,11],[20,11],[4,12],[24,12],[2,12],
                               [25,12],[9,11],[18,11],[10,11],[17,11],
                               [11,11],[16,11],[12,11],[14,11],[15,11]
]

defense_secondary_wall_locations =[
                                  [4,10],[5,9],[6,9],[7,9],
                                  [22,10],[21,9],[20,9],[19,9]
]


defense_primary_turret_locations =[[2,11],[8,10],[19,10],[25,11],[13,10]]


defense_secondary_turret_locations = [[3,11],[24,11],[14,10],[9,10],[18,10]]

defense_tertiary_turret_locations = [[1,12],[26,12],[12,10],[15,10]]

defense_remaining_turret_locations =[
                                    [4,11],[23,11],[2,12],[25,12],[7,10],[20,10],
                                    [10,10],[17,10],[11,10],[16,10]
]

defense_build_order=[ [('turret','build'),defense_primary_turret_locations],
                      [('turret','upgrade'),defense_primary_turret_locations],
                      [('wall','build'),defense_wall_locations],
                      [('wall','upgrade'),defense_wall_upgrade_priority],
                      [('turret','build'),defense_secondary_turret_locations],
                      [('turret','upgrade'),defense_secondary_turret_locations],
                      [('wall','build'),defense_secondary_wall_locations],
                      [('wall','upgrade'),defense_secondary_wall_locations],
                      [('turret','build'),defense_tertiary_turret_locations],
                      [('turret','upgrade'),defense_tertiary_turret_locations],
                      [('turret','build'),defense_remaining_turret_locations],
                      [('turret','upgrade'),defense_remaining_turret_locations],
]


##################
### OFFENSE V2 ###
##################

offense_config_walls = [[14, 5], [14, 6], [14, 7], [14, 8], [14, 9], [14, 10], [14, 11], [14, 12]]

offense_config_supports = [[14, 4], [14, 3], [14, 2], [14, 1], [14, 0],
                            [13, 2], [11, 2], [11, 3], [12, 4],
                            [15, 1], [15, 2], [15, 3], [15, 4],
                            [16, 2], [16, 3]]

offense_config_walls_reversed = [[13, 5], [13, 6], [13, 7], [13, 8], [13, 9], [13, 10], [13, 11], [13, 12]]

offense_config_supports_reversed = [[13, 4], [13, 3], [13, 2], [13, 1], [13, 0],
                                    [14, 2], [16, 2], [16, 3], [15, 4],
                                    [12, 1], [12, 2], [12, 3], [12, 4],
                                    [11, 2], [11, 3]]

offense_build_order = [[('wall', 'build'), offense_config_walls],
                        [('support', 'build'), offense_config_supports],
                        [('support', 'upgrade'), offense_config_supports]]

offense_build_order_reversed = [[('wall', 'build'), offense_config_walls_reversed],
                                [('support', 'build'), offense_config_supports_reversed],
                                [('support', 'upgrade'), offense_config_supports_reversed]]

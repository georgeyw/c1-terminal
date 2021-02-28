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
                        [[('wall', 'build'), [[20, 12], [19, 11], [20, 10]]
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

# new offense strategy
def spawn_offense(game_state, attack_type = 'scout', side = 'left'):
    if side == 'right':
        location_1 = [18, 4]
        location_2 = [17, 3]
    else:
        location_1 = [9, 4]
        location_2 = [10, 3]

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

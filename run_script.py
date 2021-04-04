from fuzzy_asteroids.fuzzy_asteroids import AsteroidGame, FuzzyAsteroidGame

from controller import FuzzyController


if __name__ == "__main__":
    # Available settings
    settings = {
        # "graphics_on": True,
        # "sound_on": False,
        # "frequency": 60,
        "real_time_multiplier": 2,
        # "lives": 3,
        "prints": False,
        # "allow_key_presses": False
    }

    # Whether the users controller should be run
    run_with_controller = 1

    # Gene from first training session
    # gene = [[[-0.04271540380975858, -0.2166291541179315, -0.8827970872185638],
    #          [0.5806767382269792, 0.8953509991256308, 0.438211409494729],
    #          [728, 385, 27, 837, 963, 450, 687]], 38342.15483870968]
    # fitness = [4627.306182795699, 4627.306182795699, 30943.491803278688, 30943.491803278688,
    # 30943.491803278688, 30943.491803278688, 30943.491803278688, 30943.491803278688, 30943.491803278688,
    #            30943.491803278688, 30943.491803278688, 38342.15483870968, 38342.15483870968,
    #            38342.15483870968, 38342.15483870968, 38342.15483870968, 38342.15483870968, 38342.15483870968,
    #            38342.15483870968, 38342.15483870968, 38342.15483870968, 38342.15483870968, 38342.15483870968,
    #            38342.15483870968, 38342.15483870968, 38342.15483870968, 38342.15483870968,
    #            38342.15483870968, 38342.15483870968, 38342.15483870968, 38342.15483870968, 38342.15483870968,
    #            38342.15483870968, 38342.15483870968, 38342.15483870968, 38342.15483870968,
    #            38342.15483870968, 38342.15483870968, 38342.15483870968, 38342.15483870968, 38342.15483870968,
    #            38342.15483870968, 38342.15483870968, 38342.15483870968, 38342.15483870968,
    #            38342.15483870968, 38342.15483870968, 38342.15483870968, 38342.15483870968]

# Gene from 2nd training
#     gene = [[[-0.016246364446154682, -0.025565952540989922, -0.9539658434541948],
#             [0.4649000608588642, 0.5085767386066072, 0.2892988027420131],
#             [3, 0, 2, 0, 2, 3, 0, 1, 3, 0, 1, 2],
#             [0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1],
#             [-32, -165, -87, -160, -37, -58, -77],
#             [131, 102, 62, 21, 28, 127, 102]], 0]

# Gene from 3rd training
    gene = [[[-0.016246364446154682, -0.36285930195602933, -0.9702654976469424],
             [0.4649000608588642, 0.73135334195408, 0.7840761736391507],
             [0, 3, 1, 0, 2, 2, 1, 0, 0, 2, 1, 2],
             [0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
             [-32, -118, -29, -86, -114, -70, -29],
             [131, 138, 149, 79, 41, 59, 81]], 41.842592592592595]
    # Run with FuzzyController
    if run_with_controller:
        # Instantiate the environment
        game = FuzzyAsteroidGame(settings=settings)
        score = game.run(controller=FuzzyController(gene))
        print(score)

    else:
        # Run the Asteroids game with no
        game = AsteroidGame(settings=settings)
        game.run()
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
    gene = [[[-0.04271540380975858, -0.2166291541179315, -0.8827970872185638],
             [0.5806767382269792, 0.8953509991256308, 0.438211409494729],
             [728, 385, 27, 837, 963, 450, 687]], 38342.15483870968]
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

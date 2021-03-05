from fuzzy_asteroids.fuzzy_asteroids import TrainerEnvironment

from src.sample_controller import FuzzyController
from sample_score import SampleScore

if __name__ == "__main__":
    # Available settings
    settings = {
        # "frequency": 60,
        "lives": 3,
        "prints": False,
    }

    # To use the controller within the context of a training solution
    # It is important to not create a new instance of the environment everytime
    game = TrainerEnvironment(settings=settings)

    for i in range(10):
        # Call run() on an instance of the TrainerEnvironment
        # This function automatically manages cleanup
        score = game.run(controller=FuzzyController(), score=SampleScore())

        print(f"Generation {i}: {str(score)}")

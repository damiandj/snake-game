import random

from model.runer.runner import Runner, GUIRunner


class RandomRunner(Runner):

    def make_move(self):
        actions = [
                      self.game.snake.turn_north,
                      self.game.snake.turn_south,
                      self.game.snake.turn_west,
                      self.game.snake.turn_east,
                  ] + [None] * 50
        action = random.choice(actions)
        if action:
            action()


class RandomRunnerGUI(GUIRunner, RandomRunner):
    pass

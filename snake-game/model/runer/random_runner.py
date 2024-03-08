import random

import config
from model.game import SnakeGame


class RandomRunner:
    def __init__(self):
        self.game = SnakeGame(arena_size=config.arena_size)

    def make_move(self):
        actions = [
                      self.game.snake.turn_north,
                      self.game.snake.turn_south,
                      self.game.snake.turn_west,
                      self.game.snake.turn_east,
                  ] + [None] * 100
        action = random.choice(actions)
        if action:
            action()

    def run(self):
        self.game.initialize_game()
        i = 0
        while i < 1000:
            i += 1
            # if self._check_if_quit():
            #     self.game.history.save()
            #     break
            self.make_move()
            self.game.step()
        self.game.history.save()

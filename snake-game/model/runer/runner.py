import pygame

import config
from model.game import SnakeGame
from model.gui import GameGui


class Runner:
    def __init__(self):
        self.game = SnakeGame(arena_size=config.arena_size)

    def make_move(self):
        pass

    def action_when_die(self):
        self.game.history.save()
        # self.game.restart()

    def run(self, steps: int = 1000):
        self.game.initialize_game()

        for _ in range(steps):
            self.make_move()
            self.game.step()
            if self.game.death_condition():
                self.action_when_die()
                break
        self.game.history.save()


class GUIRunner(Runner):
    def __init__(self):
        super().__init__()
        self.gui = GameGui(game=self.game)

    def _bind_additional_keys(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.game.snake.speed_up()
        elif keys[pygame.K_s]:
            self.game.snake.speed_donw()
        elif keys[pygame.K_a]:
            self.game.snake.add_part()
        elif keys[pygame.K_r]:
            self.game.restart()

    def run(self, steps: int = 1000):
        self.gui.initialize()
        clock = pygame.time.Clock()
        self.game.initialize_game()
        while True:
            if self.gui.check_if_quit():
                self.game.history.save()
                break
            self.make_move()
            self.game.step()
            self.gui.draw_step(self.game.history[-1])
            self._bind_additional_keys()
            if self.game.death_condition():
                self.action_when_die()
                break
            clock.tick(60)
            pygame.display.update()

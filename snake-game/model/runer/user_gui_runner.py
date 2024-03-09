import pygame

from model.runer.runner import GUIRunner


class UserGuiRunner(GUIRunner):

    def make_move(self):
        """Bind keys to the snake's directions."""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.game.snake.turn_north()
        elif keys[pygame.K_DOWN]:
            self.game.snake.turn_south()
        elif keys[pygame.K_LEFT]:
            self.game.snake.turn_west()
        elif keys[pygame.K_RIGHT]:
            self.game.snake.turn_east()

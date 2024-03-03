import pygame

from model.game.game import SnakeGame
from model.gui.game_gui import GameGui


class UserGuiRunner(GameGui):
    """Represents the user GUI runner.

    Attributes:
        game (SnakeGame): The snake game.
    """

    def __init__(self):
        """Initialize the user GUI runner."""
        game = SnakeGame(arena_size=25)
        super().__init__(game)

    def _bind_keys(self):
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
        elif keys[pygame.K_v]:
            self.game.snake.speed_up()

    def run(self):
        """Run the game."""
        self.initialize()
        clock = pygame.time.Clock()
        self.game.initialize_game()
        while True:
            if self._check_if_quit():
                self.game.history.save()
                break
            self._bind_keys()
            self.game.step()
            self.draw_step(self.game.history[-1])
            clock.tick(60)
            pygame.display.update()

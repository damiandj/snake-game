import pygame

from config import screen_size, screen_color, arena_color, grid_line_color, title
from model.arena import Arena
from model.game.game import SnakeGame
from model.history.history import HistoryItem


class GameGui:
    """Represents the game GUI.

    Attributes:
        game (SnakeGame): The snake game.
        cell_size (int): The size of a cell in the game arena.
        screen (pygame.Surface): The game screen.
        game_area (pygame.Surface): The game area.
        font (pygame.font.Font): The font of the game.
    """

    def __init__(self, game: SnakeGame):
        """Initialize the game GUI.

        Args:
            game (SnakeGame): The snake game.
        """
        self.game = game

        self.cell_size = int(screen_size / self.game.arena_size)
        self.screen = None
        self.screen = None
        self.game_area = None
        self.font = None

    def initialize(self):
        """Initialize the game GUI."""
        pygame.init()
        pygame.display.set_caption(title)

        self.screen = pygame.display.set_mode((screen_size + 100, screen_size + 100))
        self.game_area = pygame.Surface((screen_size, screen_size))
        self.font = pygame.font.Font(None, 36)

    def _draw_actors(self, arena: Arena, surface: pygame.Surface):
        """Draw the actors in the game."""
        for item in arena.flat_arena:
            if item:
                pygame.draw.rect(
                    surface,
                    item.color,
                    (
                        item.position[0] * self.cell_size,
                        item.position[1] * self.cell_size,
                        self.cell_size,
                        self.cell_size,
                    ),
                )

    def _draw_grid(self, surface: pygame.Surface):
        """Draw the grid in the game."""
        for x in range(0, (self.game.arena_size + 1) * self.cell_size, self.cell_size):
            pygame.draw.line(
                surface,
                grid_line_color,
                (x, 0),
                (x, self.game.arena_size * self.cell_size),
            )
        for y in range(0, (self.game.arena_size + 1) * self.cell_size, self.cell_size):
            pygame.draw.line(
                surface,
                grid_line_color,
                (0, y),
                (self.game.arena_size * self.cell_size, y),
            )

    @staticmethod
    def check_if_quit():
        """Check if the game should quit."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return True
        return False

    def draw_step(self, game_stage: HistoryItem):
        """Draw a step in the game."""
        game_area = pygame.Surface((screen_size, screen_size))
        game_area.fill(arena_color)
        self.screen.fill(screen_color)
        self.game_area.fill(arena_color)

        self._draw_actors(arena=game_stage.arena, surface=game_area)
        self._draw_grid(surface=game_area)
        self.screen.blit(
            self.font.render(f"Score: {game_stage.score}", True, (0, 0, 0)),
            (10, 10),
        )
        self.screen.blit(game_area, (50, 50))

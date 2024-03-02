import random
import time
from dataclasses import dataclass
from typing import List

import pygame

from config import (
    grid_line_color,
    screen_size,
    screen_color,
    title,
    arena_color,
    save_dir,
)
from model.actor import Snake, Mouse, Devil


@dataclass(frozen=True)
class HistoryStep:
    """
    Represents a step in the game history.
    """

    snake_head: List[int]
    snake_tail: List[List[int]]
    mouse: List[int]
    devils: List[List[int]]
    score: int

    def __eq__(self, other):
        return (
                self.snake_head == other.snake_head
                and self.snake_tail == other.snake_tail
                and self.mouse == other.mouse
                and self.devils == other.devils
                and self.score == other.score
        )


class Game:
    """
    Represents the game.

    Attributes:
        arena_size (int): The size of the game arena.
        history (List): The history of the game.
        score (int): The score of the game.
        actors (List): The actors in the game.
        snake (Snake): The snake in the game.
        mouse (Mouse): The mouse in the game.
        devils (List): The devils in the game.
    """

    def __init__(self):
        """
        Initialize a Game object.
        """
        self.font = None
        self.screen = None
        self.arena_size = int(25)
        self.cell_size = int(screen_size / self.arena_size)

        self.history: List[HistoryStep] = []
        self.score = 0

        # Actors
        self.actors = []
        self.snake = None
        self.mouse = None
        self.devils = []

        # History
        self.history = []

    def _create_snake(self, init_size: int = 0):
        """
        Create a snake.

        Args:
            init_size (int): The initial size of the snake.
        """
        head_position = [int(self.arena_size / 2), int(self.arena_size / 2)]
        snake = Snake(
            position=head_position, arena_sizes=[self.arena_size, self.arena_size]
        )
        for _ in range(init_size):
            snake.add_part()

        self.snake = snake
        self.actors.extend(self.snake.body)

    def actors_step(self):
        """Make a step for all actors."""
        self.snake.step()

    def _bind_keys(self):
        """Bind keys to the snake's directions."""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.snake.turn_north()
        elif keys[pygame.K_DOWN]:
            self.snake.turn_south()
        elif keys[pygame.K_LEFT]:
            self.snake.turn_west()
        elif keys[pygame.K_RIGHT]:
            self.snake.turn_east()
        elif keys[pygame.K_v]:
            self.snake.speed_up()

    def _get_used_positions(self):
        """Get the used positions in the game."""
        return [actor.position for actor in self.actors]

    def _get_free_random_position(self):
        """Get a free random position in the game."""
        used_position = self._get_used_positions()
        while True:
            random_position = [
                random.randint(0, self.arena_size - 1),
                random.randint(0, self.arena_size - 1),
            ]
            if random_position not in used_position:
                return random_position

    def _create_mouse(self):
        """Create a mouse."""
        self.mouse = Mouse(self._get_free_random_position())
        self.actors.append(self.mouse)

    def _create_devil(self):
        """Create a devil."""
        devil_position = [
            random.randint(0, self.arena_size - 1),
            random.randint(0, self.arena_size - 1),
        ]
        self.devils.append(Devil(devil_position))
        self.actors.append(self.devils[-1])

    def eat_mouse(self):
        """Eat the mouse."""
        self.actors.remove(self.mouse)
        self.snake.add_part()
        self.actors.append(self.snake.body[-1])
        self._create_mouse()
        self.score += 1
        if not self.score % 2:
            self.snake.speed_up()

    def draw_grid(self, surface, cell_size):
        """Draw the grid on the surface."""
        for x in range(0, (self.arena_size + 1) * cell_size, cell_size):
            pygame.draw.line(
                surface, grid_line_color, (x, 0), (x, self.arena_size * cell_size)
            )
        for y in range(0, (self.arena_size + 1) * cell_size, cell_size):
            pygame.draw.line(
                surface, grid_line_color, (0, y), (self.arena_size * cell_size, y)
            )

    def draw_actors(self, surface, cell_size):
        """Draw the actors on the surface."""
        for actor in self.actors:
            _actor = pygame.Rect(
                cell_size * actor.position[0] + 1,
                cell_size * actor.position[1] + 1,
                cell_size,
                cell_size,
            )
            pygame.draw.rect(surface, actor.color, rect=_actor)

    def draw_score(self, surface):
        """Draw the score on the surface."""

    def restart(self):
        """Restart the game."""
        self.actors = []
        self.score = 0
        self._create_snake(init_size=0)
        self._create_mouse()
        self.devils = []
        self._create_devil()

    def _check_if_dead(self):
        """Check if the snake is dead."""
        for tail in self.snake.tail:
            if tail.position == self.snake.head.position:
                return True
        for devil in self.devils:
            if devil.position == self.snake.head.position:
                return True
        return False

    @staticmethod
    def _check_if_quit():
        """Check if the game should quit."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return True
        return False

    def initialize(self):
        """Initialize the game."""
        self._create_snake(init_size=0)
        self._create_mouse()
        self._create_devil()

    def game_step(self):
        """Make a step in the game."""
        if self._check_if_dead():
            # self._create_restart_banner()
            self.restart()
        self.actors_step()
        if self.snake.head.position == self.mouse.position:
            self.eat_mouse()

    def save_step_to_history(self):
        """Save the step to the history."""
        step = HistoryStep(
            snake_head=self.snake.head.position,
            snake_tail=[part.position for part in self.snake.tail],
            mouse=self.mouse.position,
            devils=[devil.position for devil in self.devils],
            score=self.score,
        )
        if self.snake.direction != [0, 0]:
            self.history.append(step)

    def load_step_from_history(self):
        """Load the step from the history."""
        step = self.history.pop(0)
        self.snake.head.position = step.snake_head
        if len(step.snake_tail) != len(self.snake.tail):
            self.snake.add_part()

        for part, position in zip(self.snake.tail, step.snake_tail):
            part.position = position

        self.mouse.position = step.mouse
        for devil, position in zip(self.devils, step.devils):
            devil.position = position
        self.score = step.score
        self.actors = [self.snake.head] + self.snake.tail + [self.mouse] + self.devils

    def save_history(self, filename: str):
        """Save the history to a file."""
        with open(save_dir / filename, "w") as file:
            file.write(str(self.history))

    def load_history(self, filename: str):
        """Load the history from a file."""
        with open(filename, "r") as file:
            self.history = eval(file.read())

    def run_from_history(self):
        """Run the game from the history."""
        pygame.init()
        pygame.display.set_caption(title)

        self.screen = pygame.display.set_mode((screen_size + 100, screen_size + 100))
        self.font = pygame.font.Font(None, 36)

        self.initialize()

        clock = pygame.time.Clock()
        while self.history:
            self.load_step_from_history()
            if self._check_if_quit():
                return

            self.screen.fill(screen_color)
            grid_surface = pygame.Surface((screen_size, screen_size))
            grid_surface.fill(arena_color)

            self.game_step()

            self.draw_actors(grid_surface, self.cell_size)
            self.draw_grid(grid_surface, self.cell_size)
            try:
                score_text = self.font.render(
                    f"Score: {self.score}, speed: {self.snake.speed}", 1, (0, 0, 0)
                )
                self.screen.blit(score_text, (10, 10))
                self.screen.blit(grid_surface, (50, 50))
            except pygame.error:
                pass

            clock.tick(60)
            pygame.display.update()
        # self._create_restart_banner()

    def _create_restart_banner(self):
        """Create a restart banner."""

        def _add_text(text, position):
            text = self.font.render(text, 1, (255, 255, 255))
            banner.blit(text, position)

        banner = pygame.Surface((screen_size, screen_size))
        banner.set_alpha(200)
        banner.fill((128, 128, 128))
        _add_text("You are dead! ", (100, 100))
        _add_text(f"Your score: {self.score}.", (100, 140))
        _add_text("Press enter to restart.", (100, 180))
        self.screen.blit(banner, (50, 50))
        pygame.display.update()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    self.save_history(f"{time.time()}_history.txt")
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.restart()
                        return

    def run(self):
        """Run the game."""
        pygame.init()
        pygame.display.set_caption(title)

        self.screen = pygame.display.set_mode((screen_size + 100, screen_size + 100))
        self.font = pygame.font.Font(None, 36)

        self.initialize()

        clock = pygame.time.Clock()
        while True:
            self.save_step_to_history()
            if self._check_if_quit():
                self.save_history(f"{time.time()}_history.txt")
                return

            self.screen.fill(screen_color)
            grid_surface = pygame.Surface((screen_size, screen_size))
            grid_surface.fill(arena_color)

            self._bind_keys()

            self.game_step()

            self.draw_actors(grid_surface, self.cell_size)
            self.draw_grid(grid_surface, self.cell_size)
            try:
                score_text = self.font.render(
                    f"Score: {self.score}, speed: {self.snake.speed}", 1, (0, 0, 0)
                )
                self.screen.blit(score_text, (10, 10))
                self.screen.blit(grid_surface, (50, 50))
            except pygame.error:
                pass

            clock.tick(60)
            pygame.display.update()

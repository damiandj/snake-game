import random

import pygame
from config import grid_line_color, screen_size, screen_color, title, arena_color
from model.actor import Snake, Mouse


class Game:
    def __init__(self):
        self.arena_size = int(25)

        self.history = []
        self.score = 0

        # Actors
        self.snake = self._create_snake(init_size=0)
        self.mouse = self._create_mouse()

    def _create_snake(self, init_size=0):
        head_position = [int(self.arena_size / 2), int(self.arena_size / 2)]
        # snake_head = SnakeHead(position=snake_position)
        snake = Snake(
            position=head_position, arena_sizes=[self.arena_size, self.arena_size]
        )
        for _ in range(init_size):
            snake.add_part()

        return snake

    def step(self):
        self.snake.step()

    def _bind_keys(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.snake.turn_up()
        elif keys[pygame.K_DOWN]:
            self.snake.turn_bottom()
        elif keys[pygame.K_LEFT]:
            self.snake.turn_left()
        elif keys[pygame.K_RIGHT]:
            self.snake.turn_right()
        elif keys[pygame.K_v]:
            self.snake.speed_up()

    def _create_mouse(self):
        mouse_position = [
            random.randint(0, self.arena_size - 1),
            random.randint(0, self.arena_size - 1),
        ]
        return Mouse(mouse_position)

    def eat_mouse(self):
        self.snake.add_part()
        self.mouse = self._create_mouse()
        self.score += 1
        if not self.score % 2:
            self.snake.speed_up()

    def draw_grid(self, surface, cell_size):
        for x in range(0, (self.arena_size + 1) * cell_size, cell_size):
            pygame.draw.line(
                surface, grid_line_color, (x, 0), (x, self.arena_size * cell_size)
            )
        for y in range(0, (self.arena_size + 1) * cell_size, cell_size):
            pygame.draw.line(
                surface, grid_line_color, (0, y), (self.arena_size * cell_size, y)
            )

    def draw_actors(self, surface, cell_size):
        for actor in [self.mouse] + self.snake.body:
            _actor = pygame.Rect(
                cell_size * actor.position[0] + 1,
                cell_size * actor.position[1] + 1,
                cell_size,
                cell_size,
            )
            pygame.draw.rect(surface, actor.color, rect=_actor)

    def draw_score(self, surface, font):
        score_text = font.render(
            f"Score: {self.score}, speed: {self.snake.speed}", 1, (0, 0, 0)
        )
        surface.blit(score_text, (10, 10))

    def restart(self):
        self.score = 0
        self.snake = self._create_snake(init_size=0)
        self.mouse = self._create_mouse()

    def _check_if_dead(self):
        for tail in self.snake.body[1:]:
            if tail.position == self.snake.head.position:
                return True
        return False

    @staticmethod
    def _check_if_quit():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
        return False

    def run(self):

        pygame.init()

        screen = pygame.display.set_mode((screen_size + 100, screen_size + 100))
        pygame.display.set_caption(title)

        font = pygame.font.Font(None, 36)
        clock = pygame.time.Clock()
        cell_size = int(screen_size / self.arena_size)
        running = True

        while running:
            if self._check_if_quit():
                running = False

            screen.fill(screen_color)
            grid_surface = pygame.Surface((screen_size, screen_size))
            grid_surface.fill(arena_color)

            self._bind_keys()

            if self._check_if_dead():
                self.restart()

            self.step()

            if self.snake.head.position == self.mouse.position:
                self.eat_mouse()

            self.draw_actors(grid_surface, cell_size)
            self.draw_grid(grid_surface, cell_size)
            self.draw_score(screen, font)

            screen.blit(grid_surface, (50, 50))

            clock.tick(60)
            pygame.display.update()

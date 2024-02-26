import random

import pygame
from model.actor import SnakeHead, Snake, Mouse, SnakeBody
from model.arena import Arena


class Game:
    def __init__(self):
        self.arena_size = int(25)
        self.arena = Arena(size=self.arena_size)
        self.snake = self._create_snake(init_size=0)
        self.mouse = None
        self.snake_speed = 2 / 20
        self._step = 0
        self.history = []
        self.score = 0

    def _create_snake(self, init_size=0):
        snake_position = [int(self.arena_size / 2), int(self.arena_size / 2)]
        snake_head = SnakeHead(position=snake_position)
        snake = Snake(head=snake_head, arena_sizes=[self.arena_size, self.arena_size])
        for _ in range(init_size):
            snake.add_part()

        return snake

    def step(self):
        self.history.append(self.arena)
        self.arena = Arena(size=self.arena_size)
        self._step += 1
        if int(self._step * self.snake_speed) == self._step * self.snake_speed:
            self.snake.step()
        for part in self.snake.body:
            self.arena.add_snake_part(snake_part=part)

        if self.mouse:
            self.arena.add_mouse(self.mouse)

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

    def _add_mouse(self):
        mouse_position = [
            random.randint(0, self.arena_size - 1),
            random.randint(0, self.arena_size - 1),
        ]
        self.mouse = Mouse(mouse_position)

    def _del_mouse(self):
        self.mouse = None

    def _speed_up(self):
        if self.snake_speed == 1 / 20:
            self.snake_speed = 2 / 20
        elif self.snake_speed == 2 / 20:
            self.snake_speed = 4 / 20
        elif self.snake_speed == 4 / 20:
            self.snake_speed = 5 / 20
        elif self.snake_speed == 5 / 20:
            self.snake_speed = 10 / 20

    def run(self):
        pygame.init()

        clock = pygame.time.Clock()
        screen_size = 640
        cell_size = int(screen_size / self.arena_size)
        line_color = "grey64"
        font = pygame.font.Font(None, 36)

        def draw_grid(surface):
            for x in range(0, (self.arena_size + 1) * cell_size, cell_size):
                pygame.draw.line(
                    surface, line_color, (x, 0), (x, self.arena_size * cell_size)
                )
            for y in range(0, (self.arena_size + 1) * cell_size, cell_size):
                pygame.draw.line(
                    surface, line_color, (0, y), (self.arena_size * cell_size, y)
                )

        screen = pygame.display.set_mode((screen_size + 100, screen_size + 100))

        pygame.display.set_caption("Pygame Snake")

        running = True
        self._add_mouse()
        while running:
            screen.fill((255, 255, 255))
            for tail in self.snake.body[1:]:
                if tail.position == self.snake.head.position:
                    self.score = 0
                    self.snake_speed = 2 / 20
                    self.snake = self._create_snake(init_size=0)

            self.step()
            self._bind_keys()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            grid_surface = pygame.Surface((screen_size, screen_size))
            grid_surface.fill((255, 255, 255))  # Fill screen with white color

            if self.snake.head.position == self.mouse.position:
                self.snake.add_part()
                self._del_mouse()
                self._add_mouse()
                self.score += 1
                if not self.score % 10:
                    self._speed_up()

            for line_no in range(self.arena_size):
                for row_no in range(self.arena_size):
                    item = self.arena.arena[line_no][row_no]
                    if isinstance(item, SnakeHead) or isinstance(item, SnakeBody):
                        _item = pygame.Rect(
                            cell_size * line_no + 1,
                            cell_size * row_no + 1,
                            cell_size,
                            cell_size,
                        )
                        pygame.draw.rect(grid_surface, item.color, rect=_item)

                    if isinstance(item, Mouse):
                        _item = pygame.Rect(
                            cell_size * line_no + 1,
                            cell_size * row_no + 1,
                            cell_size,
                            cell_size,
                        )
                        pygame.draw.rect(grid_surface, item.color, rect=_item)

            draw_grid(grid_surface)

            score_text = font.render(
                f"Score: {self.score}, speed: {self.snake_speed}", 1, (0, 0, 0)
            )
            screen.blit(score_text, (10, 10))
            screen.blit(grid_surface, (50, 50))

            clock.tick(60)  # limits FPS to 6
            pygame.display.update()

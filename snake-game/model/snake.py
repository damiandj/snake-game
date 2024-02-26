# Example file showing a basic pygame "game loop"
import random

import pygame

from actor import SnakeHead, SnakeBody, Mouse, DirectionChangePoint


class Snake:
    def __init__(self):
        self.arena_size = 500
        self.resolution = (self.arena_size, self.arena_size)

        self.clock = pygame.time.Clock()

        self.snake_body = self._generate_snake()
        self.score = 0
        self.mouse = None

        self.change_direction_points = {}

    def _generate_snake(self):
        head = SnakeHead(
            position=list(map(int, (self.arena_size / 2, self.arena_size / 2))),
            size=[10, 10],
            arena_size=[self.arena_size, self.arena_size],
        )
        snake_body = SnakeBody(head=head)

        return snake_body

    def _generate_mouse(self):
        mouse = Mouse(
            position=[
                random.randint(1, self.arena_size - 1),
                random.randint(1, self.arena_size - 1),
            ],
            size=[10, 10],
            arena_size=[self.arena_size, self.arena_size],
        )
        self.mouse = mouse

    def _delete_mouse(self):
        self.mouse = None

    def _move_up(self):
        if self.snake_body.head.direction[0] != 0:
            self.snake_body.head.direction = [0, -1]
            p = DirectionChangePoint(
                center=self.snake_body.head.center,
                size=[1, 1],
                arena_size=[self.arena_size, self.arena_size],
            )
            p.direction = self.snake_body.head.direction
            for item in self.snake_body.tail:
                self.change_direction_points[item].append(p)

    def _move_down(self):
        if self.snake_body.head.direction[0] != 0:
            self.snake_body.head.direction = [0, 1]
            p = DirectionChangePoint(
                center=self.snake_body.head.center,
                size=[1, 1],
                arena_size=[self.arena_size, self.arena_size],
            )
            p.direction = self.snake_body.head.direction
            for item in self.snake_body.tail:
                self.change_direction_points[item].append(p)

    def _move_left(self):
        if self.snake_body.head.direction[1] != 0:
            self.snake_body.head.direction = [-1, 0]
            p = DirectionChangePoint(
                center=self.snake_body.head.center,
                size=[1, 1],
                arena_size=[self.arena_size, self.arena_size],
            )
            p.direction = self.snake_body.head.direction
            for item in self.snake_body.tail:
                self.change_direction_points[item].append(p)

    def _move_right(self):
        if self.snake_body.head.direction[1] != 0:
            self.snake_body.head.direction = [1, 0]
            p = DirectionChangePoint(
                center=self.snake_body.head.center,
                size=[1, 1],
                arena_size=[self.arena_size, self.arena_size],
            )
            p.direction = self.snake_body.head.direction
            for item in self.snake_body.tail:
                self.change_direction_points[item].append(p)

    def _bind_keys(self):
        keys = pygame.key.get_pressed()
        key_at_once = sum([int(k) for k in keys])
        if key_at_once > 1:
            return
        if keys[pygame.K_UP]:
            self._move_up()
        if keys[pygame.K_DOWN]:
            self._move_down()
        if keys[pygame.K_LEFT]:
            self._move_left()
        if keys[pygame.K_RIGHT]:
            self._move_right()

    def _add_piece(self):
        self.snake_body.add_piece()
        self.change_direction_points[self.snake_body.tail[-1]] = []
        for _, points in self.change_direction_points.items():
            for p in points:
                if p not in self.change_direction_points[self.snake_body.tail[-1]]:
                    self.change_direction_points[self.snake_body.tail[-1]].append(p)

    def run(self):
        pygame.init()
        self._add_piece()
        self._add_piece()
        self._add_piece()
        self._add_piece()
        self._add_piece()
        screen = pygame.display.set_mode((self.resolution[0], self.resolution[1] + 100))

        start_time = pygame.time.get_ticks()

        running = True
        self.snake_body.speed_up()
        self.snake_body.speed_up()
        # self.snake_body.speed_up()
        # self.snake_body.speed_up()

        self._generate_mouse()

        while running:
            screen.fill("blue")
            self._bind_keys()

            for tail_part in self.snake_body.tail:
                for change_direction_point in self.change_direction_points[tail_part]:
                    if change_direction_point.intersect(tail_part, epsilon=0.01):
                        tail_part.direction = change_direction_point.direction
                        self.change_direction_points[tail_part].remove(
                            change_direction_point
                        )

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # fill the screen with a color to wipe away anything from last frame
            self.snake_body.head.step()
            for piece in self.snake_body.tail:
                piece.step()
            canvas = pygame.Surface(self.resolution)
            canvas.fill("white")
            head = pygame.Rect(
                self.snake_body.head.left,
                self.snake_body.head.top,
                self.snake_body.head.size[0],
                self.snake_body.head.size[1],
            )
            pygame.draw.rect(canvas, self.snake_body.head.color, rect=head)
            for piece in self.snake_body.tail:
                _piece = pygame.Rect(
                    piece.left,
                    piece.top,
                    piece.size[0],
                    piece.size[1],
                )
                pygame.draw.rect(canvas, piece.color, rect=_piece)
            if self.mouse:
                mouse = pygame.Rect(
                    self.mouse.left,
                    self.mouse.top,
                    self.mouse.size[0],
                    self.mouse.size[1],
                )
                pygame.draw.rect(canvas, self.mouse.color, rect=mouse)
                if self.mouse.intersect(self.snake_body.head):
                    self.score += 1
                    self._delete_mouse()
                    self._generate_mouse()
                    self._add_piece()
                    # if not self.score % 2:
                    #     self.snake_body.speed_up()

            font = pygame.font.Font(None, 36)
            score_text = font.render(f"Score: {self.score}", 1, (255, 255, 255))
            screen.blit(score_text, (100, 10))

            current_time = pygame.time.get_ticks()
            time_elapsed = (current_time - start_time) / 1000.0

            time_text = font.render(
                f"Time: {round(time_elapsed, 2)}", 1, (255, 255, 255)
            )
            screen.blit(time_text, (100, 50))

            screen.blit(canvas, dest=(0, 100))
            pygame.display.update()
            self.clock.tick(60)  # limits FPS to 60

        pygame.quit()


asd = Snake()
asd.run()

import copy
import random
from typing import Union, Type, List, Optional

from model.actor import Snake, Mouse, Devil
from model.arena import Arena
from model.history import HistoryItem, GameHistory


class SnakeGame:
    """Represents a snake game.

    Attributes:
        arena_size (int): The size of the game arena.
        score (int): The score of the game.
        snake (Snake): The snake in the game.
        mouse (Mouse): The mouse in the game.
        arena (Arena): The game arena.
        devils (List[Devil]): The devils in the game.
        history (model.history.history.GameHistory): The history of the game.
    """

    def __init__(self, arena_size: int = 25):
        self.arena_size = arena_size
        self.score = 0
        self.snake = None
        self.mouse = None
        self.arena = None
        self.devils = []
        self.history = GameHistory()

    def initialize_game(self):
        """Initialize the game."""
        self.mouse = self._create_mouse()
        self.snake = self._create_snake()
        self.devils.append(self._create_devil())

    def _create_arena(self) -> Arena:
        """Create the game arena."""
        arena = Arena(size=self.arena_size)
        arena.add_snake(copy.deepcopy(self.snake))
        arena.add_mouse(copy.deepcopy(self.mouse))
        for devil in self.devils:
            arena.add_devil(copy.deepcopy(devil))

        return arena

    def _create_snake(self) -> Snake:
        """Create the snake in the middle of arena."""
        return Snake(
            position=[self.arena_size // 2, self.arena_size // 2],
            arena_sizes=[self.arena_size, self.arena_size],
        )

    def get_used_positions(self) -> List[List[int]]:
        """Get the used positions in the game."""
        used_positions = []
        if self.snake:
            used_positions.extend([part.position for part in self.snake.body])
        if self.mouse:
            used_positions.append(self.mouse.position)
        for devil in self.devils:
            used_positions.append(devil.position)
        return used_positions

    def get_deadly_positions(self) -> List[List[int]]:
        """Get the deadly positions in the game."""
        deadly_positions = [a.position for a in self.snake.tail + self.devils]

        return deadly_positions

    def _create_actor_on_random_position(
            self, actor_cls: Union[Type[Devil], Type[Mouse]]
    ) -> Optional[Union[Devil, Mouse]]:
        """Create an actor on a random position."""
        for _ in range(self.arena_size ** 2):
            actor = actor_cls(
                position=[
                    random.randint(0, self.arena_size - 1),
                    random.randint(0, self.arena_size - 1),
                ]
            )
            if actor.position not in self.get_used_positions():
                return actor

        return None

    def _create_mouse(self) -> Optional[Mouse]:
        """Create the mouse on a random position."""
        return self._create_actor_on_random_position(Mouse)

    def _create_devil(self) -> Optional[Devil]:
        """Create the devil on a random position."""
        return self._create_actor_on_random_position(Devil)

    def snake_eat_mouse(self):
        """The snake eats the mouse."""
        self.snake.add_part()
        self.score += 1
        if self.score % 5 == 0:
            self.devils.append(self._create_devil())
            self.snake.speed_up()

    def restart(self):
        """Restart the game."""
        self.snake = None
        self.mouse = None
        self.devils = []
        self.score = 0
        self.history = GameHistory()
        self.initialize_game()

    def death_condition(self):
        return self.snake.head.position in self.get_deadly_positions()

    def step(self):
        """Advance the game by one step."""
        self.snake.step()
        for devil in self.devils:
            devil.step()
        self.mouse.step()

        if self.snake.head.position == self.mouse.position:
            self.snake_eat_mouse()
            self.mouse = self._create_mouse()

        # if self.snake.head.position in self.get_deadly_positions():
        #     self.history.save()
        #     self.restart()

        self.arena = self._create_arena()
        self.history.add_to_history(HistoryItem(arena=self.arena, score=self.score))

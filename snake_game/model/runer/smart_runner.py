from typing import Tuple, List

from snake_game.model.runer.runner import Runner, GUIRunner
from snake_game.model.utils.find_path import find_path_with_omission


class SmartRunner(Runner):

    def make_move(self):
        """
        Method to make a move in the game.
        """
        start = (self.game.snake.head.position[0], self.game.snake.head.position[1])
        goal = (self.game.mouse.position[0], self.game.mouse.position[1])

        path = find_path_with_omission(
            size=(self.game.arena_size, self.game.arena_size),
            start=start,
            goal=goal,
            omitted_points=[
                (a.position[0], a.position[1])
                for a in self.game.snake.tail + self.game.devils
            ],
        )
        if path:
            self._follow_the_path(path, start)
        else:
            if (
                self.game.snake.get_new_head_position()
                not in self.game.get_deadly_positions()
            ):
                pass
            else:
                self._survive()

    def _survive(self) -> None:
        """
        Method to handle survival when a path is not found.
        """
        head_pos = self.game.snake.head.position
        deadly_positions = self.game.get_deadly_positions()

        if self.game.snake.direction[0]:
            if [
                head_pos[0],
                (head_pos[1] + 1) % self.game.arena_size,
            ] not in deadly_positions:
                self.game.snake.turn_south()
            elif [
                head_pos[0],
                (head_pos[1] - 1) % self.game.arena_size,
            ] not in deadly_positions:
                self.game.snake.turn_north()
        else:
            if [
                (head_pos[0] + 1) % self.game.arena_size,
                head_pos[1],
            ] not in deadly_positions:
                self.game.snake.turn_east()
            elif [
                (head_pos[0] - 1) % self.game.arena_size,
                head_pos[1],
            ] not in deadly_positions:
                self.game.snake.turn_west()

    def _follow_the_path(
        self, path: List[Tuple[int, int]], snake_head_position: Tuple[int, int]
    ) -> None:
        """
        Method to follow the calculated path.

        Args:
            path (List[Tuple[int, int]]): The path to follow.
            snake_head_position (Tuple[int, int]): Position of the snake's head.
        """
        next_step = path[1]
        if next_step == (
            (snake_head_position[0] + 1) % self.game.arena_size,
            snake_head_position[1],
        ):
            self.game.snake.turn_east()
        elif next_step == (
            (snake_head_position[0] - 1) % self.game.arena_size,
            snake_head_position[1],
        ):
            self.game.snake.turn_west()
        elif next_step == (
            snake_head_position[0],
            (snake_head_position[1] + 1) % self.game.arena_size,
        ):
            self.game.snake.turn_south()
        elif next_step == (
            snake_head_position[0],
            (snake_head_position[1] - 1) % self.game.arena_size,
        ):
            self.game.snake.turn_north()


class SmartRunnerGUI(GUIRunner, SmartRunner):
    pass

import unittest
import unittest.mock
from typing import List

from parameterized import parameterized

from model.actor.snake import Snake


class TestSnake(unittest.TestCase):
    def setUp(self):
        self.arena_size = [10, 20]
        self.snake = Snake(position=[1, 2], arena_sizes=self.arena_size)

    def test_speed_up(self):
        self.snake._reset_steps_to_move = unittest.mock.MagicMock()
        self.snake.speed = 1
        self.snake.speed_up()
        self.assertEqual(self.snake.speed, 2)
        self.snake._reset_steps_to_move.assert_called_once()

    @parameterized.expand(
        [([1, 0], [0, 2]), ([-1, 0], [2, 2]), ([0, 1], [1, 1]), ([0, -1], [1, 3])]
    )
    def test_add_part(self, prev_direction: List[int], exp_position: List[int]):
        self.snake.head.position = [1, 2]
        self.snake.direction = prev_direction
        self.snake.add_part()
        self.assertEqual(len(self.snake.tail), 1)
        self.assertEqual(self.snake.tail[-1].position, exp_position)

    def test_add_part_out_of_arena(self):
        self.snake.arena_sizes = [3, 3]
        self.snake.head.position = [0, 0]
        self.snake.direction = [1, 0]
        self.snake.add_part()
        self.assertEqual(self.snake.tail[-1].position, [2, 0])
        self.snake.tail[-1].direction = [0, 1]
        self.snake.add_part()
        self.assertEqual(self.snake.tail[-1].position, [2, 2])

    def test_make_step(self):
        self.snake.head.position = [1, 2]
        self.snake.direction = [0, 1]
        self.snake.add_part()
        self.snake.add_part()
        self.snake.make_step()
        self.assertEqual(self.snake.head.position, [1, 3])
        self.assertEqual(self.snake.tail[-2].position, [1, 2])
        self.assertEqual(self.snake.tail[-1].position, [1, 1])

    def test_make_step_out_of_arena(self):
        self.snake.head.position = [0, 0]
        self.snake.direction = [-1, 0]
        self.snake.add_part()
        self.snake.add_part()
        self.snake.make_step()
        self.assertEqual(self.snake.head.position, [9, 0])
        self.assertEqual(self.snake.tail[-2].position, [0, 0])
        self.assertEqual(self.snake.tail[-1].position, [1, 0])

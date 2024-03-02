import unittest
import unittest.mock
from typing import List

from parameterized import parameterized

from model.actor import Actor, Snake


class TestActor(unittest.TestCase):
    def setUp(self):
        self.actor = Actor(position=[1, 2])

    def test_step(self):
        self.assertEqual(self.actor.step_to_move, 10)
        self.actor.step()
        self.assertEqual(self.actor.step_to_move, 9)

    def test__reset_steps_to_move(self):
        self.actor.step()
        self.actor._reset_steps_to_move()
        self.assertEqual(self.actor.step_to_move, 10)

    @parameterized.expand(
        [([1, 0], [0, -1]), ([-1, 0], [0, -1]), ([0, 1], [0, 1]), ([0, -1], [0, -1])]
    )
    def test_turn_north(self, cur_direction: List[int], exp_direction: List[int]):
        self.actor.direction = cur_direction
        self.actor.turn_north()
        self.assertEqual(self.actor.direction, exp_direction)

    @parameterized.expand(
        [([1, 0], [0, 1]), ([-1, 0], [0, 1]), ([0, -1], [0, -1]), ([0, 1], [0, 1])]
    )
    def test_turn_south(self, cur_direction: List[int], exp_direction: List[int]):
        self.actor.direction = cur_direction
        self.actor.turn_south()
        self.assertEqual(self.actor.direction, exp_direction)

    @parameterized.expand(
        [([0, 1], [-1, 0]), ([0, -1], [-1, 0]), ([1, 0], [1, 0]), ([-1, 0], [-1, 0])]
    )
    def test_turn_west(self, cur_direction: List[int], exp_direction: List[int]):
        self.actor.direction = cur_direction
        self.actor.turn_west()
        self.assertEqual(self.actor.direction, exp_direction)

    @parameterized.expand(
        [([0, 1], [1, 0]), ([0, -1], [1, 0]), ([1, 0], [1, 0]), ([-1, 0], [-1, 0])]
    )
    def test_turn_east(self, cur_direction: List[int], exp_direction: List[int]):
        self.actor.direction = cur_direction
        self.actor.turn_east()
        self.assertEqual(self.actor.direction, exp_direction)

    @parameterized.expand(
        [([0, 1], [0, -1]), ([0, -1], [0, 1]), ([1, 0], [-1, 0]), ([-1, 0], [1, 0])]
    )
    def test_turn_back(self, cur_direction: List[int], exp_direction: List[int]):
        self.actor.direction = cur_direction
        self.actor.turn_back()
        self.assertEqual(self.actor.direction, exp_direction)


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

import unittest.mock
from typing import List

from parameterized import parameterized

from model.actor.actor import Actor


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

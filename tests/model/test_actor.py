import unittest

from model.actor import Actor


class TestActor(unittest.TestCase):
    def setUp(self):
        self.actor = Actor(position=[1, 2])

    def test_step(self):
        self.assertEqual(self.actor.step_to_move, 10)
        self.actor.step()
        self.assertEqual(self.actor.step_to_move, 9)

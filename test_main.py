import requests
import unittest
import parser


class TestMain(unittest.TestCase):

    def test_experience(self):
        self.assertEqual(parser.input_yoe(1), "beginner")
        self.assertEqual(parser.input_yoe(20), "expert")

    def test_goal(self):
        correct = ("bodybuilding", "strength")
        self.assertEqual(parser.input_goal(3), correct)

    def test_diet(self):
        correct = ("low-carb", "findByNutrients?minCarbs=15&maxCarbs=35")
        self.assertEqual(parser.input_diet(2), correct)

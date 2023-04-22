import unittest
from dataclasses import dataclass

from middleware.types.JsonCoding import EnhancedJSONEncoder


@dataclass
class Person:
    name: str
    age: int


class TestEnhancedJSONEncoder(unittest.TestCase):
    def setUp(self):
        self.encoder = EnhancedJSONEncoder()

    def test_encode_dataclass(self):
        person = Person("Alice", 25)
        expected_result = '{"name": "Alice", "age": 25}'
        self.assertEqual(self.encoder.encode(person), expected_result)

    def test_encode_non_dataclass(self):
        obj = {"foo": "bar"}
        expected_result = '{"foo": "bar"}'
        self.assertEqual(self.encoder.encode(obj), expected_result)

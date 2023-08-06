import unittest
from degreesConversion.src.degreesConversion.converter import *


class TestMain(unittest.TestCase):
    def setUp(self) -> None:
        self.conv = Converter()
        self.error = "Couldn't convert string to float."

    def test_celFah(self):
        self.assertEqual(self.conv.celFah(0), 32.0)
        self.assertEqual(self.conv.celFah(15.2), 59.36)
        self.assertEqual(self.conv.celFah("0"), 32.0)
        self.assertEqual(self.conv.celFah("a"), self.error)

    def test_fahCel(self):
        self.assertEqual(self.conv.fahCel(0), -17.78)
        self.assertEqual(self.conv.fahCel("0"), -17.78)
        self.assertEqual(self.conv.fahCel(100), 37.78)
        self.assertEqual(self.conv.fahCel("a"), self.error)

    def test_celKel(self):
        self.assertEqual(self.conv.celKel(0), 273.15)
        self.assertEqual(self.conv.celKel("0"), 273.15)
        self.assertEqual(self.conv.celKel(100), 373.15)
        self.assertEqual(self.conv.celKel("a"), self.error)

    def test_kelCel(self):
        self.assertEqual(self.conv.kelCel(0), -273.15)
        self.assertEqual(self.conv.kelCel("0"), -273.15)
        self.assertEqual(self.conv.kelCel(100), -173.15)
        self.assertEqual(self.conv.kelCel("a"), self.error)

    def test_fahKel(self):
        self.assertEqual(self.conv.fahKel(0), 255.37)
        self.assertEqual(self.conv.fahKel("0"), 255.37)
        self.assertEqual(self.conv.fahKel(100), 310.93)
        self.assertEqual(self.conv.fahKel("a"), self.error)

    def test_kelFah(self):
        self.assertEqual(self.conv.kelFah(0), -459.67)
        self.assertEqual(self.conv.kelFah("0"), -459.67)
        self.assertEqual(self.conv.kelFah(100), -279.67)
        self.assertEqual(self.conv.kelFah("a"), self.error)


if __name__ == "__main__":
    unittest.main()

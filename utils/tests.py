# -*- coding: utf-8 -*-
import unittest
from utils import moeda

class TestUtilTest(unittest.TestCase):
    def testMoney3Digitos(self):
        self.assertEqual(moeda(1.99), 'R$ 1,99')

    def testMoney4Digitos(self):
        self.assertEqual(moeda(10.51), 'R$ 10,51')

    def testMoney5Digitos(self):
        self.assertEqual(moeda(131.01), 'R$ 131,01')

    def testMoney6Digitos(self):
        self.assertEqual(moeda(1280.50), 'R$ 1.280,5')

    def testMoney7Digitos(self):
        self.assertEqual(moeda(10345.75), 'R$ 10.345,75')


if __name__ == '__main__':
    unittest.main()

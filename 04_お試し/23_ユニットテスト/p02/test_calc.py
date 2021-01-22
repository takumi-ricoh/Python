# -*- coding: utf-8 -*-
"""
Created on Wed Jun  3 15:29:45 2020

@author: p000495138
"""

import unittest
import calc

class Test_GetCalc(unittest.TestCase):
    def setUp(self):
        print("setup")
        self.gc = calc.GetCalc([1,2,3,4])
        
    def test_get_sum(self):
        expected = 10
        actual = self.gc.get_sum()
        self.assertEqual(expected, actual)

    def test_data(self):
        expected = [1,2,3,4]
        actual = self.gc.data
        self.assertEqual(expected, actual)

    def test_data_almost(self):
        expected = [1,2,3,4.0000000000000000001]
        actual = self.gc.data
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
    
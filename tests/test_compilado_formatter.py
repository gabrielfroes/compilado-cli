import sys, os
sys.path.insert(0, './src')
import unittest
from datetime import date
from compilado_formatter import CompiladoFormatter

class TestCompiladoFormatter(unittest.TestCase):
    
    def setUp(self):
        self.formatter = CompiladoFormatter()

    def test_episode(self):
        self.assertEqual(self.formatter.episode(1), '#001')
        self.assertEqual(self.formatter.episode(100), '#100')
        self.assertEqual(self.formatter.episode(99), '#099')
        self.assertEqual(self.formatter.episode(1000), '#1000')

    def test_period(self):
        period_start = date(2021, 7, 17)
        period_end = date(2021, 7, 23)
        self.assertEqual(self.formatter.period(period_start, period_end), '17/07 a 23/07')

if __name__ == '__main__':
    unittest.main()
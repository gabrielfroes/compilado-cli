import sys, os
sys.path.insert(0, './src')
import unittest
from compilado_feed import CompiladoFeed
from datetime import datetime, date

class TestCompiladoFeed(unittest.TestCase):

    def setUp(self):
        self.feed_path = os.path.abspath("./tests/resources/anchor-feed.xml")
        self.compilado_feed = CompiladoFeed(self.feed_path)

    def test_period_episode(self):
        post_date = date(2021, 7, 17)
        period_date = {"start": date(2021, 7, 10), "end": date(2021, 7, 16)}
        self.assertEqual(self.compilado_feed.period_episode(post_date), period_date)

    def test_current_episode(self):
        current_episode = {"id": 17, "post_date": date(2021, 7, 17), "period": {"start": date(2021, 7, 10), "end": date(2021, 7, 16)} }
        self.assertEqual(self.compilado_feed.current_episode(), current_episode)

    def test_next_episode(self):
        next_episode = {"id": 18, "post_date": date(2021, 7, 24), "period": {"start": date(2021, 7, 17), "end": date(2021, 7, 23)}}
        self.assertEqual(self.compilado_feed.next_episode(), next_episode)

if __name__ == '__main__':
    unittest.main()
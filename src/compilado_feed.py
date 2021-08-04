import feedparser
from datetime import datetime, timedelta, time

class CompiladoFeed():
    EPISODE_INTERVAL_IN_DAYS = 7
    EPISODE_TOTAL_PERIOD_IN_DAYS = 6

    def __init__(self, feed_url):
        self.feed = feedparser.parse(feed_url)

    def period_episode(self, post_date):
        return {
            'start': post_date - timedelta(days=self.EPISODE_INTERVAL_IN_DAYS),
            'end': post_date - timedelta(days=self.EPISODE_INTERVAL_IN_DAYS-self.EPISODE_TOTAL_PERIOD_IN_DAYS)
        }

    def current_episode(self):
        last_entry = self.feed.entries[0]
        if last_entry == None:
            return False

        current_episode = {}
        current_episode["id"] = int(last_entry["itunes_episode"])
        current_episode["post_date"] = datetime.strptime(last_entry["published"], "%a, %d %b %Y %H:%M:%S %Z").date()
        current_episode["period"] = self.period_episode(current_episode["post_date"])

        return current_episode

    def next_episode(self):
        current_episode = self.current_episode()
        
        if current_episode == False:
            return False

        next_episode = {}
        next_episode["id"] = current_episode["id"] + 1
        next_episode["post_date"] = current_episode["post_date"] + timedelta(days=self.EPISODE_INTERVAL_IN_DAYS)
        next_episode["period"] = self.period_episode(next_episode["post_date"])

        return next_episode
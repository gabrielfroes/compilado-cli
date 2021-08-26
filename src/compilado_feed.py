import feedparser
from datetime import datetime, timedelta, time
import logging

class CompiladoFeed():
    EPISODE_INTERVAL_IN_DAYS = 7
    EPISODE_TOTAL_PERIOD_IN_DAYS = 6

    def __init__(self, feed_url):
        self.feed = feedparser.parse(feed_url)
        self.log = logging.getLogger(__name__)

    def period_episode(self, post_date):
        episode_period = {
            'start': post_date - timedelta(days=self.EPISODE_INTERVAL_IN_DAYS),
            'end': post_date - timedelta(days=self.EPISODE_INTERVAL_IN_DAYS-self.EPISODE_TOTAL_PERIOD_IN_DAYS)
        }
        self.log.debug ("Period episode: {0}".format(episode_period))
        return episode_period

    def current_episode(self):
        last_entry = self.feed.entries[0]
        if last_entry == None:
            self.log.error ("Current episode is not found on feed")
            return False

        current_episode = {}
        current_episode["id"] = int(last_entry["itunes_episode"])
        current_episode["post_date"] = datetime.strptime(last_entry["published"], "%a, %d %b %Y %H:%M:%S %Z").date()
        current_episode["period"] = self.period_episode(current_episode["post_date"])

        self.log.debug ("Current episode: {0}".format(current_episode))
        return current_episode

    def next_episode(self):
        current_episode = self.current_episode()
        
        if current_episode == False:
            return False

        next_episode = {}
        next_episode["id"] = current_episode["id"] + 1
        next_episode["post_date"] = current_episode["post_date"] + timedelta(days=self.EPISODE_INTERVAL_IN_DAYS)
        next_episode["period"] = self.period_episode(next_episode["post_date"])

        self.log.debug ("Next episode: {0}".format(next_episode))
        return next_episode
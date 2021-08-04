from datetime import date

class CompiladoFormatter:
    EPISODE_NUMERIC_SYMBOL = '#'

    def episode(self, episode: int):
        numeric_symbol = self.EPISODE_NUMERIC_SYMBOL
        episode = str(episode).zfill(3)
        return numeric_symbol + episode

    def period(self, start_date: date, end_date: date):
        return start_date.strftime('%d/%m') + ' a ' + end_date.strftime('%d/%m')
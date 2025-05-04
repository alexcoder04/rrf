
class Time:
    def __init__(self, hour, minute):
        if not (0 <= hour < 24) or not (0 <= minute < 60):
            raise ValueError("Invalid time: hour must be 0–23 and minute must be 0–59")
        self.hour = hour
        self.minute = minute

    def __repr__(self):
        return f"{self.hour:02d}:{self.minute:02d}"

    def _total_minutes(self):
        return self.hour * 60 + self.minute

    def __eq__(self, other):
        return self._total_minutes() == other._total_minutes()

    def __lt__(self, other):
        return self._total_minutes() < other._total_minutes()

    def __le__(self, other):
        return self._total_minutes() <= other._total_minutes()

    def __gt__(self, other):
        return self._total_minutes() > other._total_minutes()

    def __ge__(self, other):
        return self._total_minutes() >= other._total_minutes()

    def __ne__(self, other):
        return not self.__eq__(other)

    def __sub__(self, other):
        if not isinstance(other, Time):
            return NotImplemented
        return self._total_minutes() - other._total_minutes()



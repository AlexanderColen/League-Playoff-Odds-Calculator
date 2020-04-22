from functools import total_ordering
from typing import List


@total_ordering
class Team:
    name: str
    wins: int
    losses: int
    average_win_time: int
    total_win_time: int
    red_wins: int
    red_losses: int
    red_win_loss: float
    blue_wins: int
    blue_losses: int
    blue_win_loss: float
    won_vs: List[str]
    lost_vs: List[str]
    own_h2h: List[str]
    lost_h2h: List[str]

    def __init__(self, name: str, wins: int = 0, losses: int = 0):
        self.name = name
        self.wins = wins
        self.losses = losses
        self.average_win_time = 0
        self.total_win_time = 0
        self.red_wins = 0
        self.red_losses = 0
        self.red_win_loss = 0.0
        self.blue_wins = 0
        self.blue_losses = 0
        self.blue_win_loss = 0.0
        self.won_vs = []
        self.lost_vs = []
        self.own_h2h = []
        self.lost_h2h = []

    def add_win(self, playtime: int, side: str, enemy: str):
        self.wins += 1
        self.total_win_time += playtime
        self.average_win_time = self.total_win_time // self.wins

        # Keep track of head-to-head for tiebreakers.
        if enemy in self.won_vs:
            self.won_vs.remove(enemy)
            self.own_h2h.append(enemy)
        else:
            self.won_vs.append(enemy)

        # Recalculate win % per side.
        if side == 'red':
            self.red_wins += 1
            self.red_win_loss = round(self.red_wins / (self.red_wins + self.red_losses) * 100, 2)
        else:
            self.blue_wins += 1
            self.blue_win_loss = round(self.blue_wins / (self.blue_wins + self.blue_losses) * 100, 2)

    def add_loss(self, side: str, enemy: str):
        self.losses += 1

        # Keep track of head-to-head for tiebreakers.
        if enemy in self.lost_vs:
            self.lost_vs.remove(enemy)
            self.lost_h2h.append(enemy)
        else:
            self.lost_vs.append(enemy)

        # Recalculate loss % per side.
        if side == 'red':
            self.red_losses += 1
            self.red_win_loss = round(self.red_wins / (self.red_wins + self.red_losses) * 100, 2)
        else:
            self.blue_losses += 1
            self.blue_win_loss = round(self.blue_wins / (self.blue_wins + self.blue_losses) * 100, 2)

    def __eq__(self, other):
        return self.wins == other.wins \
               and self.losses == other.losses \
               and other.name not in self.own_h2h \
               and other.name not in self.lost_h2h \
               and self.average_win_time == other.average_win_time \
               and self.name == other.name

    def __lt__(self, other):
        # Sort on wins first.
        if self.wins > other.wins:
            return False
        elif self.wins < other.wins:
            return True
        else:
            # Sort on losses second if wins are equal.
            if self.losses < other.losses:
                return False
            elif self.losses > other.losses:
                return True
            else:
                # Sort on head-to-head if losses are also equal.
                if other.name in self.own_h2h:
                    return False
                elif other.name in self.lost_h2h:
                    return True
                else:
                    # Sort on average win-time if head-to-head are also equal.
                    if self.average_win_time < other.average_win_time:
                        return False
                    elif self.average_win_time > other.average_win_time:
                        return True
                    else:
                        # If everything is equal, just sort alphabetically.
                        if self.name > other.name:
                            return False
                        elif self.name < other.name:
                            return True
                        else:
                            # If all else fails. It's a tie.
                            return True

    def __str__(self) -> str:
        m, s = divmod(self.average_win_time, 60)
        avg_win_str = f'{m:02d}:{s:02d}'
        return f'{self.name}: {self.wins}-{self.losses} - Avg Win: {avg_win_str}' \
            f' - Red % {self.red_win_loss} ({self.red_wins}-{self.red_losses})' \
            f' - Blue % {self.blue_win_loss} ({self.blue_wins}-{self.blue_losses})' \
            f' - Owns H2H vs {self.own_h2h}' \
            f' - Loses H2H vs {self.lost_h2h}'

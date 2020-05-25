from typing import List


class Odds:
    team_name: str
    win_loss: str
    total_times: int
    rank_times: List[int]
    rank_odds: List[float]

    def __init__(self, team_name: str, wins: int, losses: int, total_teams: int):
        self.team_name = team_name
        self.win_loss = f'{wins}-{losses}'
        self.total_times = 0
        self.rank_times = [0] * total_teams
        self.rank_odds = [0] * total_teams

    def calculate_odds(self):
        for i, times in enumerate(self.rank_times):
            if times > 0:
                self.rank_odds[i] = times / self.total_times

    def add_possibility(self, rank: int):
        self.total_times += 1
        self.rank_times[rank] += 1

    def __str__(self):
        formatted: str = f'Team: {self.team_name} - Total: {self.total_times}'
        for i, times in enumerate(self.rank_times):
            formatted += f' - {i + 1}: {times} ({self.rank_odds[i]})' \

        return formatted

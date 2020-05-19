from models.team import Team
import time


class Match:
    red_team: str
    blue_team: str
    winner: str
    playtime: int

    def __init__(self, blue_team: str, red_team: str, winner: str = None, playtime: int = None):
        self.blue_team = blue_team
        self.red_team = red_team
        self.winner = winner
        self.playtime = playtime

    def __str__(self) -> str:
        return f'{self.red_team} vs {self.blue_team} - Winner: {self.winner} - Playtime: {self.playtime}'

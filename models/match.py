from models.team import Team
import time


class Match:
    red_team: Team
    blue_team: Team
    winner: str
    playtime: int

    def __init__(self, blue_team: Team, red_team: Team, winner: str = None, playtime: int = None):
        self.blue_team = blue_team
        self.red_team = red_team
        self.winner = winner
        self.playtime = playtime

    def __str__(self) -> str:
        return f'{self.red_team.name} vs {self.blue_team.name} - Winner: {self.winner} - Playtime: {self.playtime}'

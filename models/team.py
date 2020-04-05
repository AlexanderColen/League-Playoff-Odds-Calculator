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

    def add_win(self, playtime: int, side: str):
        self.wins += 1
        self.total_win_time += playtime
        self.average_win_time = self.total_win_time // self.wins

        if side == 'red':
            self.red_wins += 1
            self.red_win_loss = round(self.red_wins / (self.red_wins + self.red_losses) * 100, 2)
        else:
            self.blue_wins += 1
            self.blue_win_loss = round(self.blue_wins / (self.blue_wins + self.blue_losses) * 100, 2)

    def add_loss(self, side: str):
        self.losses += 1

        if side == 'red':
            self.red_losses += 1
            self.red_win_loss = round(self.red_wins / (self.red_wins + self.red_losses) * 100, 2)
        else:
            self.blue_losses += 1
            self.blue_win_loss = round(self.blue_wins / (self.blue_wins + self.blue_losses) * 100, 2)

    def __str__(self) -> str:
        m, s = divmod(self.average_win_time, 60)
        avg_win_str = f'{m:02d}:{s:02d}'
        return f'{self.name}: {self.wins}-{self.losses} - Avg Win: {avg_win_str}' \
            f' - Red % {self.red_win_loss} ({self.red_wins}-{self.red_losses})' \
            f' - Blue % {self.blue_win_loss} ({self.blue_wins}-{self.blue_losses})'

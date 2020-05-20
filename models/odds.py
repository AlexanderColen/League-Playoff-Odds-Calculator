class Odds:
    team_name: str
    win_loss: str
    total_times: int
    first_odds: float
    first_times: int
    second_odds: float
    second_times: int
    third_odds: float
    third_times: int
    fourth_odds: float
    fourth_times: int
    fifth_odds: float
    fifth_times: int
    sixth_odds: float
    sixth_times: int
    seventh_odds: float
    seventh_times: int
    eighth_odds: float
    eighth_times: int
    ninth_odds: float
    ninth_times: int
    tenth_odds: float
    tenth_times: int

    def __init__(self, team_name: str, wins: int, losses: int):
        self.team_name = team_name
        self.win_loss = f'{wins}-{losses}'
        self.total_times = 0
        self.first_times = 0
        self.first_odds = 0
        self.second_times = 0
        self.second_odds = 0
        self.third_times = 0
        self.third_odds = 0
        self.fourth_times = 0
        self.fourth_odds = 0
        self.fifth_times = 0
        self.fifth_odds = 0
        self.sixth_times = 0
        self.sixth_odds = 0
        self.seventh_times = 0
        self.seventh_odds = 0
        self.eighth_times = 0
        self.eighth_odds = 0
        self.ninth_times = 0
        self.ninth_odds = 0
        self.tenth_times = 0
        self.tenth_odds = 0

    def calculate_odds(self):
        if self.first_times > 0:
            self.first_odds = round(self.first_times / self.total_times * 100, 2)
        if self.second_times > 0:
            self.second_odds = round(self.second_times / self.total_times * 100, 2)
        if self.third_times > 0:
            self.third_odds = round(self.third_times / self.total_times * 100, 2)
        if self.fourth_times > 0:
            self.fourth_odds = round(self.fourth_times / self.total_times * 100, 2)
        if self.fifth_times > 0:
            self.fifth_odds = round(self.fifth_times / self.total_times * 100, 2)
        if self.sixth_times > 0:
            self.sixth_odds = round(self.sixth_times / self.total_times * 100, 2)
        if self.seventh_times > 0:
            self.seventh_odds = round(self.seventh_times / self.total_times * 100, 2)
        if self.eighth_times > 0:
            self.eighth_odds = round(self.eighth_times / self.total_times * 100, 2)
        if self.ninth_times > 0:
            self.ninth_odds = round(self.ninth_times / self.total_times * 100, 2)
        if self.tenth_times > 0:
            self.tenth_odds = round(self.tenth_times / self.total_times * 100, 2)

    def add_possibility(self, rank: int):
        self.total_times += 1
        if rank == 1:
            self.first_times += 1
        elif rank == 2:
            self.second_times += 1
        elif rank == 3:
            self.third_times += 1
        elif rank == 4:
            self.fourth_times += 1
        elif rank == 5:
            self.fifth_times += 1
        elif rank == 6:
            self.sixth_times += 1
        elif rank == 7:
            self.seventh_times += 1
        elif rank == 8:
            self.eighth_times += 1
        elif rank == 9:
            self.ninth_times += 1
        elif rank == 10:
            self.tenth_times += 1

        self.calculate_odds()

    def __str__(self):
        return f'Team: {self.team_name} - Total: {self.total_times}' \
            f' - First: {self.first_times} ({self.first_odds})' \
            f' - Second: {self.second_times} ({self.second_odds})' \
            f' - Third: {self.third_times} ({self.third_odds})' \
            f' - Fourth: {self.fourth_times} ({self.fourth_odds})' \
            f' - Fifth: {self.fifth_times} ({self.fifth_odds})' \
            f' - Sixth: {self.sixth_times} ({self.sixth_odds})' \
            f' - Seventh: {self.seventh_times} ({self.seventh_odds})' \
            f' - Eighth: {self.eighth_times} ({self.eighth_odds})' \
            f' - Ninth: {self.ninth_times} ({self.ninth_odds})' \
            f' - Tenth: {self.tenth_times} ({self.tenth_odds})'

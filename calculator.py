import itertools
from typing import Any, Dict, Iterable, List, Tuple
from models.match import Match
from models.team import Team


def read_teams() -> List[Team]:
    """
    Reads the team names from the resources/teams.txt file.
    :return: A list with all the teams as Team objects.
    """
    t: List[Team] = []
    with open('resources/teams.txt', 'r', encoding='utf-8') as f:
        for l in f:
            t.append(Team(name=l.rstrip('\n')))

    return t


def generate_results() -> List[List]:
    """
    Reads the results and increments wins and losses in the list of teams appropriately.
    :return: The list of teams with their new wins and losses.
    """
    t: List[Team] = read_teams()
    m: List[Match] = []

    with open('resources/results.txt', 'r', encoding='utf-8') as f:
        for l in f:
            w = l.split()
            match: Match = Match(blue_team=w[0], red_team=w[1])

            if len(w) == 4:
                match.winner = w[2]
                match.playtime = int(w[3].split(':')[0]) * 60 + int(w[3].split(':')[1])

            m.append(match)

            # Only add wins/losses when there was a match winner. Otherwise it hasn't been played yet.
            if match.winner:
                for team in t:
                    if team.name == match.red_team:
                        if match.winner == 'red':
                            team.add_win(playtime=match.playtime, side='red', enemy=match.blue_team)
                        else:
                            team.add_loss(side='red', enemy=match.blue_team)
                    elif team.name == match.blue_team:
                        if match.winner == 'blue':
                            team.add_win(playtime=match.playtime, side='blue', enemy=match.red_team)
                        else:
                            team.add_loss(side='blue', enemy=match.red_team)

    return [t, m]


def sort_standings(t: List[Team]) -> List[Team]:
    """
    Sort the standings based on multiple Team attributes.
    :param t: The List of Teams.
    :return: The sorted List of Teams.
    """
    sorted_teams: List[Team] = sorted(t)
    sorted_teams.reverse()
    return sorted_teams


if __name__ == '__main__':
    teams, matches = generate_results()
    standings: List[Team] = sort_standings(t=teams)

    for s in standings:
        print(s)

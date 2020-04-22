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


def calculate_three_way_ties(t: List[Team]) -> List[Team]:
    tied_teams: List[Team] = []
    tied_teams_indexes: List[int] = []
    three_way_ties = []
    three_way_ties_indexes = []
    last_win_loss = 0
    for r, te in enumerate(t):
        team_win_loss = te.wins / te.losses
        if team_win_loss != last_win_loss:
            last_win_loss = team_win_loss
            tied_teams = [te]
            tied_teams_indexes = [r]
        else:
            tied_teams.append(te)
            tied_teams_indexes.append(r)

        # Save the three way tie.
        if len(tied_teams) == 3:
            three_way_ties.append(tied_teams)
            three_way_ties_indexes.append(tied_teams_indexes)

    # Recalculate order of teams that are in three way ties.
    for num, tie in enumerate(three_way_ties):
        mini_bracket: List[Team] = []
        bracket_team_names: List[str] = []
        for team in tie:
            # Redefine Team for mini_bracket.
            bracket_team: Team = Team(team.name)
            bracket_team.won_vs = team.won_vs
            bracket_team.lost_vs = team.lost_vs

            mini_bracket.append(bracket_team)
            bracket_team_names.append(bracket_team.name)

        print('\nZipped Before:')
        zipped = list(zip(tie, three_way_ties_indexes[num]))
        for z in zipped:
            print(f'{z[0].name} - {z[1]}')

        for team in mini_bracket:
            # Add wins.
            for win in team.won_vs:
                if win in bracket_team_names:
                    team.wins += 1
            # Add losses.
            for loss in team.lost_vs:
                if loss in bracket_team_names:
                    team.losses += 1

        sorted_bracket = sorted(mini_bracket)
        sorted_bracket.reverse()
        three_way_ties[num] = sorted_bracket

    # Reorder standings with these results.
    new_standings: List[Team] = t
    # TODO: Magic.
    return new_standings


if __name__ == '__main__':
    teams, matches = generate_results()
    standings: List[Team] = sort_standings(t=teams)
    standings = calculate_three_way_ties(t=standings)

    for rank, s in enumerate(standings):
        print(f'{rank+1}: {s}')

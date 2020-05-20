from copy import deepcopy
import time
from typing import List
from models.match import Match
from models.odds import Odds
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
    p: List[Match] = []
    u: List[Match] = []

    with open('resources/results.txt', 'r', encoding='utf-8') as f:
        for l in f:
            w = l.split()
            match: Match = Match(blue_team=w[0], red_team=w[1])

            # Match has been played and contains a winner and playtime.
            if len(w) == 4:
                match.winner = w[2]
                match.playtime = int(w[3].split(':')[0]) * 60 + int(w[3].split(':')[1])
                p.append(match)
            # Match has not been played yet.
            else:
                u.append(match)

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

    return [t, p, u]


def calculate_three_way_ties(t: List[Team]) -> List[Team]:
    """
    Calculate the result of three way ties based on H2H and average game time.
    :param t: The List of Teams.
    :return: The newly sorted List of Teams.
    """
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


def sort_standings(t: List[Team], print_outcomes: bool = True) -> List[Team]:
    """
    Sort the standings based on multiple Team attributes.
    :param t: The List of Teams.
    :param print_outcomes: Boolean indicating if the standings needs to be printed afterwards.
    :return: The sorted List of Teams.
    """
    sorted_teams: List[Team] = sorted(t)
    sorted_teams.reverse()
    sorted_teams = calculate_three_way_ties(sorted_teams)

    if print_outcomes:
        # Outputs the current standings.
        print('Current standings:')
        for rank, s in enumerate(sorted_teams):
            print(f'{rank + 1}: {s}')

    return sorted_teams


def increment_team_win_loss(match: Match, t: List[Team]) -> List[List[Team]]:
    """
    Add win and loss possibilities for a match.
    :param match: The Match that is to be played.
    :param t: The List of Teams.
    :return: A List containing possible standings.
    """
    possible_team_standings: List[List[Team]] = []
    # If red team wins
    new_teams: List[Team] = deepcopy(t)
    for team in new_teams:
        if team.name == match.red_team:
            # Take average game time of 30 minutes to not influence average win time as much.
            team.add_win(playtime=1800, side='red', enemy=match.blue_team)
        elif team.name == match.blue_team:
            team.add_loss(side='blue', enemy=match.red_team)

    possible_team_standings.append(new_teams)

    # If blue team wins
    new_teams: List[Team] = deepcopy(t)
    for team in new_teams:
        if team.name == match.red_team:
            team.add_loss(side='red', enemy=match.blue_team)
        elif team.name == match.blue_team:
            # Take average game time of 30 minutes to not influence average win time as much.
            team.add_win(playtime=1800, side='blue', enemy=match.red_team)

    possible_team_standings.append(new_teams)

    return possible_team_standings


def visualize_odds(odds: List[Odds]):
    """
    Visualize the standings as a table in the output window.
    :param odds: The List of Odds.
    """
    print(f'\nPredicted Standings Odds: ({odds[0].total_times} Total Scenarios)')
    column_width = 7
    print('-'*97)
    columns: List[str] = ['team', 'score', '1st', '2nd', '3rd', '4th', '5th', '6th', '7th', '8th', '9th', '10th']
    header_string: str = "|"
    for column in columns:
        header_string += f'{"{:^{width}}".format(column.capitalize(), width=column_width)}|'
    print(header_string)
    print('-'*97)
    for o in odds:
        # Team column.
        concatenated_string: str = f'|{"{:^{width}}".format(o.team_name, width=column_width)}|'
        # Score column.
        concatenated_string += f'{"{:^{width}}".format(o.win_loss, width=column_width)}|'
        # 1st column.
        concatenated_string += f'{"{:^{width}}".format(o.first_odds, width=column_width)}|'
        # 2nd column.
        concatenated_string += f'{"{:^{width}}".format(o.second_odds, width=column_width)}|'
        # 3rd column.
        concatenated_string += f'{"{:^{width}}".format(o.third_odds, width=column_width)}|'
        # 4th column.
        concatenated_string += f'{"{:^{width}}".format(o.fourth_odds, width=column_width)}|'
        # 5th column.
        concatenated_string += f'{"{:^{width}}".format(o.fifth_odds, width=column_width)}|'
        # 6th column.
        concatenated_string += f'{"{:^{width}}".format(o.sixth_odds, width=column_width)}|'
        # 7th column.
        concatenated_string += f'{"{:^{width}}".format(o.seventh_odds, width=column_width)}|'
        # 8th column.
        concatenated_string += f'{"{:^{width}}".format(o.eighth_odds, width=column_width)}|'
        # 9th column.
        concatenated_string += f'{"{:^{width}}".format(o.ninth_odds, width=column_width)}|'
        # 10th column.
        concatenated_string += f'{"{:^{width}}".format(o.tenth_odds, width=column_width)}|'
        print(concatenated_string)
        print('-'*97)


def predict_future_standings_loops(t: List[Team], u: List[Match], print_outcomes: bool = True) -> List[List[Team]]:
    """
    Predict the future standings based on unplayed matches with a 50% chance for either team to win.
    :param t: The List of Teams.
    :param u: The List of unplayed Matches.
    :param print_outcomes: Boolean indicating if the possible standings need to be printed afterwards.
    :return The List containing all outcome possibilities.
    """
    print(f'\n{"#"*30}\nPredicting future standings...\n{"#"*30}\n')
    possible_team_standings: List[List[Team]] = []
    for match_num, unplayed in enumerate(u):
        print(f'Predicting match #{match_num}/{len(u)}... ({unplayed.blue_team} vs {unplayed.red_team})')
        new_possibilities: List[List[Team]] = []
        if match_num == 0:
            new_possibilities.extend(increment_team_win_loss(match=unplayed, t=t))
        else:
            for p in possible_team_standings:
                new_possibilities.extend(increment_team_win_loss(match=unplayed, t=p))
        possible_team_standings.extend(new_possibilities)

    # Initialize the Odds list for each team.
    odds: List[Odds] = []
    for team in t:
        odds.append(Odds(team_name=team.name, wins=team.wins, losses=team.losses))

    # Splice the possible standings to only include the final 2^length of unplayed matches.
    spliced_standings = possible_team_standings[len(possible_team_standings)-2**len(u):]

    for i, possible in enumerate(spliced_standings):
        if print_outcomes:
            print(f'\nPrediction #{i+1}:')

        possible = sort_standings(t=possible, print_outcomes=print_outcomes)
        for num, p in enumerate(possible):
            for o in odds:
                if o.team_name == p.name:
                    o.add_possibility(num + 1)

    visualize_odds(odds=odds)

    return spliced_standings


if __name__ == '__main__':
    start = time.time()
    teams, played_matches, unplayed_matches = generate_results()
    # Calculates the current standings.
    standings: List[Team] = sort_standings(t=teams, print_outcomes=False)

    if len(unplayed_matches) > 0:
        # Predict possible standings with unplayed matches using loops.
        predict_future_standings_loops(standings, unplayed_matches, print_outcomes=False)

    end = time.time()
    print(f'Calculated in {end - start} seconds.')

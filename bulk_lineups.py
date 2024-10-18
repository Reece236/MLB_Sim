import joblib
import argparse
from src.single_game import SingleGameSimulator
from constants import LINEUPS, PITCHERS, PITCH_TEAMS, RUNS_CAP, INNINGS_CAP

def simulate(n, lineup, pitcher, pitch_team, run_cap=5, inning_cap=7):

    # Load the data
    transition_probs = joblib.load('data/simple_event_next_state_data.pkl')
    dist_bt = joblib.load('data/reg_bat_stats.pkl')
    dist_pt = joblib.load('data/pitch_stats_updated.pkl')
    team_pitching = joblib.load('data/team_bullpen_split.pkl')
    bat_sides = joblib.load('data/bat_sides.pkl')
    lg_dist = joblib.load('data/lg_dist_updated.pkl')
    stat_col = joblib.load('data/stat_col.pkl')
    pitcher_name_to_id = joblib.load('data/pitcher_name_to_id.pkl')
    batter_name_to_id = joblib.load('data/batter_name_to_id.pkl')
    pitch_teams = joblib.load('data/unique_pitch_teams.pkl')
    pitcher_hands = joblib.load('data/pitcher_hands.pkl')

    # Set the pitcher's runs and innings caps
    pitcher_dict = {pitcher_name_to_id[pitcher]: {'Runs Cap': run_cap, 'Inning Cap': inning_cap,
                                                  'Throws': pitcher_hands[pitcher_name_to_id[pitcher]]}}
    # Store the total runs
    total_runs = 0

    # Convert the lineup to ids
    lineup_ids = [batter_name_to_id[batter] for batter in lineup]

    # Create a game simulator
    game_simulator = SingleGameSimulator(transition_probs, dist_bt, dist_pt, team_pitching, pitch_team,
                                         bat_sides, lg_dist, stat_col, pitcher_dict, lineup_ids)

    for i in range(n):
        # Simulate the game
        game_simulator.simulate_game()

    # Recall the total runs and calculate the average
    runs = game_simulator.runs
    avg_runs = runs / n

    return avg_runs

def main(n: int, lineups: list, pitchers: list, pitch_teams: list, runs_cap: list, inning_cap: list):
    """
    Simulate a bulk of games for a list of lineups and pitchers.

    Parameters:
    n (int): Number of games to simulate
    lineups (list): List of lineups
    pitchers (list): List of pitchers
    pitch_teams (list): List of pitch teams
    runs_cap (list): List of runs caps for each pitcher
    inning_cap (list): List of inning caps for each pitcher

    """

    runs_list = []

    for i in range(len(lineups)):
        runs = simulate(n, lineups[i], pitchers[i], pitch_teams[i], runs_cap[i], inning_cap[i])
        runs_list.append(runs)

    for i in range(len(runs_list)):
        print(f'{lineups[i]}:')
        print(f'{round(runs_list[i],2)} runs per game\n')

def arg_parser():
    """
    Parse the command line arguments.

    Returns:
    args: The command line arguments
    """

    parser = argparse.ArgumentParser(description='Simulate a bulk of games for a list of lineups and pitchers.')
    parser.add_argument('-n', type=int, help='Number of games to simulate', required=True)
    parser.add_argument('-lineups', nargs='+', help='List of lineups', default=LINEUPS)
    parser.add_argument('-pitchers', nargs='+', help='List of pitchers', default=PITCHERS)
    parser.add_argument('-pitch_teams', nargs='+', help='List of pitch teams', default=PITCH_TEAMS)
    parser.add_argument('-runs_cap', nargs='+', type=int, help='List of runs caps for each pitcher', default=RUNS_CAP)
    parser.add_argument('-inning_cap', nargs='+', type=int, help='List of inning caps for each pitcher', default=INNINGS_CAP)


    args = parser.parse_args()

    return args

if __name__ == '__main__':

    args = arg_parser()
    
    main(args.n, args.lineups, args.pitchers, args.pitch_teams, args.runs_cap, args.inning_cap)
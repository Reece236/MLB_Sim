import joblib
from src.single_game import SingleGameSimulator

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

if __name__ == '__main__':

    # Simulations per lineup
    n = 10000

    # List of lineups
    # Players in Last, First, Team format
    lineups = [['Marte, Ketel, AZ', 'Carroll, Corbin, AZ', 'Moreno, Gabriel, AZ','Walker, Christian, AZ', 'Pham, Tommy, AZ',
                'Gurriel, Lourdes, AZ', 'Longoria, Evan, AZ', 'Rivera, Emmanuel, AZ', 'Perdomo, Geraldo, AZ'],
               ['Schwarber, Kyle, PHI', 'Turner, Trea, PHI', 'Harper, Bryce, PHI', 'Bohm, Alec, PHI', 'Stott, Bryson, PHI',
                'Realmuto, J.T., PHI', 'Castellanos, Nick, PHI', 'Marsh, Brandon, PHI', 'Rojas, Johan, PHI']]

    # List of pitchers
    # Players in Last, First, Team format
    pitchers = ['Suarez, Ranger, PHI', 'Pfaadt, Brandon, AZ']

    # List of pitch teams
    pitch_teams = ['PHI', 'AZ']

    # Set the caps for runs and innings for each starting pitcher
    runs_cap = [4, 4]
    inning_cap = [5, 5]

    runs_list = []

    for i in range(len(lineups)):
        runs = simulate(n, lineups[i], pitchers[i], pitch_teams[i])
        runs_list.append(runs)

    for i in range(len(runs_list)):
        print(f'{lineups[i]}:')
        print(f'{round(runs_list[i],2)} runs per game\n')

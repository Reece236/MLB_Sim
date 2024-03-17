from flask import Flask, render_template, request
import joblib
from src.single_game import SingleGameSimulator

app = Flask(__name__)

pitcher_name_to_id = joblib.load('data/pitcher_name_to_id.pkl')
batter_name_to_id = joblib.load('data/batter_name_to_id.pkl')
pitch_teams = joblib.load('data/unique_pitch_teams.pkl')

# Set up the dropdown options
hitters = list(batter_name_to_id.keys())
pitchers = list(pitcher_name_to_id.keys())
bullpen_teams = list(pitch_teams)

# Make sure the dropdown options are sorted
hitters.sort()
pitchers.sort()
bullpen_teams.sort()

@app.route('/')
def index():
    return render_template('index.html', hitters=hitters, pitchers=pitchers, bullpen_teams=bullpen_teams)

@app.route('/simulate', methods=['POST'])
def simulate():
    # Handle the form submission and simulation logic here
    n = int(request.form['n'])
    lineup = [request.form[f'hitter{i}'] for i in range(1, 10)]
    pitcher = request.form['pitcher']
    pitch_team = request.form['pitch_team']

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

    pitcher_dict = {pitcher_name_to_id[pitcher]: {'Runs Cap': 5, 'Inning Cap': 7,
                                                  'Throws': pitcher_hands[pitcher_name_to_id[pitcher]]}}

    total_runs = 0

    lineup_ids = [batter_name_to_id[batter] for batter in lineup]

    for i in range(n):
        game_simulator = SingleGameSimulator(transition_probs, dist_bt, dist_pt, team_pitching, pitch_team,
                                             bat_sides, lg_dist, stat_col, pitcher_dict, lineup_ids)
        runs = game_simulator.simulate_game()
        total_runs += runs

    avg_runs = total_runs / n

    return render_template('result.html', avg_runs=avg_runs)

if __name__ == '__main__':
    app.run(debug=True)

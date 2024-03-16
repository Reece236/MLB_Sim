# Path: single_game.py
import random
import numpy as np
import joblib
import datetime
import pandas as pd

class SingleGameSimulator:
    def __init__(self, transition_probs, dist_bt, dist_pt, team_pitching, pitch_team, bat_sides, lg_dist, stat_col,
                 pitcher_dict, lineup, bunt_thresholds=None):
        self.transition_probs = transition_probs
        self.dist_bt = dist_bt
        self.dist_pt = dist_pt
        self.team_pitching = team_pitching
        self.pitch_team = pitch_team
        self.bat_sides = bat_sides
        self.lg_dist = lg_dist
        self.stat_col = stat_col
        self.pitcher_num = 0
        self.pitcher_dict = pitcher_dict
        self.game_lineup = lineup
        self.batter = 0
        self.runs = 0
        self.bunt_thresholds = bunt_thresholds

    def update_matchup_stats(self):
        # runs allowed by the pitcher and innings pitched
        pitcher_runs = 0
        pitcher_inning = 0
        pitcher_dist = {}

        # Create a df with stats against lhp and rhp
        '''game_lineup_r = self.game_lineup.copy()
        game_lineup_l = self.game_lineup.copy()
        for player in range(len(self.game_lineup)):
            game_lineup_r = dict([(player, 'R') for player in self.game_lineup])
            game_lineup_l = dict([(player, 'L') for player in self.game_lineup])
        print(game_lineup_r)
        print(game_lineup_l)'''

        # If pitcher_dict is not None, set the pitcher's stats to the first pitcher       in the dictionary
        if self.pitcher_dict is not None:
            pitchers_list = list(self.pitcher_dict.keys())
            if self.pitcher_num <= len(pitchers_list):
                pitcher = pitchers_list[self.pitcher_num]
                try:
                    pitcher_dist['L'] = self.dist_pt[(pitcher, 'L')]
                    pitcher_dist['R'] = self.dist_pt[(pitcher, 'R')]
                except:
                    pitcher_dist['L'] = pd.Series(self.lg_dist)
                    pitcher_dist['R'] = pd.Series(self.lg_dist)

                pitcher_runs_cap = self.pitcher_dict[pitcher]['Runs Cap']
                pitcher_inning_cap = self.pitcher_dict[pitcher]['Inning Cap']
                p_throws = self.pitcher_dict[pitcher]['Throws']

            # If we have gone through all the pitchers, use the team's bullpen stats. Randomly select handedness based on the bullpen's handedness frequency
            else:
                print('there')
                freq = self.team_pitching[(self.pitch_team, 'L', 'R')]['freq%'] + self.team_pitching[(self.pitch_team, 'L', 'L')]['freq%']
                p_throws = random.choices(['L', 'R'], weights=[freq, 1 - freq])[0]
                for side in ['L', 'R']:
                    pitcher_dist[side] = self.team_pitching[(self.pitch_team, p_throws, side)]
                pitcher_runs_cap = 2
                pitcher_inning_cap = 1

        else:
            freq = self.team_pitching[(self.pitch_team, 'L', 'R')]['freq%'] + self.team_pitching[(self.pitch_team, 'L', 'L')]['freq%']
            p_throws = random.choices(['L', 'R'], weights=[freq, 1 - freq])[0]
            for side in ['L', 'R']:
                pitcher_dist[side] = self.team_pitching[(self.pitch_team, p_throws, side)]
            pitcher_runs_cap = 2
            pitcher_inning_cap = 1

        '''if p_throws == 'R':
            game_lineup = game_lineup_r
        else:
            game_lineup = game_lineup_l'''

        batter_stats = {}
        pitcher_stats = {}

        # Create a list of the batters' handedness
        b_side = []
        for batter in self.game_lineup:
            b_side.append(self.bat_sides[batter])


        # Loop through each batter in game_lineup and append their stats to batter_stats
        for n, batterId in enumerate(self.game_lineup):

            try:
                batter_stats[n] = self.dist_bt[(batterId, p_throws)]
            except:
                batter_stats[n] = pd.Series(self.lg_dist)

        for n, side in enumerate(b_side):
            pitcher_stats[n] = pitcher_dist[side]

        # Set weights based on previous research
        player_stats = {}

        for batter in batter_stats:
            player_stats[batter] = np.array(batter_stats[batter]) * .72 + np.array(pitcher_stats[batter][0:42]) * .28


        return player_stats, pitcher_runs, pitcher_inning, pitcher_dist, batter_stats, pitcher_stats, pitcher_inning_cap, pitcher_runs_cap

    def simulate_game(self):


            ### Set up the game ##


            player_stats, pitcher_runs, pitcher_inning, pitcher_dist, batter_stats, pitcher_stats, pitcher_inning_cap, pitcher_runs_cap = self.update_matchup_stats()

            for _ in range(9):
                pitcher_inning += 1
                current_state = '0/000'
                inning_runs = 0
                while current_state != '3/000':
                    try:
                        weights = list(player_stats[self.batter])
                    except:
                        print('ahhh fire')

                    if self.bunt_thresholds != None and current_state in self.transition_probs[
                        'Bunt'].keys() and current_state in self.bunt_thresholds.keys():
                        batter_rv = player_stats.iloc[self.batter][current_state]
                        if batter_rv < self.bunt_thresholds[current_state]:
                            result = 'Bunt'
                        else:
                            result = random.choices(self.stat_col, weights=weights)[0]
                    else:
                        result = random.choices(self.stat_col, weights=weights)[0]


                    # print(result,current_state )

                    if current_state not in self.transition_probs[result] and (
                            result[0:6] != 'triple' and result[0:8] != 'home_run'):
                        base = int(result[-1])
                        delta = random.choice([-1, 1])
                        new_result = result[:-1] + str(base + delta)
                        if new_result in self.transition_probs:
                            if current_state in self.transition_probs[new_result]:
                                result = new_result
                                break
                        new_result = result[:-1] + str(base + -1 * delta)
                        if new_result in self.transition_probs:
                            if current_state in self.transition_probs[new_result]:
                                result = new_result
                                break

                        new_result = result[:-1] + str(base + 2 * delta)
                        if new_result in self.transition_probs:
                            if current_state in self.transition_probs[new_result]:
                                result = new_result
                                break

                        new_result = result[:-1] + str(base + -2 * delta)
                        if new_result in self.transition_probs:
                            if current_state in self.transition_probs[new_result]:
                                result = new_result
                                break

                        else:
                            print(f'No transition from {current_state} to {result}')
                            break

                    if current_state in self.transition_probs[result] or result[0:6] == 'triple' or result[0:8] == 'home_run':

                        if current_state not in self.transition_probs[result]:
                            if result[0:8] == 'home_run':
                                next_state = f'{current_state[0]}/000'
                            else:
                                next_state = f'{current_state[0]}/001'
                        else:
                            next_state_probs = self.transition_probs[result][current_state]
                            next_states = list(next_state_probs.keys())
                            next_state = random.choices(next_states, weights=list(next_state_probs.values()))[0]

                        # Calculate runs scored based on the difference between new and old state values
                        old_outs, old_runners = map(int, current_state.split('/'))
                        old_runner = 0
                        for runner in str(old_runners):
                            if runner != '0':
                                old_runner += 1
                        old_runners = old_runner
                        old_state_value = old_outs + old_runners + 1
                        new_outs, new_runners = map(int, next_state.split('/'))
                        new_runner = 0
                        for runner in str(new_runners):
                            if runner != '0':
                                new_runner += 1
                        new_runners = new_runner
                        new_state_value = new_outs + new_runners
                        if next_state != '3/000':
                            runs_scored = old_state_value - new_state_value
                        else:
                            runs_scored = 0

                        current_state = next_state
                        inning_runs += runs_scored
                        pitcher_runs += runs_scored

                        if self.batter >= 8:
                            self.batter = 0
                        else:
                            self.batter += 1

                        player_stats, pitcher_runs, pitcher_inning, pitcher_dist, batter_stats, pitcher_stats, pitcher_inning_cap, pitcher_runs_cap = self.update_matchup_stats()

                    else:
                        print(f'No transition from {current_state} to {result}')
                        break

                self.runs += inning_runs

            return self.runs

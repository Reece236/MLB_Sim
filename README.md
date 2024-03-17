# MLB_Sim

### By Reece Calvin

### Presented at 2024 SABR Analytics Conference

## Uses

### `python app.py`

Run `app.py` to simulate an individual lineup.

  #### Inputs:

  `Simulations to Run`: Number of simulations for the lineup
  `Lineup Order`: The lineup order
  `Starter`: The starting pitcher
  `SP Runs Cap`: Max runs allowed before pulling starting pitcher
  `SP Innings Cap `: Max Innings Pitched allowed for the starting pitcher
  `Bullpen Team`: Bullpen team to use after replacing starter. Optimizes platoon advantage based on current batter.



### `python bulk_lineups.py`

  `bulk_lineups.py` allows one to simulate multiple games at a time. Adjusts inputs, listed below, before running file.
  
  #### Inputs:
  
  `n`: Number of simulations for each lineup
   
   Ex: n=10000
  
   
  `lineups`: A list of list storing lineups. Player are listed in Last, First, Team format
   
   Ex: lineups = [['Marte, Ketel, AZ', 'Carroll, Corbin, AZ', 'Moreno, Gabriel, AZ','Walker, Christian, AZ', 'Pham, Tommy, AZ',
                  'Gurriel, Lourdes, AZ', 'Longoria, Evan, AZ', 'Rivera, Emmanuel, AZ', 'Perdomo, Geraldo, AZ'],
                 ['Schwarber, Kyle, PHI', 'Turner, Trea, PHI', 'Harper, Bryce, PHI', 'Bohm, Alec, PHI', 'Stott, Bryson, PHI',
                  'Realmuto, J.T., PHI', 'Castellanos, Nick, PHI', 'Marsh, Brandon, PHI', 'Rojas, Johan, PHI']]
  
  
  `pitchers`: Pitchers in Last, First, Team format
  
   Ex: pitchers = ['Suarez, Ranger, PHI', 'Pfaadt, Brandon, AZ']
  
  
  `pitch_teams`: List of pitch teams
  
   Ex: pitch_teams = ['PHI', 'AZ']
  
  
  `runs_cap`: the runs cap for a starting pitcher
  
   runs_cap = [4, 4]
  
  
   `inning_cap`: the inning cap for a starting pitcher
  
    inning_cap = [5, 5]


  
Uses 2023 Statcast data. 

premier_league_url = "https://fbref.com/en/comps/9/Premier-League-Stats"
la_liga_url = "https://fbref.com/en/comps/12/La-Liga-Stats"
premier_league_24_url = "https://fbref.com/en/comps/9/2023-2024/2023-2024-Premier-League-Stats"

stats_wanted = {
    "Standard Stats": ["games", "minutes", "goals", "assists", "cards_yellow"],
    "Shooting": ["shots"],
    "Goalkeeping": ["gk_saves"],
    "Passing": ["passes", "assisted_shots"],
    "Defensive Actions": ["tackles", "interceptions", "clearances"],
    "Miscellaneous Stats": ["fouls", "fouled"]
}
year = "2023-2024"
team_stats_wanted = {
    "Squad Standard Stats": ["games", "goals", "assists", "cards_yellow"],
    "Squad Shooting": ["shots"],
    "Squad Goalkeeping": ["gk_saves"],
    "Squad Passing": ["passes", "assisted_shots"],
    "Squad Defensive Actions": ["tackles", "interceptions", "clearances"],
    "Squad Miscellaneous Stats": ["fouls", "fouled"]
}

def get_stats_wanted(type = 'pp'):
    return list(pp_to_fbref_stats.keys()) if type == 'pp' else ["name", "team", "games", "minutes"] + list(fbref_to_pp_stats.keys()) 

fbref_to_pp_stats = {
    "gk_saves": "Goalie Saves",
    "clearances": "Clearances",
    "tackles": "Tackles",
    "assisted_shots": "Shots Assisted",
    "fouled": "Fouls Drawn",
    "shots": "Shots",
    "crosses": "Crosses",
    "shots_on_target": "Shots On Target",
    "passes": "Passes Attempted",
    "interceptions": "Interceptions",
    "fouls": "Fouls",
    "goals": "Goals",
    "assists": "Assists",
    "cards_yellow": "Yellow Cards",
}

pp_to_fbref_stats = {
    "Goalie Saves": "gk_saves",
    "Clearances": "clearances",
    "Tackles": "tackles",
    "Shots Assisted": "assisted_shots",
    "Fouls Drawn": "fouled",
    "Shots": "shots",
    "Crosses": "crosses",
    "Shots On Target": "shots_on_target",
    "Passes Attempted": "passes",
    "Interceptions": "interceptions",
    "Fouls": "fouls",
    "Goals": "goals",
    "Assists": "assists"
}

"""
['name',
 'Pitcher Fantasy Score',
 'Hits Allowed',
 'Pitcher Strikeouts',
 'Pitching Outs',
 'Earned Runs Allowed',
 'Walks Allowed',
 'Hits+Runs+RBIS',
 'Hitter Strikeouts',
 'Hitter Fantasy Score',
 'Total Bases',
 'Runs',
 'Walks',
 """


"""
 'home runs',
 'home runs_Over',
 'home runs_Under',
 'hits',
 'hits_Over',
 'hits_Under',
 'total bases',
 'total bases_Over',
 'total bases_Under',
 'rbis',
 'rbis_Over',
 'rbis_Under',
 'runs',
 'runs_Over',
 'runs_Under',
 'hits + runs + rbis',
 'hits + runs + rbis_Over',
 'hits + runs + rbis_Under',
 'strikeouts',
 'strikeouts_Over',
 'strikeouts_Under',
 'singles',
 'singles_Over',
 'singles_Under',
 'doubles',
 'doubles_Under',
 'walks',
 'walks_Over',
 'walks_Under',
 'doubles_Over',
 'stolen bases',
 'stolen bases_Over',
 'stolen bases_Under',
 'triples',
 'triples_Over',
 'triples_Under',
 'strikeouts thrown',
 'strikeouts thrown_Over',
 'strikeouts thrown_Under',
 'outs',
 'outs_Over',
 'outs_Under']
"""

pp_to_dk_stats = {
    "Rebounds": "rebounds",
    "Points": "points",
    "Pts+Asts": "points + assists",
    "Pts+Rebs": "points + rebounds",
    "Pts+Rebs+Asts": "points + rebounds + assists",
    "Assists": "assists",
    "Rebs+Asts": "rebounds + assists",
    "Fantasy Score": "fantasy score",
    "3-PT Made": "three pointers made",
    'Hits Allowed': 'hits',
    'Pitcher Strikeouts': 'strikeouts thrown',
    'Pitching Outs': 'outs',
    # 'Earned Runs Allowed': 'earned runs',
    'Walks Allowed': 'walks',
    'Hits+Runs+RBIS': 'hits + runs + rbis',
    'Hitter Strikeouts': 'hitter strikeouts',
    'Total Bases': 'total bases',
    'Runs': 'runs',
    'Walks': 'walks'
}

dk_to_pp_stats = {
    "rebounds": "Rebounds",
    "points": "Points",
    "points + assists": "Pts+Asts",
    "points + rebounds": "Pts+Rebs",
    "points + rebounds + assists": "Pts+Rebs+Asts",
    "assists": "Assists",
    "rebounds + assists": "Rebs+Asts",
    "fantasy score": "Fantasy Score",
    "three pointers made": "3-PT Made",
    'hits': 'Hits Allowed',
    'strikeouts thrown': 'Pitcher Strikeouts',
    'outs': 'Pitching Outs',
    # 'earned runs': 'Earned Runs Allowed',
    'walks': 'Walks Allowed',
    'hits + runs + rbis': 'Hits+Runs+RBIS',
    'hitter strikeouts': 'Hitter Strikeouts',
    'total bases': 'Total Bases',
    'runs': 'Runs',
    'walks': 'Walks'
    
}


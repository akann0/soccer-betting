premier_league_url = "https://fbref.com/en/comps/9/Premier-League-Stats"
la_liga_url = "https://fbref.com/en/comps/12/La-Liga-Stats"

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
    return list(pp_to_fbref_stats.keys()) if type == 'pp' else ["name", "games", "minutes"] + list(fbref_to_pp_stats.keys()) 

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


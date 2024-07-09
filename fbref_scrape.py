import requests
from bs4 import BeautifulSoup as bs
import time, random, csv
from unidecode import unidecode
from constants import *
import os

TEAMS_TO_FIND = 1
PLAYERS_PER_TEAM = 1

def test_print(response, x):
    to_test = [0, 14]
    if x in to_test:
        if isinstance(response, list):
            for i in range(min(len(response), 10)):
                print(response[i])
        else:
            print(response)


# Prints the url and status code of the response, allowing for easier debugging
def requests_test(response, url=""):
    #return None - uncomment this to disable the print statements
    print(url)
    code = response.status_code
    if code != 200:
        print("Error: " + str(code))
    else:
        print("200.  We're in")
    if code == 429:
        print("Error: Too many requests, retry after:")
        print(str(int(response.headers["Retry-After"]) / 60) + " minutes")
    time.sleep(random.random() * 5 + 5)


#Create an class type Soccer League
class SoccerLeague:
    def constants(self, teams):
        self.stats_wanted = team_stats_wanted
        for key in self.stats_wanted.copy():
            self.stats_wanted[key + " Against"] = [stat for stat in self.stats_wanted[key]]
        self.year = year
        self.list_teams = teams

        test_print(self.stats_wanted, 2)


    def __init__(self, url, teams):
        self.constants(teams)

        self.url = url
        self.response = requests.get(url, headers={'User-Agent': 'Safari/537.36'})
        requests_test(self.response, self.url)
        self.soup = bs(self.response.content, "html.parser")

        self.tables = self.gen_tables() #creates a dictionary of tables, with the key being the table name
        test_print(["Tables: ", self.tables.keys(), len(self.tables)], 2)
        self.table = self.gen_table()

        self.league = url.split("/")[-1][:url.split("/")[-1].index("-Stats")].replace("-", " ")
        self.team_objs = self.gen_teams()
        test_print(["team objs", self.team_objs], 2)
        self.team_names = [unidecode(team.text.strip()) for team in self.team_objs]
        test_print(["team names", self.team_names], 2)
        self.team_links = [team.a["href"] for team in self.team_objs]
        
        self.team_stats = self.gen_team_stats()
        #self.relativize_team_stats()

        if self.list_teams == None:
            self.list_teams = range(len(self.team_names))
        
        self.teams = [SoccerTeam("https://fbref.com" + self.team_objs[team].a["href"], self.team_stats[team], self.league) for team in self.list_teams] #TODO: change back once Arsenal glitch is gone
        self.save_stats()

    def gen_tables(self):
        ans = {}
        for caption in self.soup.find_all("caption"):
            key = caption.get_text().split(":")[0].split(" " + self.year)[0].split(" Table")[0]
            key += (" Against" if key in ans else "")
            ans[key] = caption.find_parent('table', {'class': 'stats_table'})
        return ans
        
        # return {table.get_text().split(":")[0] : table.find_parent('table', {'class': 'stats_table'}) for table in self.soup.find_all("caption")}

    def gen_table(self):
        return self.tables['Squad Standard Stats']
    
    # given the table in self.table, generate the teams in the league
    # TEST_NUMBER = 20
    def gen_teams(self):
        teams = []
        for row in self.table.find_all("tr"):
            # test_print(row, 20)
            for col in row.find_all("td")+row.find_all("th"):
                # test_print(col, 20)
                if col.get("data-stat") == "team":
                    # exclude the squad header
                    if "Squad" in col.get_text():
                        continue
                    teams.append(col)
        return teams


    def __str__(self):
        return self.league

    def __repr__(self):
        return self.league

    def get_teams(self):
        return self.team_names

    def get_team_links(self):
        return self.team_links
    
    def get_team_objs(self):
        return self.teams

    def get_team_stats(self):
        return self.team_stats

    def get_league(self):
        return self.league

    def get_table(self):
        return self.table

    def get_soup(self):
        return self.soup

    def get_response(self):
        return self.response

    def get_url(self):
        return self.url
    
    def save_stats(self):
        self.save_league_stats()
        self.save_player_stats()
        # self.save_last_five_stats()
        self.save_player_matchlogs()

    def save_league_stats(self):
        with open(self.league.replace(" ", "_") + "_Team_Stats.csv", "w") as csvfile:
            # creating a csv dict writer object
            writer = csv.DictWriter(csvfile, fieldnames=self.team_stats[0].keys())
            # writing headers (field names)
            writer.writeheader()
            # writing data rows
            writer.writerows(self.team_stats)

    
    def save_player_stats(self):
        league_stats = []
        for team in self.teams:
            for player in team.player_objs:
                league_stats.append(player.get_stats())

        with open(self.league.replace(" ", "_") + "_Player_Stats.csv", "w") as csvfile:
            # creating a csv dict writer object
            writer = csv.DictWriter(csvfile, fieldnames=get_stats_wanted("fbref"))
            # writing headers (field names)
            writer.writeheader()
            # writing data rows
            writer.writerows(league_stats)

    def save_last_five_stats(self):
        league_stats = []
        for team in self.teams:
            for player in team.player_objs:
                dict = {}
                for stat in player.l5_table.keys():
                    dict["L5_" + stat] = player.l5_table[stat]
                league_stats.append(player.l5_table)

        with open(self.league.replace(" ", "_") + "_Last_Five_Stats.csv", "w") as csvfile:
            # creating a csv dict writer object
            writer = csv.DictWriter(csvfile, fieldnames=league_stats[0].keys())
            # writing headers (field names)
            writer.writeheader()
            # writing data rows
            writer.writerows(league_stats)

    def save_player_matchlogs(self):
        folder_name = self.league.replace(" ", "_") + "_Player_Matchlogs"
        try:
            os.mkdir(folder_name)
        except FileExistsError:
            pass
        for team in self.teams:
            for player in team.player_objs:
                with open(folder_name + "/" + player.player.replace(" ", "_") + "_Matchlogs.csv", "w") as csvfile:
                    # creating a csv dict writer object
                    writer = csv.DictWriter(csvfile, fieldnames=player.matchlogs[0].keys())
                    # writing headers (field names)
                    writer.writeheader()
                    # writing data rows
                    writer.writerows(player.matchlogs)


    def gen_team_stats(self):
        team_stats_index_map = {}
        team_stats = []
        dex = 0
        for team in self.team_names: #creates the entire array of dicts, with zero values, so that we can map by index rather than checking for team name
            team_stats.append({"name": team.strip()})
            team_stats_index_map[team] = len(team_stats) - 1
            team_stats_index_map["vs " + team] = len(team_stats) - 1

        test_print(team_stats, 1)
        test_print(team_stats_index_map, 1)
        
        stats_wanted = list(self.stats_wanted.keys())
        self.totals = {}
        for stat in get_stats_wanted('fbref'):
            test_print(stat, 1)
            self.totals[stat] = 0
            self.totals[stat + "_against"] = 0
        for table in self.tables:
            if table not in stats_wanted:
                continue
            stats_wanted.remove(table)
            # Find the row that corresponds to the most recent season
            for row in self.tables[table].find_all("tr"):
                # Find the column that corresponds to the stats we want
                for header in row.find_all("th"):
                    if header.get("data-stat") == "team":
                        team = header.get_text()
                        test_print(team, 1)
                        dex = team_stats_index_map[team] if team in team_stats_index_map else dex
                        test_print(dex, 1)
                for col in row.find_all("td"):
                    if col.get("data-stat") in self.stats_wanted[table]:
                        if "Against" in table:
                            team_stats[dex][col.get("data-stat") + "_against"] = int(col.get_text().replace(",", ""))
                            self.totals[col.get("data-stat") + "_against"] += int(col.get_text().replace(",", ""))
                        else:
                            team_stats[dex][col.get("data-stat")] = int(col.get_text().replace(",", ""))
                            self.totals[col.get("data-stat")] += int(col.get_text().replace(",", ""))

        test_print("Team Stats: " + str(team_stats), 2)
        return team_stats
    
    def relativize_team_stats(self):
        for team in self.team_stats:
            for stat in team:
                if stat in ["name", "team"]:
                    continue
                if "against" in stat:
                    team[stat] = team[stat] * len(self.team_stats) / self.totals[stat]
                else:
                    team[stat] = team[stat] * len(self.team_stats) / self.totals[stat + "_against"]
        return None


class SoccerTeam():
    def constants(self):
        self.stats_wanted = team_stats_wanted
        self.player_stats_wanted = stats_wanted
        self.year = year


    def __init__(self, url, stats, league):
        self.constants()
        self.url = url
        self.stats = stats
        self.response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        requests_test(self.response, self.url)
        self.soup = bs(self.response.content, "html.parser")
        self.tables = self.gen_tables()
        self.table = self.gen_table()
        self.team = url.split("/")[-1][:url.split("/")[-1].index("-Stats")].replace("-", " ")
        self.players = self.gen_players()
        self.player_names = [unidecode(player.text) for player in self.players]
        self.player_links = [player.a["href"] for player in self.players]
        self.player_stats = self.gen_player_stats()
        self.player_objs = [SoccerPlayer("https://fbref.com" + self.players[player].a["href"], self.player_stats[player], self.team, league, False) for player in range(min(PLAYERS_PER_TEAM ,len(self.players)))]
        

    def gen_table(self):
        test_print(self.tables.keys(), 3)
        return self.tables['Standard Stats']
    
    def gen_tables(self):
        return {table.get_text().split(":")[0].split(year)[0].strip(): table.find_parent('table', {'class': 'stats_table'}) for table in self.soup.find_all("caption")}
    
    def gen_players(self):
        players = []
        nonplayers = ["Player", "Squad Total", "Opponent Total", "On-Off"]
        for row in self.table.find_all("tr"):
            for col in row.find_all("th"):
                if col.get("data-stat") == "player" and col.text not in nonplayers:
                    players.append(col)
        return players

    def players_test(self, players):
        for player in players:
            if player.a is None:
                print("No link found for player: " + player.text)
        return None

    def __str__(self):
        return self.team

    def __repr__(self):
        return self.team

    def get_players(self):
        return self.player_names

    def get_player_links(self):
        return self.player_links

    def get_player_stats(self):
        return self.player_stats

    def get_team(self):
        return self.team

    def get_table(self):
        return self.table

    def get_soup(self):
        return self.soup

    def get_response(self):
        return self.response

    def get_url(self):
        return self.url

    def gen_player_stats(self):
        player_stats_index_map = {}
        player_stats = []
        dex = 0
        for player in self.player_names:
            player_stats.append({"name": player.strip(), "team": self.team})
            player_stats_index_map[player] = len(player_stats) - 1


        test_print(player_stats, 4)
        test_print(player_stats_index_map, 4)

        stats_wanted = list(self.player_stats_wanted.keys())
        test_print(stats_wanted, 3)
        for table in self.tables:
            test_print(table, 3)
            if table not in stats_wanted:
                continue
            stats_wanted.remove(table)
            test_print(table, 3)
            # Find the row that corresponds to the most recent season
            for row in self.tables[table].find_all("tr"):
                test_print("row", 3)
                # Find the column that corresponds to the stats we want
                for header in row.find_all("th"):
                    if header.get("data-stat") == "player":
                        player = unidecode(header.get_text())
                        test_print(player, 3)
                        dex = player_stats_index_map[player] if player in player_stats_index_map else -1
                        test_print(dex, 3)
                if dex == -1:
                    continue
                for col in row.find_all("td"):
                    if col.get("data-stat") in self.player_stats_wanted[table]:
                        player_stats[dex][col.get("data-stat")] = int(col.get_text().replace(",", "")) if col.get_text() != "" else 0

        test_print("player Stats: " + str(player_stats), 3)
        return player_stats

class SoccerPlayer():
    def constants(self):
        self.stats_wanted = get_stats_wanted("fbref") + ["game_started"]
        self.matchlog_stats = ['dayofweek', 'comp', 'round', 'venue', 'result', 'team', 'opponent', 'game_started', 'position', 'minutes', 'goals', 'assists', 'pens_made', 'pens_att', 'shots', 'shots_on_target', 'cards_yellow', 'cards_red', 'touches', 'tackles', 'interceptions', 'blocks', 'xg', 'npxg', 'xg_assist', 'sca', 'gca', 'passes_completed', 'passes', 'passes_pct', 'progressive_passes', 'carries', 'progressive_carries', 'take_ons', 'take_ons_won', 'match_report']
        self.year = year

    #TEST_NUMBER = 11
    def __init__(self, url, stats, team, league, scrape=True, matchlog=True):
        self.constants()
        self.url = url
        self.player = url.split("/")[-1].replace("-", " ")
        test_print(self.player, 11)
        self.stats = stats
        self.team = team
        self.league = league    
        if scrape:
            self.response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
            requests_test(self.response, self.url)
            self.soup = bs(self.response.content, "html.parser")
            self.tables = self.gen_tables()
            self.player = url.split("/")[-1].replace("-", " ")
            self.stats = self.gen_stats()
        if matchlog:
            self.matchlog_table = self.get_matchlog_table() #this just gets us the HMTL code
            # test_print(self.matchlog_table, 10)
            # self.l5_table = self.gen_l5_table()
            self.matchlogs = self.gen_matchlogs()
            test_print(self.matchlogs, 10)



    def gen_tables(self):
        return {table.get_text().split(":")[0]: table.find_parent('table', {'class': 'stats_table'}) for table in self.soup.find_all("caption")}
    
    def show_tables(self):
        print(len(self.tables))
        for table in self.tables:
            print(table)
            print("--------------------")

    def gen_stats(self):
        stats = {"name": self.player}
        stats_wanted = self.stats_wanted.copy()
        for table in self.tables:
            if table not in stats_wanted:
                continue
            stats_wanted.remove(table)
            # Find the row that corresponds to the most recent season
            for row in self.tables[table].find_all("tr"):
                if self.year in row.get_text():
                    # Find the column that corresponds to the stats we want
                    for col in row.find_all("td"):
                        if col.get("data-stat") in self.stats_wanted[table]:
                            stats[col.get("data-stat")] = int(col.get_text().replace(",", ""))

        # If we didn't find the stats we wanted, add them to the dict with a value of 0
        for table in stats_wanted:
            for stat in self.stats_wanted[table]:
                stats[stat] = 0

                            

        test_print("Stats: " + str(stats), 4)
        return stats
    
    def __str__(self):
        return self.player

    def __repr__(self):
        return self.player

    def get_stats(self):
        return self.stats

    def get_player(self):
        return self.player

    def get_tables(self):
        return self.tables

    def get_soup(self):
        return self.soup

    def get_response(self):
        return self.response

    def get_url(self):
        return self.url

    def get_stat(self, stat_name):
        stat_index = self.stats.index(stat_name)
        stat = self.stats[stat_index]
        return stat

    def get_stat_soup(self, stat_name):
        stat_index = self.stats.index(stat_name)
        stat_link = stat_name.a["href"]
        stat_url = "https://fbref.com" + stat_link
        stat_response = requests.get(stat_url)
        stat_soup = bs(stat_response.content, "html.parser")
        return stat_soup

    def get_stat_response(self, stat_name):
        stat_index = self.stats.index(stat_name)
        stat_link = stat_name.a["href"]
        stat_url = "https://fbref.com" + stat_link
        stat_response = requests.get(stat_url)
        return stat_response


    # TODO: Find a way to encorporate the passing table so that kp's can be included in analysis, as well as clearances
    # TEST_NUMBER = 5
    def get_matchlog_table(self):
        #add matchlog/ right before the last / in self.url
        matchlog_url = self.url[:self.url.rfind("/")] + "/matchlogs/2023-2024/" + self.url[self.url.rfind("/") + 1:] + "-Match-Logs"
        stat_response = requests.get(matchlog_url)
        requests_test(stat_response, matchlog_url)
        stat_soup = bs(stat_response.content, "html.parser")
        for table in stat_soup.find_all("caption"):
            test_print(table.get_text(), 5)
            if ("Match Logs" in table.get_text()):
                return table.find_parent('table', {'class': 'stats_table'})
        print("No matchlog table found for " + self.player)
        return None

    
    def gen_l5_table(self):
        last_five_games_totals = {"name": self.player, "team": self.team, "league": self.league}
        for stat in self.stats_wanted:
            if stat in ["name", "team"]:
                continue
            last_five_games_totals[stat] = 0
        if self.matchlog_table is None:
            return last_five_games_totals
        games = 5
        for row in self.matchlog_table.find_all("tr"):
            if games == 0:
                break
            for col in row.find_all("td"):
                if col.get("data-stat") == "team" and col.get_text() != self.team:
                    break
                if col.get("data-stat") == "game_started" and col.get_text() in ["Y", "Y*"]:
                    games -= 1
                if col.get("data-stat") in last_five_games_totals.keys():
                    if col.get("data-stat") in ["name", "team", "league"]:
                        continue

                    test_print(col.get("data-stat") + ": " + col.get_text(), 5)
                    last_five_games_totals[col.get("data-stat")] += int(col.get_text().replace(",", "")) if col.get_text().isdigit() else 0

        last_five_games_totals["games"] = 5 - games #The variable is a countdown hence the subtraction

        test_print("Last 5 games totals for :" + self.url[self.url.rfind("/") + 1:] + str(last_five_games_totals), 5)
        return last_five_games_totals
    
    # given the html for the matchlogs (self.matchlog_table), generate the relevant matchlogs in dictionary form
    # TEST_NUMBER = 12
    def gen_matchlogs(self):
        matchlogs = []
        player_game_count = 1
        games = self.matchlog_table.find_all("tr")

        for row in games:
            matchlog = self.gen_matchlog(row, player_game_count)
            if matchlog is not None:
                player_game_count += 1
                matchlogs.append(matchlog)

        test_print([matchlogs, len(matchlogs)], 12)
        return matchlogs

    # given a row in the matchlog table, generate the relevant matchlog in dictionary form
    # note: we seperated the functions so that we can return None, rather than dealing with breaking out of a nested loop
    # TEST_NUMBER = 13
    def gen_matchlog(self, row, player_game_count):
        # can be adjusted as needed
        # TEST_NUMBER = 14
        def is_valid_matchlog(row):
            # test_print(["row", row.get("class")], 14)

            # in theory, gets rid of the rows that aren't games, including rows from browser view (benched games)
            if row.get("class") != None:
                # test_print("False", 14)
                return False
            
            ans = False
            for col in row.find_all("td"):
                # automatically returns false for internatinonal games
                if col.get("data-stat") == "team" and col.get_text() != self.team:
                    return False
                # automatically return false for games out of league (ie FA Cup)
                if col.get("data-stat") == "comp" and col.get_text() != self.league:
                    test_print([col.get_text(), self.league], 14)
                    return False
                # if the day of the week is valid, then the matchlog is valid, if not then will return false
                if col.get("data-stat") == "dayofweek" and col.get_text() in ["Sat", "Sun", "Mon", "Tue", "Wed", "Thu", "Fri"]:
                    ans = True
            return ans
        
        # test_print(row, 13)
        if not is_valid_matchlog(row):
            return None
        # test_print(row, 13)

        # creates a new dictionary with empty values, to be replaced
        matchlog = {
            "game_started": "N",
            "game_count": player_game_count,
        }

        # for stat in self.stats_wanted:
        #     if stat in ["name", "team"]:
        #         continue
        #     matchlog[stat] = 0

        # TODO: we must encorporate fouls, fouled, clearances, and key passes
        for col in row.find_all("td"):
            # test_print(["col", col], 13)
            if col.get("data-stat") in self.matchlog_stats:
                if col.get("data-stat") == "game_started" and col.get_text() in ["Y", "Y*"]:
                    matchlog["game_started"] = "Y"
                elif col.get("data-stat") == "result":
                    matchlog["result"] = unidecode(col.get_text())
                else:
                    matchlog[col.get("data-stat")] = int(col.get_text().replace(",", "")) if col.get_text().isdigit() else col.get_text()

        test_print(matchlog, 13)
        return matchlog


# # Create an instance of the SoccerLeague class
# premier_league = SoccerLeague(premier_league_url)
# premier_league.save_league_stats()




import requests
from bs4 import BeautifulSoup as bs
import time, random, csv
from unidecode import unidecode
from constants import *

def test_print(response, x):
    to_test = [3]
    if x in to_test:
        print(response)


# Make sure we bypass 429 and wait a reasonable amount of time between reqs
def code_test(response):
    code = response.status_code
    if code != 200:
        print("Error: " + str(code))
    else:
        print("200.  We're in")
    if code == 429:
        print("Error: Too many requests, retry after:")
        print(str(int(response.headers["Retry-After"]) / 60) + " minutes")
    time.sleep(random.random() * 1.5 + 0.75)


#Create an class type Soccer League
class SoccerLeague:
    def constants(self):
        self.stats_wanted = team_stats_wanted
        for key in self.stats_wanted.copy():
            self.stats_wanted[key + " Against"] = [stat for stat in self.stats_wanted[key]]
        self.year = year

        test_print(self.stats_wanted, 2)


    def __init__(self, url):
        self.constants()
        self.url = url
        self.response = requests.get(url, headers={'User-Agent': 'Safari/537.36'})
        code_test(self.response)
        self.soup = bs(self.response.content, "html.parser")
        self.tables = self.gen_tables()
        # test_print("Tables: ", self.tables.keys(), len(self.tables), 2)
        self.table = self.gen_table()
        self.league = url.split("/")[-1][:url.split("/")[-1].index("-Stats")].replace("-", " ")
        self.team_objs = self.gen_teams()
        self.team_names = [unidecode(team.text.strip()) for team in self.team_objs]
        self.team_links = [team.a["href"] for team in self.team_objs]
        self.team_stats = self.gen_team_stats()
        self.teams = [SoccerTeam("https://fbref.com" + self.team_objs[team].a["href"], self.team_stats[team]) for team in range(len(self.team_objs))]
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
        return self.tables['Regular season']
    
    def gen_teams(self):
        teams = []
        for row in self.table.find_all("tr"):
            for col in row.find_all("td"):
                if col.get("data-stat") == "team":
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

    def gen_team_stats(self):
        team_stats_index_map = {}
        team_stats = []
        dex = 0
        for team in self.team_names:
            team_stats.append({"name": team.strip()})
            team_stats_index_map[team] = len(team_stats) - 1
            team_stats_index_map["vs " + team] = len(team_stats) - 1

        test_print(team_stats, 1)
        test_print(team_stats_index_map, 1)
        
        stats_wanted = list(self.stats_wanted.keys())
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
                        else:
                            team_stats[dex][col.get("data-stat")] = int(col.get_text().replace(",", ""))

        test_print("Team Stats: " + str(team_stats), 2)
        return team_stats


class SoccerTeam():
    def constants(self):
        self.stats_wanted = team_stats_wanted
        self.player_stats_wanted = stats_wanted
        self.year = year


    def __init__(self, url, stats):
        self.constants()
        self.url = url
        self.stats = stats
        self.response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        code_test(self.response)
        self.soup = bs(self.response.content, "html.parser")
        self.tables = self.gen_tables()
        self.table = self.gen_table()
        self.team = url.split("/")[-1][:url.split("/")[-1].index("-Stats")].replace("-", " ")
        self.players = self.gen_players()
        self.player_names = [unidecode(player.text) for player in self.players]
        self.player_links = [player.a["href"] for player in self.players]
        self.player_stats = self.gen_player_stats()
        self.player_objs = [SoccerPlayer("https://fbref.com" + self.players[player].a["href"], self.player_stats[player], False) for player in range(len(self.players))]
        

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
            player_stats.append({"name": player.strip()})
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
        self.stats_wanted = stats_wanted
        self.year = year


    def __init__(self, url, stats, scrape=True):
        self.constants()
        self.url = url
        self.stats = stats
        if scrape:
            self.response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
            code_test(self.response)
            self.soup = bs(self.response.content, "html.parser")
            self.tables = self.gen_tables()
            self.player = url.split("/")[-1].replace("-", " ")
            self.stats = self.gen_stats()

    def gen_tables(self):
        return {table.get_text().split(":")[0]: table.find_parent('table', {'class': 'stats_table'}) for table in self.soup.find_all("caption")}
    
    def show_tables(self):
        print(len(self.tables))
        for table in self.tables:
            print(table)
            print("--------------------")

    def gen_stats(self):
        stats = {"name": self.player}
        stats_wanted = list(self.stats_wanted.keys())
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

                            

        print("Stats: ", stats)
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

    def get_stat_table(self, stat_name):
        stat_index = self.stats.index(stat_name)
        stat_link = stat_name.a["href"]
        stat_url = "https://fbref.com" + stat_link
        stat_response = requests.get(stat_url)
        stat_soup = bs(stat_response.content, "html.parser")


# Create an instance of the SoccerLeague class
premier_league = SoccerLeague(premier_league_url)
premier_league.save_league_stats()




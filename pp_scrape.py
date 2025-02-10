from curl_cffi import requests
import json, csv
from unidecode import unidecode
from constants import *


def check(s):
    print(type(s)   )
    print(s[:1000] + '...' + s[-1000:])

def print_a_player(players):
    for key in players:
        print(players[key])
        return
    
def is_multiple_players(player):
    return player.find("+") != -1

def get_data_scrape():
    # Set up Selenium webdriver
    driver = webdriver.Chrome()

    # Navigate to the URL
    url = "https://api.prizepicks.com/projections"
    driver.get(url)

    # Get the page source
    page_source = driver.page_source
    # Get the part of the string from the first { to the last }
    jsonified = page_source[page_source.find('{'):page_source.rfind('}')+1]

    #now turn it into a json object
    driver.quit()
    return json.loads(jsonified)

def get_data_scrape_cffi():
    url = "https://api.prizepicks.com/projections"
    response = requests.get(url, impersonate="safari_ios")
    return response.json()

# Save data to a file
def save_data_file(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f)

# Load data from a file
def get_data_file(filename):
    with open(filename, 'r') as f:
        return json.load(f)
    
def is_sport(datapoint, sport_id = "82"):
    soccer_id = "82"
    if ("attributes") not in datapoint.keys():
        return False
    if ("league_id" in datapoint["attributes"].keys()):
        return str(datapoint["attributes"]["league_id"]) == sport_id
    if ("relationships") in datapoint.keys():
        return str(datapoint["relationships"]["league"]["data"]["id"]) == sport_id
    return False

# Get the data
def get_data(sport_id = "82"):
    data = get_data_scrape_cffi()
    # data = get_data_file("pp_sample_web_data.json")

    # Sort the data into relevant lists, depending on category
    players = {}
    lines = {}

    # Get the players by their id number
    for inc in data["included"]:
        if inc["type"] == "new_player":
            if is_sport(inc, sport_id):
                players[inc["id"]] = inc

    # print(len(players), len(lines))
    # print_a_player(players)

    # Get the lines, and save them to a dictionary with player names as keys
    for datapoint in data["data"]:
        if "type" in datapoint.keys():
            if datapoint["type"] == "projection":
                if is_sport(datapoint, sport_id):
                    if "odds_type" in datapoint["attributes"].keys():
                        if datapoint["attributes"]["odds_type"] != "standard": # do not want goblin/demon lines
                            continue
                    player_id = datapoint["relationships"]["new_player"]["data"]["id"]
                    if player_id in players.keys():
                        player_name = unidecode(players[player_id]["attributes"]["display_name"])
                        lines[player_name] = [datapoint] if player_name not in lines.keys() else lines[player_name] + [datapoint]

    final_csv = list()
    stat_types = list()
    for player in lines:
        if is_multiple_players(player):
            continue
        dic = {'name': player}
        for line in lines[player]:
            if "attributes" in line.keys():
                # GOAL: add the opponent to the dictionary
                print(line["attributes"].keys())
                print(line["attributes"])
                if "description" in line["attributes"].keys():
                    dic["opponent"] = unidecode(line["attributes"]["description"])

                if "stat_type" in line["attributes"].keys():
                    dic[line["attributes"]["stat_type"]] = line["attributes"]["line_score"]
                    stat_types = stat_types + [line["attributes"]["stat_type"]] if line["attributes"]["stat_type"] not in stat_types else stat_types
        final_csv.append(dic)

    with open("pp_lines.csv", "w") as f:
        writer = csv.DictWriter(f, fieldnames=["name", "opponent"] + stat_types)
        writer.writeheader()
        writer.writerows(final_csv)

    return final_csv

get_data()


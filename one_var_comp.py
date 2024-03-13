import json, csv
import pandas as pd

# Load data from files
def get_data_file(filename):
    with open(filename) as f:
        return json.load(f)
    
def get_data_csv(filename):
    with open(filename, "r") as f:
        return [row for row in csv.reader(f)]

players = pd.read_csv("Premier_League_Player_Stats.csv")
lines = pd.read_csv("pp_lines.csv")

merged = pd.merge(players, lines, on="name")

print(merged.head())







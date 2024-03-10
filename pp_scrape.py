from selenium import webdriver
import json

def check(s):
    print(type(s)   )
    print(s[:1000] + '...' + s[-1000:])

def print_a_player(players):
    for key in players:
        print(players[key])
        return

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

# Save data to a file
def save_data_file(data):
    with open('pp_data.json', 'w') as f:
        json.dump(data, f)

# Load data from a file
def get_data_file():
    with open('pp_data.json', 'r') as f:
        return json.load(f)

# Get the data
# data = get_data_scrape()
data = get_data_file()

# Sort the data into relevant lists, depending on category
players = {}
lines = []

for datapoint in data["data"]:
    if "type" in datapoint.keys():
        if datapoint["type"] == "projection":
            lines.append(datapoint)

for inc in data["included"]:
    if inc["type"] == "new_player":
        print("new player")
        players[inc["id"]] = inc

print(len(players), len(lines))
print_a_player(players)
print(lines[0])
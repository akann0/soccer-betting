# %%
from curl_cffi import requests
import csv

draftkings_nfl_api_url = "https://sportsbook.draftkings.com//sites/US-SB/api/v5/eventgroups/88808?format=json"
draftkings_nfl_site_url = "https://sportsbook/https:.draftkings.com/leagues/football/nfl"
draftkings_cbb_api_url = "https://sportsbook.draftkings.com//sites/US-SB/api/v5/eventgroups/92483?format=json"
draftkings_nba_api_url = "https://sportsbook.draftkings.com//sites/US-SB/api/v5/eventgroups/42648?format=json"

# %%
# Code to help find the api - do not run
def find_access_code_in_server():
    response = requests.get(draftkings_nfl_site_url, headers={"User-Agent": "Mozilla/5.0"})
    if ("88808" in response.text):
        print("Found the event group id on the site")
        index_found = response.text.find("88808")
        print(response.text[index_found-500:index_found+500])
    else:
        print("Did not find the event group id on the site")
        print(response.text)

# %%
# put a request into the url
def get_draftkings_cbb_data():
    response = requests.get(draftkings_cbb_api_url, headers={"User-Agent": "Mozilla/5.0"})

    json = response.json()
    json['eventGroup'].keys()

    # %%


    # %%
    category_urls = {}
    cat_names = {}
    for event in json['eventGroup']['offerCategories']:
        print(event['offerCategoryId'], event['name'])
        category_urls[event['offerCategoryId']] = "https://sportsbook.draftkings.com//sites/US-SB/api/v5/eventgroups/92483/categories/" + str(event['offerCategoryId']) + "?format=json"
        cat_names[event['offerCategoryId']] = event['name']

    print(category_urls)

    # %%
    url = "https://sportsbook.draftkings.com//sites/US-SB/api/v5/eventgroups/92483/categories/1218?format=json"
    print(url)

    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    json = response.json()

    # %%
    csv_data = []

    for cat_id in category_urls:
        response = requests.get(category_urls[cat_id], headers={"User-Agent": "Mozilla/5.0"})
        json = response.json()

        for category in json['eventGroup']['offerCategories']:
            if 'offerSubcategoryDescriptors' in category.keys():
                for offer in category['offerSubcategoryDescriptors'][0]['offerSubcategory']['offers']:
                    for i in offer:
                        for outcome in i['outcomes']:
                            dict = outcome
                            dict['category'] = cat_names[cat_id]
                            if 'label' in i.keys():
                                dict['prop_label'] = i['label']
                            else:
                                print(i)
                                continue
                            csv_data.append(dict)

    # %%
    # turn the data in csv_data into a csv file
    import csv

    with open('draftkings_cbb.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(csv_data[0].keys())
        for row in csv_data:
            writer.writerow(row.values())

# %%

# %%

def get_draftkings_nba_data():
    print("Getting DraftKings NBA data")
    try:
       response = requests.get(draftkings_nba_api_url, impersonate="safari_ios")
       response.raise_for_status()  # Raise an exception for bad status codes
    except requests.exceptions.Timeout:
       print("Request timed out")
    except requests.exceptions.RequestException as e:
       print(f"An error occurred: {e}")
    print(response)

    json = response.json()
    json['eventGroup'].keys()

    category_urls = {}
    cat_names = {}
    for event in json['eventGroup']['offerCategories']:
        print(event['offerCategoryId'], event['name'])
        category_urls[event['offerCategoryId']] = "https://sportsbook.draftkings.com//sites/US-SB/api/v5/eventgroups/42648/categories/" + str(event['offerCategoryId']) + "?format=json"
        cat_names[event['offerCategoryId']] = event['name']

    print(category_urls)

    url = "https://sportsbook.draftkings.com//sites/US-SB/api/v5/eventgroups/42648/categories/1218?format=json"
    print(url)

    response = requests.get(url, impersonate="safari_ios")
    json = response.json()
    print(json.keys())

    csv_data = []

    for cat_id in category_urls:
        if cat_id == 1206:
            continue
        response = requests.get(category_urls[cat_id], impersonate="safari_ios")
        json = response.json()

        for category in json['eventGroup']['offerCategories']:
            if 'offerSubcategoryDescriptors' in category.keys():
                for offer in category['offerSubcategoryDescriptors'][0]['offerSubcategory']['offers']:
                    for i in offer:
                        for outcome in i['outcomes']:
                            dict = outcome
                            dict['category'] = cat_names[cat_id]
                            if 'label' in i.keys():
                                dict['prop_label'] = i['label']
                            else:
                                print(i)
                                continue
                            csv_data.append(dict)

    # turn the data in csv_data into a csv file

    with open('draftkings_nba.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(csv_data[0].keys())
        for row in csv_data:
            writer.writerow(row.values())

# %%
get_draftkings_nba_data()


import json


def find_route(data, route_no):
    return list(filter(lambda x: x.get('rounteNo') == route_no, data))

def save_discord_id(Team_ID,Discord_ID):
    '''Saves the teams discord ID to the database.'''
    #Opens the file to save to local database.
    with open('data.json') as json_file:
          data = json.load(json_file)
    #Searches for index that has the same key value as wanted.
    location = next((index for (index, d) in enumerate(data["Teams"]) if d["Team_ID"] == Team_ID), None)
    teams = data['Teams']

    #Checks if team exists, if not adds to list otherwise will add to existing teams discord ID's.
    if location == None:
        teams.append({'Team_ID':Team_ID,"Discord_IDs":[Discord_ID]})
    else:
        if Discord_ID in teams[location]["Discord_IDs"]:
            pass
        else:
            teams[location]["Discord_IDs"].append(Discord_ID)

    new_data = {"Teams":teams}
    #Saves the database to file.
    with open('data.json', 'w') as f:
        json.dump(new_data, f)

def get_discord_ids(Team_ID):
    '''Returns a list of discord ID's for a given Team ID'''
    #Opens the file to save to local database.
    with open('data.json') as json_file:
          data = json.load(json_file)
    #Searches for index that has the same key value as wanted.
    location = next((index for (index, d) in enumerate(data["Teams"]) if d["Team_ID"] == Team_ID), None)
    
    #Makes sure location isn't empty.
    if location == None:
        return None
    #Extracts discord users.
    Discord_IDs=data["Teams"][location]["Discord_IDs"]
    #Returns the users.
    return Discord_IDs




save_discord_id("324",2323)
print(get_discord_ids("26222599-9b15-474a-b6cd-e421d827fdca"))
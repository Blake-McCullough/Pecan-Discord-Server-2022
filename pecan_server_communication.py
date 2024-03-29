import os
import requests
from dotenv import load_dotenv





def get_current_team_score(Team_ID):
    '''Returns the given team_ids score.'''
 
    url = "https://ctf.pecan.tplant.com.au/api/v1/users/"+Team_ID

    response = requests.request("GET", url)
    if response.status_code == 200:
        data = response.json()
        score = data["data"]["score"]
        return score
    else:
        print('Team score error' +str(response.status_code))


def get_teamname_by_id(team_id):
    '''Gets the username from a team name.'''
    url = "https://ctf.pecan.tplant.com.au/api/v1/users/"+team_id

    response = requests.request("GET", url)

    if response.status_code == 200:
        data = response.json()

        name = data["data"]["name"]
        return name
    else:
        print('Team ID error ' +str(response.status_code))
        return None

def get_division_by_id(team_id):
    '''Gets the team skill level via the ID'''
    url = "https://ctf.pecan.tplant.com.au/api/v1/users/"+team_id

    response = requests.request("GET", url)

    if response.status_code == 200:
        data = response.json()

        name = data["data"]["division"]
        return name
    else:
        print('division ID error ' +str(response.status_code))
        return None

def get_challenges():
    '''Fetches challenges from the server'''

    url = "https://ctf.pecan.tplant.com.au/api/v1/challs"

    headers = {
        'authorization': "Bearer "+os.getenv('SERVER_TOKEN'),
        }

    response = requests.request("GET", url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        results = data['data']
        return results 
    else:
        print('Challenges error' +str(response.status_code))


def get_leaderboard(limit):
    '''Returns a list of the leaderboard for games (Limit is the maximum amount of users for the system to return)'''
    url = "https://ctf.pecan.tplant.com.au/api/v1/leaderboard/now?offset=0&limit="+str(limit)



    response = requests.request("GET", url)
    
    if response.status_code == 200:
        data = response.json()
        results = data['data']['leaderboard']
        return results
    else:
        print('Leaderboard error' +str(response.status_code)) 


if __name__ == "__main__":
   
    load_dotenv()
    get_challenges()
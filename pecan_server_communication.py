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



def get_leaderboard():
    '''Returns a list with the leaderboard.'''

    url = " https://ctf.pecan.tplant.com.au/api/v1/leaderboard/now?offset=0&limit=10"

    response = requests.request("GET", url)
    if response.status_code == 200:
        data = response.json()
        leaderboard = data["data"]["leaderboard"]
        return leaderboard

def get_challenges():


    url = "https://ctf.pecan.tplant.com.au/api/v1/challs"

    headers = {
        'authorization': "Bearer "+os.getenv('SERVER_TOKEN'),
        }

    response = requests.request("GET", url, headers=headers)
    print(response.status_code)
    if response.status_code == 200:
        data = response.json()
        results = data['data']
        print(results)
        return results 
def get_leaderboard(limit):
    
    url = "https://ctf.pecan.tplant.com.au/api/v1/leaderboard/now?offset=0&limit="+str(limit)



    response = requests.request("GET", url)
    print(response.status_code)
    if response.status_code == 200:
        data = response.json()
        results = data['data']['leaderboard']
        print(results)
        return results 


if __name__ == "__main__":
   
    load_dotenv()
    get_challenges()
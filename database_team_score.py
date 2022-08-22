import requests
def get_current_team_score(Team_ID):

    
 
    url = "https://ctf.pecan.tplant.com.au/api/v1/users/"+Team_ID


    response = requests.request("GET", url)
    if response.status_code == 200:
        data = response.json()
        score = data["data"]["score"]
        return score
import requests
import os
def exchange_code(code):
  data = {
    'client_id': os.getenv("CLIENT_ID"),
    'client_secret': os.getenv("CLIENT_SECRET"),
    'grant_type': 'authorization_code',
    'code': code,
    'redirect_uri': os.getenv("REDIRECT_URI")
  }
  headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
  }
  r = requests.post(url='https://discord.com/api/v10/oauth2/token', data=data, headers=headers)
  r.raise_for_status()
  data = r.json()
  return data['access_token']

def get_user_id(token):

    headers = {
        'Authorization': 'Bearer ' + token
    }
    r = requests.get(url='https://discord.com/api/v10/users/@me',  headers=headers)
    r.raise_for_status()
    data = r.json()
    return data['id']


def join_discord(token,userid):
    import requests

    url = "https://discord.com/api/v10/guilds/"+os.getenv("GUILD_ID")+"/members/"+str(userid)

    payload = '{\"access_token\": \"'+str(token)+'\"}'
    headers = {
        'authorization': "Bot MTAxMjU3MDQzMDI5MDI3MjI2Ng.GlaT7p.t-LbWH1AwL32nZou8K3NvV1c6hf0DVanqeGfyk",
        'content-type': "application/json",
        'cache-control': "no-cache",
        'postman-token': "2f5932cd-c30b-1dc8-e36d-dbcc70753813"
        }

    response = requests.request("PUT", url, data=payload, headers=headers)
    if response.status_code == 201:
        return True
    elif response.status_code ==204:
        return False
    else:
        return None


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


def join_discord(token,user_id):
    import requests

    url = "https://discord.com/api/v10/guilds/"+os.getenv("GUILD_ID")+"/members/"+str(user_id)

    payload = '{\"access_token\": \"'+str(token)+'\"}'
    headers = {
        'authorization': "Bot " + os.getenv("BOT_TOKEN"),
        'content-type': "application/json",


        }

    response = requests.request("PUT", url, data=payload, headers=headers)
    if response.status_code == 201:
        return True
    elif response.status_code ==204:
        return False
    else:
        return None

def get_username_by_id(user_id):
    url = "https://discord.com/api/v10/users/"+str(user_id)


    headers = {
        'authorization': "Bot " + os.getenv("BOT_TOKEN")
       
        }

    response = requests.request("GET", url,  headers=headers)
    if response.status_code == 201 or response.status_code ==200 or response.status_code ==204:
        data = response.json()
        user_name = data['username']
        tag = data['discriminator']
        user_name_tag = user_name+"#"+tag
        return user_name_tag
    else:
        return None


if __name__ == "__main__":
    get_username_by_id()
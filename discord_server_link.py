import requests
import os
from discord_webhook import DiscordWebhook

def give_user_role(Member_ID,Role_ID):
    '''Uses the discord API to give a user a role, then will return true on success, false on error.'''
    url = "https://discord.com/api/guilds/"+os.getenv("GUILD_ID")+ "/members/"+Member_ID

    payload = '{"roles":['+Role_ID+']}'
    headers = {
        'authorization': "Bot "+os.getenv('BOT_TOKEN'),
        'content-type': "application/json",
        }

    response = requests.request("PATCH", url, data=payload, headers=headers)
    if response.status_code == 204:
        return True
    else:
        return False
  

  
def send_message(message):



    response = DiscordWebhook(url=os.getenv('GAME_WEBHOOK_URL'), content=message).execute()

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    print(give_user_role(Member_ID= "107295705239986176",Role_ID = "975326545843458099"))
    send_message(message="I AM SENT")
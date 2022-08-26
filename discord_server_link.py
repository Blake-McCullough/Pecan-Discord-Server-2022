from operator import itemgetter
import requests
import os
from discord_webhook import DiscordWebhook
from dotenv import load_dotenv
from pecan_server_communication import get_challenges, get_leaderboard
from datetime import datetime,timezone


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


def edit_top_challenges_message():
    '''Edits the message of the top challenge results.'''
    url = "https://discord.com/api/channels/"+os.getenv("Graph_Channel_ID")+ "/messages/"+os.getenv("Graph_Message_ID")
    #Fetches current challenges.
    challenges = get_challenges()
    #Sorts list by 'solves' key value.
    challenges_sorted = sorted(challenges, key=itemgetter('solves'), reverse=True) 
    #Loops through list until reaches top x amount to the message.
    x = 0
    challenges_message = "__**Name: Solves **__\n\n"
    for item in challenges_sorted:
        if x >= 10:
            break
        else:
            challenges_message = challenges_message + f"**{item['name']}:** {item['solves']}\n"
        x = x+1
    #Gets current time.
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat()


    #Sends of editing message.
    payload = {
        'embeds':
        [
            {
                'title':'__**TOP COMPLETED CHALLENGES**__',
                'type':'rich',
                'description':challenges_message,
                'color':7419530,
                'timestamp':now,
                'author':
                {
                    'name':'Blake McCullough',
                    'url':'https://blakemccullough.com/'
                },
                'footer':
                {
                    'text':'Last Updated'
                }   
            }
        ]
    }
    headers = {
        'authorization': "Bot "+os.getenv('BOT_TOKEN'),
        'content-type': "application/json",
        }

    response = requests.request("PATCH", url, json=payload, headers=headers)
    print(response.status_code)
    if response.status_code == 204:
        return True
    else:
        return False

def edit_leaderboard():
    url = "https://discord.com/api/channels/"+os.getenv("LEADERBOARD_CHANNEL_ID")+ "/messages/"+os.getenv("LEADERBOARD_MESSAGE_ID")
    #Fetches current challenges.
    challenges = get_leaderboard(10)
    #Sorts list by 'solves' key value.
    challenges_sorted = sorted(challenges, key=itemgetter('score'), reverse=True) 
    #Loops through list until reaches top x amount to the message.
    x = 0
    challenges_message = "__**Name: Solves **__\n\n"
    for item in challenges_sorted:
        if x >= 10:
            break
        else:
            challenges_message = challenges_message + f"**{item['name']}:** {str(item['score'])}\n"
        x = x+1
    #Gets current time.
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat()


    #Sends of editing message.
    payload = {
        'embeds':
        [
            {
                'title':'__**TOP COMPLETED CHALLENGES**__',
                'type':'rich',
                'description':challenges_message,
                'color':7419530,
                'timestamp':now,
                'author':
                {
                    'name':'Blake McCullough',
                    'url':'https://blakemccullough.com/'
                },
                'footer':
                {
                    'text':'Last Updated'
                }   
            }
        ]
    }
    headers = {
        'authorization': "Bot "+os.getenv('BOT_TOKEN'),
        'content-type': "application/json",
        }

    response = requests.request("PATCH", url, json=payload, headers=headers)
    print(response.status_code)
    if response.status_code == 204:
        return True
    else:
        return False

def create_graph_message():
    '''Creates a message to then be edited for the total.'''
    
    url = "https://discord.com/api/channels/"+os.getenv("Graph_Channel_ID")+ "/messages"

    payload = '{"content":"."}'
    headers = {
        'authorization': "Bot "+os.getenv('BOT_TOKEN'),
        'content-type': "application/json",
        }

    response = requests.request("POST", url, data=payload, headers=headers)
    print(response.status_code)
    if response.status_code == 204:
        return True
    else:
        return False



if __name__ == "__main__":
   
    load_dotenv()
    #print(give_user_role(Member_ID= "107295705239986176",Role_ID = "975326545843458099"))
    #send_message(message="I AM SENT")
    edit_top_challenges_message()

    edit_leaderboard()
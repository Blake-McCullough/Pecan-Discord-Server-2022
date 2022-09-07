from operator import itemgetter
import requests
import os
from discord_webhook import DiscordWebhook
from dotenv import load_dotenv
from discord_oauth import edit_voice_channel_name, get_users_count_for_role
from pecan_server_communication import get_challenges, get_leaderboard
from datetime import datetime,timezone
from collections import defaultdict
import time

        
def send_edit_embed(message_url,message,title):
    '''Send the request to change the embed for the channel.'''
     #Gets current time.
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat()


    #Sends of editing message.
    payload = {
        'embeds':
        [
            {
                'title':title,
                'type':'rich',
                'description':message,
                'color':7419530,
                'timestamp':now,
                'author':
                {
                    'name':'PECAN CTF 2022',
                    'url':'https://blakemccullough.com/'
                },
                'footer':
                {
                    'text':'By Blake McCullough'
                }   
            }
        ]
    }
    headers = {
        'authorization': "Bot "+os.getenv('BOT_TOKEN'),
        'content-type': "application/json",
        }

    response = requests.request("PATCH", message_url, json=payload, headers=headers)

    if response.status_code == 204 or response.status_code==200:
        pass
    elif response.status_code == 429:
        print(int(response.headers["Retry-After"]))
        print(response.headers['x-ratelimit-scope'])
        print('Embed error: ' +str(response.status_code))
        print(response.headers)
    else:
        print('Embed error: ' +str(response.status_code))
        print(response.headers)
      
def extract_categories_message(data):
    '''Takes a list of challenges, returns a message with the categories and then the amount off solves'''

    #Sets as blank due to none being specified.
    counts = defaultdict(int)
    #loops through data setting key as the category name, and value as the amount of solves.
    for d in data:
        counts[d.get("category")] += d.get("solves")
    #Sorts the categories from most to least and converts to list.
    counts_sorted = sorted(counts.items(), key=lambda x: x[1],reverse = True)
    #Starting message.
    message = '__**Name: Solves **__\n\n'
    #Extracts the key and value from each element, then will add it to the message.
    for key, value in counts_sorted:
        message = message + f'**{key}:** {value}\n'
    return message
    
def send_updates_message(message):
    response = DiscordWebhook(url=os.getenv('GAME_WEBHOOK_URL'), content=message).execute()

def send_linking_message(message):
    response = DiscordWebhook(url=os.getenv('LINKING_WEBHOOK_URL'), content=message).execute()   

def give_user_role(Member_ID,Role_ID):
    '''Uses the discord API to give a user a role, then will return true on success, false on error.'''
    url = "https://discord.com/api/guilds/"+os.getenv("GUILD_ID")+ "/members/"+Member_ID+'/roles/'+Role_ID
    print(url)

    headers = {
        'authorization': "Bot "+os.getenv('BOT_TOKEN'),
        'content-type': "application/json",
        }
    response = requests.request("PUT", url,  headers=headers)
    if response.status_code == 204:
        return True
    else:
        print(response.status_code)
        return False
  
def give_team_division_role(user_id,division):
    try:
        #RoleID is determined based on what the skill id is.
        beginner_division = os.getenv('BEGINNER_DIVISION')
        intermediate_division = os.getenv('INTERMEDIATE_DIVISION')
        advance_division = os.getenv('ADVANCED_DIVISION')
        if division == beginner_division:
            role_id = os.getenv('BEGINNER_ROLE_ID')
        elif division == intermediate_division:
            role_id = os.getenv('INTERMEDIATE_ROLE_ID')
        elif division ==  advance_division:
            role_id = os.getenv('ADVANCED_ROLE_ID')
        else:
            send_linking_message(f'Failed to give the user: {user_id} a role, as division was: {division}')
            return
        give_user_role(Member_ID= user_id,Role_ID = role_id)
    except Exception as e:
        print(e)


def edit_top_challenges_message():
    '''Edits the message of the top challenge results.'''
    url = "https://discord.com/api/channels/"+os.getenv("GRAPH_CHANNEL_ID")+ "/messages/"+os.getenv("GRAPH_MESSAGE_ID")
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
      
    send_edit_embed(message_url=url,message =challenges_message,title='__**TOP COMPLETED CHALLENGES**__')


def edit_leaderboard():
    '''Edits the leaderboard on the api.'''
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
    send_edit_embed(message_url=url,message =challenges_message,title='__**USER LEADERBOARD**__')



def edit_categories_message():
    '''Edits the category solves message.'''
    url = "https://discord.com/api/channels/"+os.getenv("CATEGORIES_CHANNEL_ID")+ "/messages/"+os.getenv("CATEGORIES_MESSAGE_ID")
    data = get_challenges()
    message = extract_categories_message(data)
    send_edit_embed(message_url=url,message =message,title='__**TOP COMPLETED CATEGORIES**__')


def create_graph_message():
    '''Creates a message to then be edited for the total.'''
    
    url = "https://discord.com/api/channels/1013626850142072884/messages"
#Sends of editing message.
    payload = {
        'embeds':
        [
            {
                'title':'message',
                'type':'rich',
            }
        ]
    }
    headers = {
        'authorization': "Bot "+os.getenv('BOT_TOKEN'),
        'content-type': "application/json",
        }

    response = requests.request("POST", url, json=payload, headers=headers)
    print(response.status_code)

def edit_embeds():
    time.sleep(1)
    edit_top_challenges_message()
    time.sleep(1)
    edit_categories_message()   
    time.sleep(1)
    edit_leaderboard()

def edit_counts():
    #For beginners.
    edit_voice_channel_name(os.getenv('BEGINNERS_VC_ID'),"Beginners: " + str(get_users_count_for_role(os.getenv('BEGINNER_ROLE_ID'))))
    #For intermediate.
    edit_voice_channel_name(os.getenv('INTERMEDIATE_VC_ID'),"Intermediate: " + str(get_users_count_for_role(os.getenv('INTERMEDIATE_ROLE_ID'))))
    #For advanced.
    edit_voice_channel_name(os.getenv('ADVANCED_VC_ID'),"Advanced: " + str(get_users_count_for_role(os.getenv('ADVANCED_ROLE_ID'))))

def run_edits():
    edit_embeds()
    edit_counts()

if __name__ == "__main__":
   
    load_dotenv()
    #create_graph_message()
    run_edits()
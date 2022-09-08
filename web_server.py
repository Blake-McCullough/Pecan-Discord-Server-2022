
# importing modules
import datetime,flask,os
from flask import Flask,  redirect, request,Response, render_template, abort, redirect, request,  Response, render_template, make_response,url_for
from werkzeug.utils import secure_filename

from dotenv import load_dotenv
from discord_oauth import exchange_code, get_user_id, get_username_by_id, join_discord
from pecan_server_communication import get_current_team_score, get_division_by_id, get_teamname_by_id
from discord_server_link import edit_embeds, give_team_division_role, give_user_role, send_linking_message,  send_updates_message
from role_score_link import get_role_given
from teams_discord import fetch_team_discords, save_discord_id




load_dotenv()


# declaring app name
app = Flask(__name__)
#For adding the count of said item to the manifest ID.
@app.route('/pecanctf/challengecomplete',methods = ['POST', 'GET'])
def pecanchallengeevent():

    if request.method == 'POST':
        print('POST')
        data = request.json
        print(data)
        teamid = data["user"]["id"]
        teamname = data["user"]["name"]
        challengeid = data["challenge"]["id"]
        challengename =data["challenge"]["name"]
        description =  data["challenge"]["description"]
        challengevaluemax = data["challenge"]["points"]["max"]
        challengevaluemin = data["challenge"]["points"]["max"]
        category =  data["challenge"]["category"]


        #Gets current teams score.
        current_score = get_current_team_score(Team_ID=teamid)
        #Gets role ID, and role name
        role = get_role_given(Team_ID=teamid,Current_Score = current_score)
        
   
        #Checks if the user can recieve a role, if they can then will run this.
        if role == None:
            message = f'''**The team:** `{teamname}` | **Just completed:** `{challengename}` | **Current score:** `{current_score}`'''
        else:

            role_id = role['Role_ID']
            role_name = role['Role_Name']
            #Gets discord IDS
            discord_ids= fetch_team_discords(TEAM_ID=teamid)
            #Gives user roles.
            for user_id in discord_ids:
 
                give_user_role(Member_ID= user_id,Role_ID = role_id)


            message = f'''**The team:** `{teamname}` | **Just completed:** `{challengename}` | **Current Highest role:** `{role_name}` | **Current score:** `{current_score}`'''

        #Sends updates message
        send_updates_message(message = message)


        return 'Oh you made a <b>post</b> request that is pretty cool ngl!\n\n\n\nLol'
    if request.method == 'GET':
        return 'Oh you made a <b>get</b> request that is pretty not cool ngl!\n\n\n\nLol'

#For adding the count of said item to the manifest ID.
@app.route('/getdiscord')
def get_discord():
    team_id =request.args.get('teamid',None)
    
    if team_id == None:
        abort(412)
    else:
        data = fetch_team_discords(team_id)
        usernames = []
        for id in data:
            username = get_username_by_id(id)
            if username == None:
                pass
            else:
                usernames.append(username)
        response = flask.jsonify({"Results":usernames })
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
 



#For adding a discord user to the database (verifies via discord.)
@app.route('/adddiscord')
def add_discord():
    team_id =request.args.get('teamid',None)
    code =request.args.get('code',None)
    state =request.args.get('state',None)
    if team_id == None and (code == None or state == None):
        abort(412)
    if code != None and state != None:
        try:
            #Gets token.
            token = exchange_code(code)
            print(token)
            #Gets user ID.
            user_id = get_user_id(token)
            #Saves to database.
            save_status = save_discord_id(TEAM_ID = state,DISCORD_ID = user_id)
            #Gets the teams skill ID.
            division = get_division_by_id(team_id=state) 
            print(division)
            #Sets the users role to said teams ID
            give_team_division_role(user_id=user_id,division=division)
            #Joins the discord server.
            join_discord(token,user_id)
            #For logging event.
            username = get_username_by_id(user_id)
            teamname = get_teamname_by_id(state)
            log_message = f"The user {username} just linked the team {teamname}!\n||USER ID: {user_id} and TEAM ID: {state}||"
            send_linking_message(message = log_message)

            #Redirecting back.
            return redirect(os.getenv('BASE_PECAN_URL')+'profile')    
        except:
             return redirect("https://discord.com/oauth2/authorize?client_id="+os.getenv('CLIENT_ID')+"&redirect_uri="+os.getenv('REDIRECT_URI')+"&response_type=code&scope=identify%20guilds.join&state="+state, code=302)
    else:
        return redirect("https://discord.com/oauth2/authorize?client_id="+os.getenv('CLIENT_ID')+"&redirect_uri="+os.getenv('REDIRECT_URI')+"&response_type=code&scope=identify%20guilds.join&state="+team_id, code=302)
    
#For adding a discord user to the database (verifies via discord.)
@app.route('/pecanctf/editteamdetails')
def edit_team_details():  
    if request.method == 'POST':
        print('POST')
        data = request.json
        print(data)
        teamid = data["user"]["id"]
        teamname = data["user"]["name"]

        #Gets discord IDS
        discord_ids= fetch_team_discords(TEAM_ID=teamid)
        division = get_division_by_id(team_id=teamid) 
        #Gives user roles.
        for user_id in discord_ids:
 
                give_team_division_role(user_id=user_id,division=division)

        log_message = f"The team {teamname}! Just changed its details!\n||USER ID: {user_id}||"
        send_linking_message(message = log_message)


        return 'Oh you made a <b>post</b> request that is pretty cool ngl!\n\n\n\nLol'
    if request.method == 'GET':
        return 'Oh you made a <b>get</b> request that is pretty not cool ngl!\n\n\n\nLol' 

def start():
    print('Web server now online.')
    app.run(host='0.0.0.0', port=80)


if __name__ == "__main__":
    start()
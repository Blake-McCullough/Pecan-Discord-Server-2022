
# importing modules
import datetime,flask,os
from flask import Flask,  redirect, request,Response, render_template, abort, redirect, request,  Response, render_template, make_response,url_for
from werkzeug.utils import secure_filename

from dotenv import load_dotenv
from discord_oauth import exchange_code, get_user_id, join_discord
from pecan_server_communication import get_current_team_score
from discord_server_link import edit_embeds, give_user_role,  send_updates_message
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
@app.route('/adddiscord')
def add_discord():
    team_id =request.args.get('teamid',None)
    code =request.args.get('code',None)
    state =request.args.get('state',None)
    if team_id == None and (code == None or state == None):
        abort(412)
    if code != None and state != None:
        try:
            token = exchange_code(code)
            print(token)
            user_id = get_user_id(token)
            print(user_id)
            print(state)
            save_status = save_discord_id(TEAM_ID = state,DISCORD_ID = user_id)
            print(save_status)
            join_discord(token,user_id)

            #return redirect(os.getenv('BASE_PECAN_URL')+'/profile')
        except:
             return redirect("https://discord.com/oauth2/authorize?client_id="+os.getenv('CLIENT_ID')+"&redirect_uri="+os.getenv('REDIRECT_URI')+"&response_type=code&scope=identify%20guilds.join&state="+state, code=302)
    else:
        return redirect("https://discord.com/oauth2/authorize?client_id="+os.getenv('CLIENT_ID')+"&redirect_uri="+os.getenv('REDIRECT_URI')+"&response_type=code&scope=identify%20guilds.join&state="+team_id, code=302)
    
        

def start():
    print('Web server now online.')
    app.run(host='0.0.0.0', port=80)


if __name__ == "__main__":
    start()
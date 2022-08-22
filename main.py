

# importing modules
import datetime,flask,os
from flask import Flask,  redirect, request,Response, render_template, abort, redirect, request,  Response, render_template, make_response,url_for
from werkzeug.utils import secure_filename

from dotenv import load_dotenv
from database_team_score import get_current_team_score
from discord_server_link import give_user_role, send_message
from role_score_link import get_role_given

from teams_discord import get_discord_ids



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


        print(data)


        current_score = get_current_team_score(Team_ID=teamid)
        role = get_role_given(Team_ID=teamid,Current_score = current_score)
        role_id = role['Role_ID']
        role_name = role['Role_Name']
        print(role_id)


        if role_id == None:
            message = f'''\n
            The team: {teamname}
            Just completed {challengename}
            Current score: {current_score}
            '''
        else:
            discord_ids=get_discord_ids(Team_ID=teamid)
            print(discord_ids)
            for user_id in discord_ids:
                print(user_id)
                give_user_role(Member_ID= user_id,Role_ID = role_id)


            message = f'''\n
            The team: {teamname}
            Just completed {challengename}
            Current score: {current_score}
            Got role: {role_name}
            '''
        send_message(message = message)


        return 'Oh you made a <b>post</b> request that is pretty cool ngl!\n\n\n\n'
    if request.method == 'GET':
        return 'Oh you made a <b>get</b> request that is pretty not cool ngl!'




def start():
    app.run(host='0.0.0.0', port=80)




if __name__ == "__main__":
    start()
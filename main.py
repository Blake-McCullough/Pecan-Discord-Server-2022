from dotenv import load_dotenv
from discord_server_link import  run_edits
from teams_discord import start_up
import web_server,discord_bot
from multiprocessing import Process
def WebServer():
    web_server.start()
    
def DiscordBot():
    discord_bot.start()


#For event that occurs every x minutes.
import time
import atexit

from apscheduler.schedulers.background import BackgroundScheduler



scheduler = BackgroundScheduler()
scheduler.add_job(func=run_edits, trigger="interval", seconds=60)
scheduler.start()




if __name__ == "__main__":
    
    load_dotenv()
    start_up()
    #For running the bot and server at same time.
    #p1 = Process(target =  WebServer)
    WebServer()
    #p1.start()
    #p2 = Process(target = DiscordBot)
    #p2.start()
    
    
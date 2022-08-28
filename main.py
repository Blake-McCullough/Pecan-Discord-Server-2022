from dotenv import load_dotenv
from discord_server_link import edit_embeds
import web_server,discord_bot
from multiprocessing import Process
def WebServer():
    web_server.start()
    
def DiscordBot():
    discord_bot.start()







if __name__ == "__main__":
    
    load_dotenv()
    #For running the bot and server at same time.
    #p1 = Process(target =  WebServer)
    WebServer()
    #p1.start()
    #p2 = Process(target = DiscordBot)
    #p2.start()
    
    
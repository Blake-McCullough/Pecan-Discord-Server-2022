from dotenv import load_dotenv
import web_server,discord_bot
from multiprocessing import Process
def WebServer():
    web_server.start()
    
def DiscordBot():
    discord_bot.start()



if __name__ == "__main__":
    
    load_dotenv()
    p1 = Process(target =  WebServer)
    p1.start()
    p2 = Process(target = DiscordBot)
    p2.start()
    
    
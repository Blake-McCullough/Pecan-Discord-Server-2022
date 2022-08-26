from dotenv import load_dotenv
import web_server,discord_bot


if __name__ == "__main__":
    
    load_dotenv()
    discord_bot.start()
    web_server.start()
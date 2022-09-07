from dotenv import load_dotenv
from discord_server_link import  run_edits
from teams_discord import start_up





from apscheduler.schedulers.background import BackgroundScheduler



scheduler = BackgroundScheduler()
scheduler.add_job(func=run_edits, trigger="interval", seconds=60)
scheduler.start()




if __name__ == "__main__":
    
    load_dotenv()
    start_up()
    WebServer()

    
    
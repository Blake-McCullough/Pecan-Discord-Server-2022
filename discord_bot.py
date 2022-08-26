from dotenv import load_dotenv
import discord,os
from discord.ext import tasks
from discord_server_link import edit_embeds
from teams_discord import save_discord_id

bot = discord.Bot()

#Runs every minute.
@tasks.loop(minutes=1)
async def mytask():
    edit_embeds()

@bot.event
async def on_ready():
  print(f'{bot.user} has logged in.')
  #Starts event.
  mytask.start()

@bot.slash_command()
async def adduser(ctx, team_id,user: discord.User):
    if ctx.author.guild_permissions.manage_roles:
        try:
            result = save_discord_id(Team_ID = team_id,Discord_ID=user.id)
            if result == None:
                await ctx.respond(f"{user} Already in that team.", ephemeral=True)
            elif result == True:
                await ctx.respond(f"Successfully added {user} to team {team_id}", ephemeral=True)
            else:
                await ctx.respond(f"An error occurred.", ephemeral=True)
        except Exception as e:
            print(e)
    else:
        await ctx.respond(f"YOU DONT HAVE PERMS!!! (Need manage roles)", ephemeral=True)


def start():  
    bot.run(os.getenv('BOT_TOKEN'))



if __name__ == "__main__":
    
    load_dotenv()
    start()

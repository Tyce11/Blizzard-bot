import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

inty = discord.Intents.default()
inty.message_content = True

# Change command prefix
bot = commands.Bot(command_prefix="!",intents=inty)

# Removes the default help command
bot.remove_command("help")

# Import any new cogs here
from help_cog import help_cog
from music_cog import music_cog

@bot.event
async def on_ready():
    # Add any new cogs added here
    await bot.add_cog(help_cog(bot))
    await bot.add_cog(music_cog(bot))

# Gets discord token from .env file
load_dotenv()
token = os.getenv('TOKEN')
bot.run(token)
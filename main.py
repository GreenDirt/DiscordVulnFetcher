import discord
from config import *
from discord_bot import DiscordBot

if __name__ == "__main__":
	intents = discord.Intents.default()
	intents.message_content = True

	client = DiscordBot(intents=intents)
	client.run(DISCORD_BOT_TOKEN)
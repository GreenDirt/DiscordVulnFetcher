#!/usr/bin/env python3

import discord
from datetime import datetime
from datetime import timedelta
from discord_formatter import DiscordFormatter
from config import *

class DiscordBot(discord.Client):

	async def on_message(self, message):
		pass

	async def on_ready(self):	# Used as __init__ in our case
		print(f"Logged on as {self.user}")
		self.errors_to_display = []
		self.error_channel = None
		self.yesterday = datetime.today()-timedelta(days=1)

		for channel in self.get_all_channels():
			if channel.name == ERROR_CHANNEL_NAME:
				self.error_channel = channel

		self.formatter = DiscordFormatter(self.yesterday)
		print("Getting content for current day")
		self.full_responses = self.formatter.get_day_content()

		print("Sending for high, medium and low")
		await self.send_threats("high", "daily_high")
		await self.send_threats("medium", "daily_medium")
		await self.send_threats("low", "daily_low")

		await self.send_errors()	
		await self.close()

	async def send_threats(self, risk="high", channel_name="daily_high"):
		channel = None
		for channel_in_list in self.get_all_channels():
			if channel_in_list.name == channel_name:
				channel = channel_in_list
		if not channel:
			self.errors_to_display.append(f"Channel '{channel_name}' not found")
			return None
		
		if not risk in self.full_responses.keys():
			print(f"Risk level not found {risk}")

		try:
			threats_by_product = self.full_responses[risk]
		except KeyError:
			print("No threat today")
			return

		no_threat = True
		for product in threats_by_product.keys():
			for threat in threats_by_product[product]:
				no_threat = False
		if no_threat:
			return

		await channel.send(f"__Failles {risk} du {self.yesterday.strftime('%F')}__\n")

		for product in threats_by_product.keys():
			await channel.send(product + " : \n")
			for threat in threats_by_product[product]:
				await channel.send(threat)


	async def send_errors(self):
		if self.error_channel:
			for error in self.errors_to_display:
				print("Error during execution : " + str(error))
				await self.error_channel.send(error)
			self.errors_to_display = []
		else:
			print("Error : Error channel don't exists")

#!/usr/bin/env python3

from datetime import datetime
from vuldb_api import VuldbApi
from config import *

class DiscordFormatter:
	def __init__(self, day=datetime.now().strftime("%F").replace('-', '')):
		self.responses = {}
		self.day = str(int(day)-1)	# Permet d'avoir la veille
		self.vuldb_res = None

	def get_vuldb(self):
		self.vuldb_res = VuldbApi().get_for_day(self.day)

	# Return self.responses[risk][product][]
	def get_day_content(self, product=None):	# Return all possible content
		self.responses["high"] = self.format_vuldb(product, risk_min=40, risk_max=100)
		self.responses["medium"] = self.format_vuldb(product, risk_min=3, risk_max=4)
		self.responses["low"] = self.format_vuldb(product, risk_min=0, risk_max=2)

		return self.responses

	# Return : threats[product][]
	def format_vuldb(self, product=None, risk_min=0, risk_max=5):
		threats_list = []
		
		if not self.vuldb_res:
			self.get_vuldb()
			if not self.vuldb_res:
				return {"Error": ["Vuldb response is None"]}
		if not "result" in self.vuldb_res:
			return {"Error": ["Vuldb returned an error", str(self.vuldb_res)]}

		for result in self.vuldb_res["result"]:

			## Start formatting for threat
			clean_res = ""
			clean_res += ""
			# Title
			clean_res += "**Title : " + str(result["entry"]["title"]) + "**"
			clean_res += "\n"

			# CVE
			if "source" in result.keys():
				if "cve" in result["source"].keys():
					if "id" in result["source"]["cve"].keys():
						clean_res += "CVE : " + str(result["source"]["cve"]["id"])
			clean_res += "\n"

			# Try to determine if risk corresponds to our search
			try:
				risk_value = result["vulnerability"]["risk"]["value"]
				if risk_min >= int(risk_value) or int(risk_value) >= risk_max:
					continue
				else:
					clean_res += f"Risk : {str(risk_value)}\n"
			except KeyError:
				try:
					risk_name = result["vulnerability"]["risk"]["name"]
					if risk_name == "low" and (risk_min >= 3):
						continue
					elif risk_name == "medium" and (risk_min > 4 or risk_max <= 3):
						continue
					elif risk_name == "high" and risk_max <= 4:
						continue
					else:
						clean_res += f"Risk : {risk_name}\n"

				except KeyError:
					clean_res += "Risk can't be determined\n"
			##
			## Try to get id and create link with shape : https://vuldb.com/?id.{id}
			try:
				clean_res += "Detail link : https://vuldb.com/?id." + str(result["entry"]["id"]) + "\n"
			except KeyError:
				pass

			clean_res += ""


			# If all is OK add to returned list
			threats_list.append(clean_res)

		threats = {"Unknown" : []}
		for threat in threats_list:
			added = False
			for PRODUCT in PRODUCT_LIST:
				if PRODUCT.lower() in threat.lower():
					if PRODUCT in threats.keys():
						threats[PRODUCT].append(threat)
					else:
						threats[PRODUCT] = [threat]
					added = True
					break
			if not added:	# If no product attached, add to unknown
				threats["Unknown"].append(threat)

		return threats

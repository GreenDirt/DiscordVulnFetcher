#!/usr/bin/env python3

import requests
import json
from config import *

class VuldbApi:
	def __init__(self):
		self.api_key = VULDB_APIKEY
		self.userAgent = 'VulDB API'
		self.headers = {'User-Agent': self.userAgent, 'X-VulDB-ApiKey': self.api_key}

	def get_for_day(self, date, details=False):
		
		# Detail set on true = Many credits
		url = 'https://vuldb.com/?api'

		postData = {}
		postData['details'] = int(details)
		postData['advisory_date'] = str(date.strftime("%F").replace('-', ''))

		# Get API response
		response = requests.post(url, headers=self.headers, data=postData)

		if response.status_code != 200:
			return response.content

		responseJson = json.loads(response.content)
		return responseJson
		#return res_dbg


#api = VulndbApi()
#api.get_for_day()
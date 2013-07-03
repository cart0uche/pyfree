#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pyFree!

import os
import time
import requests
import json
import hmac
from hashlib import sha1


APP_TOKEN_FILE = '.app_token'

FREEBOX_URL    = 'http://mafreebox.freebox.fr/'
API_VERSION    = 'api_version'
API_BASE_URL   = 'api/'

LOGIN          = 'login/'
LOGIN_AUTH     = 'login/authorize/'
LOGIN_SESSION  = 'login/session/'

CALL_LOG       = 'call/log/'


class pyFree():

	def __init__(self):
		if os.path.isfile(APP_TOKEN_FILE):
			fileAppTocken = open(APP_TOKEN_FILE, 'r')
			self._appTocken = fileAppTocken.read()
			print "appTocken = " + self._appTocken
			fileAppTocken.close()
			self._AuthorizationGranted = True
		else:
			self._AuthorizationGranted = False

		version = str(self.api_version.find('.'))
		self._baseUrl = FREEBOX_URL + API_BASE_URL + 'v' + version + '/'

	def ask_autorization(self, app_id, app_name, app_version, device_name):
		"""
			This must be call the first time the application is lauched.
			An authorization has to be done directly on the Freebox.
			See http://dev.freebox.fr/sdk/os/login/
		"""
		parameter = {"app_id": app_id, "app_name": app_name, "app_version": app_version, "device_name": device_name}
		getAppToken = self._requestToFreebox(self._baseUrl + LOGIN_AUTH, 'POST', parameter)

		if (getAppToken["success"] is not True):
			return 1

		trackId = str(getAppToken["result"]["track_id"])

		while True:
			authorization = self._requestToFreebox(self._baseUrl + LOGIN_AUTH + trackId, 'GET')
			if not authorization["result"]["status"] == 'pending':
				break
			time.sleep(1)

		if not authorization["result"]["status"] == "granted":
			return 1

		appTokenFile = open(APP_TOKEN_FILE, 'w')
		appTokenFile.write(getAppToken["result"]["app_token"])
		appTokenFile.close()
		self._appTocken = getAppToken["result"]["app_token"]
		return 0

	def login(self, app_id):
		"""
			This function has to be called after the authorization has been granted by the function askAutorization.
		"""
		loginResponse = self._requestToFreebox(self._baseUrl + LOGIN, 'GET')

		if loginResponse["success"] is not True:
			return 1

		challenge = loginResponse["result"]["challenge"]

		passwordBin = hmac.new(self._appTocken, challenge, sha1)
		password  = passwordBin.hexdigest()

		parameter = {"app_id": app_id, "password": password}
		loginResponse = self._requestToFreebox(self._baseUrl + LOGIN_SESSION, 'POST', parameter)

		if loginResponse["success"] is True:
			self._sessionTocken = loginResponse["result"]["session_token"]
		else:
			print loginResponse["msg"] + " : " + loginResponse["error_code"]
			return 1

		return 0

	def get_callList(self):
		"""
			Access the Freebox call logs.
			See http://dev.freebox.fr/sdk/os/call/
		"""
		header = {'X-Fbx-App-Auth': self._sessionTocken}
		callResponse = self._requestToFreebox(self._baseUrl + CALL_LOG, 'GET', header=header)
		return callResponse

	def _requestToFreebox(self, url, requestType, parameters=None, header=None):
		# print url
		if (requestType == 'GET'):
			response = requests.get(url, headers=header)
		if (requestType == 'POST'):
			parameters = json.dumps(parameters)
			response = requests.post(url, data=parameters, headers=header)

		# print response.json()
		return response.json()

	@property
	def device_name(self):
		version = self._requestToFreebox(FREEBOX_URL + API_VERSION, 'GET')
		return version['device_name']

	@property
	def uid(self):
		version = self._requestToFreebox(FREEBOX_URL + API_VERSION, 'GET')
		return version['uid']

	@property
	def api_version(self):
		version = self._requestToFreebox(FREEBOX_URL + API_VERSION, 'GET')
		return version['api_version']

	@property
	def device_type(self):
		version = self._requestToFreebox(FREEBOX_URL + API_VERSION, 'GET')
		return version['device_type']

# def main():
# 	freebox = pyFree()
# 	print "====================================="
# 	print "Device name = " + freebox.device_name
# 	print "uid         = " + freebox.uid
# 	print "api_version = " + freebox.api_version
# 	print "device_type = " + freebox.device_type
# 	print "====================================="

# 	if freebox.ask_autorization("1", "appliTest", "0.1", "theBeast") is not 0:
# 		print "Authorization failed"

# 	if freebox.login("1") is not 0:
# 		print "Login failed"

# 	print freebox.get_callList()


# if __name__ == '__main__':
# 	main()

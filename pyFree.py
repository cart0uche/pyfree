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
		print self._baseUrl

	@property
	def device_name(self):
		version = requests.get(FREEBOX_URL + API_VERSION)
		return version.json()['device_name']

	@property
	def uid(self):
		version = requests.get(FREEBOX_URL + API_VERSION)
		return version.json()['uid']

	@property
	def api_version(self):
		version = requests.get(FREEBOX_URL + API_VERSION)
		return version.json()['api_version']

	@property
	def device_type(self):
		version = requests.get(FREEBOX_URL + API_VERSION)
		return version.json()['device_type']

	def askAutorization(self, app_id, app_name, app_version, device_name):
		request = json.dumps({"app_id": app_id, "app_name": app_name, "app_version": app_version, "device_name": device_name})
		getAppToken = requests.post(self._baseUrl + LOGIN_AUTH, data=request)
		getAppToken = getAppToken.json()

		if (getAppToken["success"] is not True):
			return 1

		trackId = str(getAppToken["result"]["track_id"])

		while True:
			authorization = requests.get(self._baseUrl + LOGIN_AUTH + trackId, data=request)
			authorization = authorization.json()
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
		loginResponse = requests.get(self._baseUrl + LOGIN)
		loginResponse = loginResponse.json()

		if loginResponse["success"] is not True:
			return 1

		challenge = loginResponse["result"]["challenge"]
		print "challenge = " + challenge
		print "appTocken = " + self._appTocken

		passwordBin = hmac.new(self._appTocken, challenge, sha1)
		password  = passwordBin.hexdigest()
		print "password = " + password

		loginRequest = json.dumps({"app_id": app_id, "password": password})
		loginResponse = requests.post(self._baseUrl + LOGIN_SESSION, data=loginRequest)
		loginResponse = loginResponse.json()

		if loginResponse["success"] is True:
			self._sessionTocken = loginResponse["result"]["session_token"]
		else:
			print loginResponse["msg"] + " : " + loginResponse["error_code"]
			return 1

		return 0

	def getCallList(self):
		header = {'X-Fbx-App-Auth': self._sessionTocken}
		callResponse = requests.get(self._baseUrl + CALL_LOG, headers=header)
		callResponse = callResponse.json()

		print callResponse
		return callResponse


def main():
	freebox = pyFree()
	print "====================================="
	print "Device name = " + freebox.device_name
	print "uid         = " + freebox.uid
	print "api_version = " + freebox.api_version
	print "device_type = " + freebox.device_type
	print "====================================="

	#if freebox.askAutorization("1", "appliTest", "0.1", "theBeast") is not 0:
		#print "Authorization failed"

	if freebox.login("1") is not 0:
		print "Login failed"

	freebox.getCallList()


if __name__ == '__main__':
	main()

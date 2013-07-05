#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pyfree!

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


class freebox():

	def __init__(self):
		if os.path.isfile(APP_TOKEN_FILE):
			file_app_tocken = open(APP_TOKEN_FILE, 'r')
			self._app_tocken = file_app_tocken.read()
			print "appTocken = " + self._app_tocken
			file_app_tocken.close()
			self._authorization_granted = True
		else:
			self._authorization_granted = False

		version = str(self.api_version.find('.'))
		self._base_url = FREEBOX_URL + API_BASE_URL + 'v' + version + '/'

	def is_authorization_granted(self):
		if os.path.isfile(APP_TOKEN_FILE):
			return True
		else:
			return False

	def ask_authorization(self, app_id, app_name, app_version, device_name):
		"""
			This must be call the first time the application is lauched.
			An authorization has to be done directly on the Freebox.
			See http://dev.freebox.fr/sdk/os/login/
		"""
		parameter = {"app_id": app_id, "app_name": app_name, "app_version": app_version, "device_name": device_name}
		authorization_reponse = self._request_to_freebox(self._base_url + LOGIN_AUTH, 'POST', parameter)

		if (authorization_reponse["success"] is not True):
			return 1

		track_id = str(authorization_reponse["result"]["track_id"])

		while True:
			authorization = self._request_to_freebox(self._base_url + LOGIN_AUTH + track_id, 'GET')
			if not authorization["result"]["status"] == 'pending':
				break
			time.sleep(1)

		if not authorization["result"]["status"] == "granted":
			return 1

		file_app_tocken = open(APP_TOKEN_FILE, 'w')
		file_app_tocken.write(authorization_reponse["result"]["app_token"])
		file_app_tocken.close()
		self._app_tocken = str(authorization_reponse["result"]["app_token"])
		return 0

	def login(self, app_id):
		"""
			This function has to be called after the authorization has been granted by the function ask_authorization.
		"""
		login_response = self._request_to_freebox(self._base_url + LOGIN, 'GET')

		if login_response["success"] is not True:
			return 1

		challenge = login_response["result"]["challenge"]

		password_bin = hmac.new(self._app_tocken, challenge, sha1)
		password  = password_bin.hexdigest()

		parameter = {"app_id": app_id, "password": password}
		login_response = self._request_to_freebox(self._base_url + LOGIN_SESSION, 'POST', parameter)

		if login_response["success"] is True:
			self._session_tocken = login_response["result"]["session_token"]
		else:
			print login_response["msg"] + " : " + login_response["error_code"]
			return 1

		return 0

	def get_call_list(self):
		"""
			Access the Freebox call logs.
			See http://dev.freebox.fr/sdk/os/call/
		"""
		header = {'X-Fbx-App-Auth': self._session_tocken}
		callResponse = self._request_to_freebox(self._base_url + CALL_LOG, 'GET', header=header)
		return callResponse

	def _request_to_freebox(self, url, requestType, parameters=None, header=None):
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
		version = self._request_to_freebox(FREEBOX_URL + API_VERSION, 'GET')
		return version['device_name']

	@property
	def uid(self):
		version = self._request_to_freebox(FREEBOX_URL + API_VERSION, 'GET')
		return version['uid']

	@property
	def api_version(self):
		version = self._request_to_freebox(FREEBOX_URL + API_VERSION, 'GET')
		return version['api_version']

	@property
	def device_type(self):
		version = self._request_to_freebox(FREEBOX_URL + API_VERSION, 'GET')
		return version['device_type']

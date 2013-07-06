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

CONTACT        = 'contact/'

CALL_LOG       = 'call/log/'

LCD            = 'lcd/config/'


class freebox():

	def __init__(self):
		if os.path.isfile(APP_TOKEN_FILE):
			file_app_tocken = open(APP_TOKEN_FILE, 'r')
			self._app_tocken = file_app_tocken.read()
			file_app_tocken.close()

		version = str(self.api_version.find('.'))
		self._base_url = FREEBOX_URL + API_BASE_URL + 'v' + version + '/'

	def is_authorization_granted(self):
		"""
			Return True if an authorization has already been granted on the freebox
		"""
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
		call_list = self._request_to_freebox(self._base_url + CALL_LOG, 'GET')
		return call_list

	################################# CONTACT #################################
	def get_contact_list(self):
		parameter = {"start": 1, "limit": 4, "group_id": 1}
		contact_list = self._request_to_freebox(self._base_url + CONTACT, 'POST', parameters=parameter)
		return contact_list

	def get_contact(self, contact_id):
		contact = self._request_to_freebox(self._base_url + CONTACT + contact_id, 'GET')
		return contact

	def create_contact(self, display_name=None, first_name=None, last_name=None):
		parameter = {'display_name': display_name, 'first_name': first_name, 'last_name': last_name}
		create_contact_response = self._request_to_freebox(self._base_url + CONTACT, 'POST', parameters=parameter)
		return create_contact_response

	def delete_contact(self, contact_id):
		delete_contact = self._request_to_freebox(self._base_url + CONTACT + contact_id, 'GET')
		return delete_contact
	###########################################################################

	################################# LCD #####################################
	def get_lcd_config(self):
		lcd_config = self._request_to_freebox(self._base_url + LCD, 'GET')
		return lcd_config

	def update_lcd_config(self, brightness=None, orientation=None, orientation_forced=None):
		parameter = {'brightness': brightness, 'orientation': orientation, 'orientation_forced': orientation_forced}
		update_lcd_config_response = self._request_to_freebox(self._base_url + LCD, 'POST', parameters=parameter)
		return update_lcd_config_response
	###########################################################################

	def _request_to_freebox(self, url, requestType, parameters=None):
		header = {'X-Fbx-App-Auth': self._session_tocken} if hasattr(self, '_session_tocken') else None
		if (requestType == 'GET'):
			response = requests.get(url, headers=header)
		if (requestType == 'POST'):
			parameters = json.dumps(parameters)
			response = requests.post(url, data=parameters, headers=header)
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

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pyfree!

"""
	This API is an unofficial imlplementation of the official Freebox OS API
	detailed here http://dev.freebox.fr/sdk/os/
"""

import os
import datetime
import time
import requests
import json
import hmac
from hashlib import sha1
import base64

GET  = 0
POST = 1
PUT  = 2


APP_TOKEN_FILE = '.app_token'

LOCAL_FREEBOX_URL = 'http://mafreebox.freebox.fr/'

API_VERSION    = 'api_version'
API_BASE_URL   = 'api/'



api_config = {
"ask_authorization1": {"path":"login/authorize/", "request_type":POST, "is_response_json":True },
"ask_authorization2": {"path":"login/authorize/", "request_type":GET , "is_response_json":True },

"login1"            : {"path":"login/"          , "request_type":GET , "is_response_json":True },
"login2"            : {"path":"login/session/"  , "request_type":POST, "is_response_json":True },

"get_call_list"     : {"path":"call/log/"       , "request_type":GET , "is_response_json":True },
"get_contact"       : {"path":"contact/"        , "request_type":GET , "is_response_json":True },

"create_contact"    : {"path":"contact/"        , "request_type":POST, "is_response_json":True },
"delete_contact"    : {"path":"contact/"        , "request_type":GET , "is_response_json":True },

"get_lcd_config"    : {"path":"lcd/config/"     , "request_type":GET , "is_response_json":True },
"update_lcd_config" : {"path":"lcd/config/"     , "request_type":POST, "is_response_json":True },

"set_wifi_status"   : {"path":"wifi/config/"    , "request_type":PUT , "is_response_json":True },

"reboot"            : {"path":"system/reboot/"  , "request_type":POST, "is_response_json":True },

"get_file_list"     : {"path":"fs/ls/"          , "request_type":GET , "is_response_json":True },
"download_file"     : {"path":"dl/"             , "request_type":GET , "is_response_json":False},
"move_files"        : {"path":"fs/mv/"          , "request_type":POST, "is_response_json":True }
}

class Freebox():

	def __init__(self, freebox_ip=None, freebox_port=None, debug=False):
		if os.path.isfile(APP_TOKEN_FILE):
			self._app_tocken = open(APP_TOKEN_FILE, 'r').read()

		if freebox_port is not None and freebox_ip is not None:
			self._freebox_url = 'http://' + freebox_ip + ':' + freebox_port + '/'
		else:
			self._freebox_url = LOCAL_FREEBOX_URL

		version = str(self.api_version.find('.'))
		if freebox_port is not None and freebox_ip is not None:
			self._base_url = 'http://' + freebox_ip + ':' + freebox_port + '/' + API_BASE_URL + 'v' + version + '/'
		else:
			self._base_url = LOCAL_FREEBOX_URL + API_BASE_URL + 'v' + version + '/'

		self._debug = debug

	def is_authorization_granted(self):
		"""
			Return True if an authorization has already been granted on the freebox.
		"""
		return True if os.path.isfile(APP_TOKEN_FILE) else False

	def ask_authorization(self, app_id, app_name, app_version, device_name):
		"""
			This must be call the first time the application is lauched.
			An authorization has to be done directly on the Freebox.
			See http://dev.freebox.fr/sdk/os/login/
		"""
		parameter = {"app_id": app_id, "app_name": app_name, "app_version": app_version, "device_name": device_name}
		authorization_reponse = self._request_to_freebox("ask_authorization1", parameters=parameter)

		if (authorization_reponse["success"] is not True):
			return None

		track_id = str(authorization_reponse["result"]["track_id"])

		while True:
			authorization = self._request_to_freebox("ask_authorization2", track_id)
			if not authorization["result"]["status"] == 'pending':
				break
			time.sleep(1)

		if authorization["result"]["status"] == "granted":
			self._app_tocken = str(authorization_reponse["result"]["app_token"])
			open(APP_TOKEN_FILE, 'w').write(self._app_tocken)
			return self._app_tocken
		else:
			return None

	def login(self, app_id):
		"""
			This function has to be called after the authorization has been granted by the function ask_authorization.
		"""
		login_response = self._request_to_freebox("login1")

		if login_response["success"] is False:
			return None

		challenge = login_response["result"]["challenge"]

		password_bin = hmac.new(self._app_tocken, challenge, sha1)
		password  = password_bin.hexdigest()

		parameter = {"app_id": app_id, "password": password}
		login_response = self._request_to_freebox("login2", parameters=parameter)

		if login_response["success"] is True:
			self._session_tocken = str(login_response["result"]["session_token"])

		return self._session_tocken

	##########################################################################

	def get_call_list(self):
		"""
			Access the Freebox call logs.
			See http://dev.freebox.fr/sdk/os/call/
		"""
		call_list = self._request_to_freebox("get_call_list")
		return call_list

	def _is_calling_today(self, timestamp):
		"""
			Return True if the parameter timestamp occurs today.
			False otherwise.
		"""
		if str(datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')) == str(datetime.date.today()):
			return True
		else:
			return False

	def get_missed_call(self, today=False, convert_date=True):
		"""
			Return missing calls.
			See http://dev.freebox.fr/sdk/os/call/
		"""
		missed_call = []
		call_list = self.get_call_list()

		if call_list["success"] is False:
			return missed_call

		for call in call_list["result"]:
			if ((self._is_calling_today(call["datetime"]) is True) and call["type"] == "missed"):
				if convert_date is True:
					call["datetime"] = str(datetime.datetime.fromtimestamp(call["datetime"]).strftime('%H:%M:%S - %d/%m/%Y'))
				missed_call.append(call)

		return missed_call

	##########################################################################

	def get_contact_list(self):
		"""
			Get list of contacts.
			See http://dev.freebox.fr/sdk/os/contacts/
		"""
		parameter = {"start": 1, "limit": 4, "group_id": 1}
		contact_list = self._request_to_freebox("get_contact_list", parameters=parameter)
		return contact_list

	def get_contact(self, contact_id):
		"""
			Access a given contact entry.
			See http://dev.freebox.fr/sdk/os/contacts/
		"""
		contact = self._request_to_freebox("get_contact", contact_id)
		return contact

	def create_contact(self, display_name=None, first_name=None, last_name=None):
		"""
			Create a contact.
			See http://dev.freebox.fr/sdk/os/contacts/
		"""
		parameter = {'display_name': display_name, 'first_name': first_name, 'last_name': last_name}
		create_contact_response = self._request_to_freebox("create_contact", parameters=parameter)
		return create_contact_response

	def delete_contact(self, contact_id):
		"""
			Delete a contact.
			See http://dev.freebox.fr/sdk/os/contacts/
		"""
		delete_contact = self._request_to_freebox("delete_contact", contact_id)
		return delete_contact

	##########################################################################

	def get_lcd_config(self):
		"""
			Get the current LCD configuration.
			See http://dev.freebox.fr/sdk/os/lcd/
		"""
		lcd_config = self._request_to_freebox("get_lcd_config")
		return lcd_config

	def update_lcd_config(self, brightness=None, orientation=None, orientation_forced=None):
		"""
			Update the current LCD configuration.
			See http://dev.freebox.fr/sdk/os/lcd/
		"""
		parameter = {'brightness': brightness, 'orientation': orientation, 'orientation_forced': orientation_forced}
		update_lcd_config_response = self._request_to_freebox("update_lcd_config", parameters=parameter)
		return update_lcd_config_response

	###########################################################################

	def set_wifi_status(self, enabled=True):
		"""
			Change Wifi status (on/off)
			See http://dev.freebox.fr/sdk/os/wifi/
		"""
		parameter = {"bss": {"perso":{"enabled": enabled}}}
		parameter = {"ap_params": {"enabled": enabled}}
		set_wifi_status_response = self._request_to_freebox("set_wifi_status", parameters=parameter)
		return set_wifi_status_response
	
	###########################################################################
	
	def reboot(self):
		"""
			Reboot Freebox
		"""
		# Cette application n'est pas autorisée à accéder à cette fonction : insufficient_rights
		self._request_to_freebox("reboot")

	###########################################################################

	def get_file_list(self, directory):
		"""
			Get a list of files from a specific directory.
			See http://dev.freebox.fr/sdk/os/fs/#list-files
		"""
		# parameter = {'onlyFolder': False, 'countSubFolder': False, 'removeHidden': True}
		file_list = self._request_to_freebox("get_file_list", base64.b64encode(directory))
		return file_list

	def download_file(self, file_path_b64, file_path_save):
		"""
			Dowload file 'file_path_b64' and save it at 'file_path_save'
			See http://dev.freebox.fr/sdk/os/fs/#download-a-file
		"""
		result = self._request_to_freebox("download_file", file_path_b64)
		open(file_path_save, 'w').write(result.content)

	def move_files(self, files_to_move_b64, destination_path_b64):
		"""
			Moves files in 'files_to_move_b64' list to 'destination_path_b64' directory
			See http://dev.freebox.fr/sdk/os/fs/#move-files
		"""
		parameter = {'files': files_to_move_b64, 'dct': destination_path_b64, 'mode': "overwrite"}
		result = self._request_to_freebox("move_files", parameters=parameter)
		return result

	###########################################################################

	@property
	def device_name(self):
		"""
			The device name "Freebox Server".
		"""
		version = requests.get(self._freebox_url + API_VERSION)
		return version.json()['device_name']

	@property
	def uid(self):
		"""
			The device unique id.
		"""
		version = requests.get(self._freebox_url + API_VERSION)
		return version.json()['uid']

	@property
	def api_version(self):
		"""
			The current API version on the Freebox.
		"""
		version = requests.get(self._freebox_url + API_VERSION)
		return version.json()['api_version']

	@property
	def device_type(self):
		"""
			“FreeboxServer1,1” for the Freebox Server revision 1,1
		"""
		version = requests.get(self._freebox_url + API_VERSION)
		return version.json()['device_type']

	@property
	def api_base_url(self):
		"""
			The API root path on the HTTP server.
		"""
		version = requests.get(self._freebox_url + API_VERSION)
		return version.json()['api_base_url']

	###########################################################################

	def _request_to_freebox(self, function_name, url_parameter="", parameters=None):
		url              = self._base_url + api_config[function_name]["path"] + url_parameter
		request_type     = api_config[function_name]["request_type"]
		is_response_json = api_config[function_name]["is_response_json"]

		self.print_debug('--> ' + url)
		header = {'X-Fbx-App-Auth': self._session_tocken} if hasattr(self, '_session_tocken') else None

		if (request_type == GET):
			response = requests.get(url, headers=header)
		if (request_type == POST):
			response = requests.post(url, data=json.dumps(parameters), headers=header)
		if (request_type == PUT):
			response = requests.put(url, data=json.dumps(parameters), headers=header)

		if is_response_json is True:
			response = response.json()
			if response["success"] is False:
				print 'Error ' + response["msg"].encode('utf-8') + ' : ' + response["error_code"].encode('utf-8')

		return response

	###########################################################################

	def print_debug(self, message):
		if self._debug:
			print message

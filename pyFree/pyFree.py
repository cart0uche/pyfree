# -*- coding: utf-8 -*-
# pyFree!

import requests

FREEBOX_URL = 'http://mafreebox.freebox.fr/'
API_VERSION = 'api_version'


class pyFree():

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


def main():
	freebox = pyFree()
	print "Device name = " + freebox.device_name
	print "uid = " + freebox.uid
	print "api_version = " + freebox.api_version
	print "device_type = " + freebox.device_type

if __name__ == '__main__':
	main()

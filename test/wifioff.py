#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append('..')
from pyfree import Freebox

BYTE_PER_MO = 1048576


def main():
	fb = Freebox(debug=True)
	print '====================================='
	print 'device name  = ' + fb.device_name
	print 'api_version  = ' + fb.api_version
	print 'device_type  = ' + fb.device_type
	print 'uid          = ' + fb.uid
	print 'api_base_url = ' + fb.api_base_url
	print '====================================='

	# Authorization
	if fb.is_authorization_granted():
		print 'Authorization already granted'
	else:
		print 'Asking authorisation ...'
		if fb.ask_authorization('1', 'ManageWifi', '0.1', 'theBeast') is not None:
			print 'Authorization granted'
		else:
			print 'Authorization failed'
			exit()

	# Login
	if fb.login("1") is not None:
		print 'Login successful'
	else:
		print 'Login faild'
		exit()

	fb.set_wifi_status(enabled=False)
	
if __name__ == '__main__':
	main()

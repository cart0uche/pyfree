#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append('..')
from pyfree import Freebox

BYTE_PER_MO = 1048576


def main():
	fb = Freebox()
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
		if fb.ask_authorization('1', 'appliTest', '0.1', 'theBeast') is not None:
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

	# Call list
	# call_list = fb.get_call_list()
	# print "Call list:"
	# print call_list

	# Contact list
	# print "Contact list:"
	# contact_list = fb.get_contact_list()
	# print contact_list

	# Contact details
	# print "Contact :"
	# contact = fb.get_contact('24')
	# print contact

	# Create contact
	# fb.create_contact(display_name='Sandy Kilo', first_name='Sandy', last_name='Kilo')

	# Delete contact
	# fb.delete_contact('24')

	# LCD config
	# lcd_config = fb.get_lcd_config()
	# print lcd_config

	# LCD update config
	# print fb.update_lcd_config(orientation=1)
	# time.sleep(3)
	# print fb.update_lcd_config(orientation=0)

	# fb.reboot()

	# missed_calls = fb.get_missed_call(today=True)
	# print str(len(missed_calls)) + " missed call found"
	# for call in missed_calls:
	# 	print call["number"] + " @ " + str(call["datetime"])

	# Get file list in directory 'Vidéo'
	file_list = fb.get_file_list('/Disque dur/Vidéos/')
	for file in file_list['result']:
		print file['name'] + ' ' + str(file['size']/BYTE_PER_MO) + 'Mo'

	# Download file video-2012-05-20-17-12-55.mp4
	for file in file_list['result']:
		if file['name'] == 'video-2012-05-20-17-12-55.mp4':
			fb.download_file(file['path'], file['name'])

if __name__ == '__main__':
	main()

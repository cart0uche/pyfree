import time
import sys
sys.path.append('..')
from pyfree import freebox


def main():
	fb = freebox()
	print '====================================='
	print 'Device name = ' + fb.device_name
	print 'api_version = ' + fb.api_version
	print 'device_type = ' + fb.device_type
	print 'uid         = ' + fb.uid
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
	if fb.login("1"):
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

	fb.reboot()


if __name__ == '__main__':
	main()

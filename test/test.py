import sys
sys.path.append('..')
from pyfree import freebox


def main():
	fb = freebox()
	print '====================================='
	print 'Device name = ' + fb.device_name
	print 'uid         = ' + fb.uid
	print 'api_version = ' + fb.api_version
	print 'device_type = ' + fb.device_type
	print "====================================="

	# Authorization
	if fb.is_authorization_granted():
		print "Authorization already granted"
	else:
		print 'Asking authorisation ...'
		if fb.ask_autorization("1", "appliTest", "0.1", "theBeast") is not 0:
			print "Authorization failed"
		else:
			print "Authorization granted"

	# Login
	if fb.login("1") is not 0:
		print "Login failed"
	else:
		print "Login success"

	# Call List
	call_list = fb.get_call_list()
	print call_list

if __name__ == '__main__':
	main()

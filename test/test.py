import sys
sys.path.append('..')
from pyfree import freebox


def main():
	fb = freebox()
	print "====================================="
	print "Device name = " + fb.device_name
	print "uid         = " + fb.uid
	print "api_version = " + fb.api_version
	print "device_type = " + fb.device_type
	print "====================================="

if __name__ == '__main__':
	main()

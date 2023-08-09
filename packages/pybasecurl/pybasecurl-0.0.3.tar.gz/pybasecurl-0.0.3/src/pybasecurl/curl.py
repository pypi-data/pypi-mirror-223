from subprocess import Popen, PIPE
import sys

def curl(url):
	try:
		print(f"URL: {url}")
		return Popen(['curl', url], stdout=PIPE, stderr=PIPE)
	except OSError as err:
		print(f"Error: {err}")
		sys.exit(1)
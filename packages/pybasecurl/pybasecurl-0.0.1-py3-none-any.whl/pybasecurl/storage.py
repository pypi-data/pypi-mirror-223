import sys

def save_data(stream, outfile):
	try:
		file = open(outfile, 'wb+')
		file.write(stream.read())
		file.close()
	except OSError as err:
		print(f"Can not open file! {err}")
		sys.exit(1)
	else:
		print("Done")

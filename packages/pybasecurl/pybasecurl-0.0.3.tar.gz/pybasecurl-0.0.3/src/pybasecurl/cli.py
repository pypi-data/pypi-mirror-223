from argparse import Action, ArgumentParser

class DriverAction(Action):
	def __call__(self, parser, namespace, values, option_string=None):
		file_path = values[0]
		namespace.file_path = file_path.lower()		

def create_parser():
	parser = ArgumentParser(description="""
		HTTP Request CLI Tool for downloading data/websites
	""")

	parser.add_argument("url", help="URL of the website need to get")
	parser.add_argument("--output", help="local file path to save the website", 
			nargs=1,
			action=DriverAction,
			required=True)

	return parser
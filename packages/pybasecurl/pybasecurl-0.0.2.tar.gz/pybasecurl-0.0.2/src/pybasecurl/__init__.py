def main():
	"""Entry point for the application script"""
	from pybasecurl import cli, curl, storage

	args = cli.create_parser().parse_args()
	print(f"args: {args} {args.url}")
	std_out, std_error = curl.curl(args.url).communicate()
	if std_error:
		print(f"Error : {std_error}")
		return
	if args.file_path:
		# write file
		storage.save_data(std_out, args.file_path)
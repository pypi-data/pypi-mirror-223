def main():
	"""Entry point for the application script"""
	from pybasecurl import cli, curl, storage

	args = cli.create_parser().parse_args()
	print(f"args: {args} {args.url}")
	std_out, std_error = curl.curl(args.url).communicate()
	if std_out and args.file_path:
		print(f"Output: {std_out}")
		# write file
		storage.save_data(std_out, args.file_path)
	elif std_error:
		print(f"Error : {std_error}")		
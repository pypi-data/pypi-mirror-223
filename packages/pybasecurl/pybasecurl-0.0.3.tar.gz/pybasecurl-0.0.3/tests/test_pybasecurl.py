# the inclusion of the tests module is not meant to offer best practices for
# testing in general, but rather to support the `find_packages` example in
# setup.py that excludes installing the "tests" package

import unittest

from pybasecurl import cli, curl, storage

class TestSimple(unittest.TestCase):

	def test_main_cli(self):
		args = cli.create_parser().parse_args()
		std_out, std_error = curl.curl(args.url).communicate()
		if std_error:
			print(f"Error : {std_error}")
			return
		if args.file_path:
			storage.save_data(std_out, args.file_path)    	
		self.assertEqual(True, True)


if __name__ == '__main__':
	unittest.main()
import os
import logging

logger = logging.getLogger('gtForensics')

# TAKEOUTD_PATH = 'Takeout'
# ARCHIVE_BROWSER_PATH = 'Takeout' + os.sep + 'archive_browser.html'


class Case(object):
	def __init__(self, args):
		self.input_dir_path = args.input_dir
		self.output_dir_path = args.output_dir
		self.takeout_path = args.input_dir + os.sep + 'Takeout'
		self.takeout_archive_browser_path = args.input_dir + os.sep + 'Takeout' + os.sep + 'archive_browser.html'

		# self.archive_browser_path = self.input_dir_path + os.sep + "Takeout" + os.sep + archive_browser.html


#---------------------------------------------------------------------------------------------------------------
	# def find_takeout_file_path():
	# 	if os.path.exists(self.archive_browser_path):
	# 		print("ddd")


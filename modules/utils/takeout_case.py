import os
import logging

logger = logging.getLogger('gtForensics')

# TAKEOUTD_PATH = 'Takeout'
# ARCHIVE_BROWSER_PATH = 'Takeout' + os.sep + 'archive_browser.html'
ANDROID_DEVICE_CONFIGURATION_SERVICE_PATH = 'Android Device Configuration Service'
MY_ACTIVITY_ASSISTANT_PATH = 'My Activity' + os.sep + 'Assistant' + os.sep + 'MyActivity.html'
MY_ACTIVITY_GMAIL_PATH = 'My Activity' + os.sep + 'Gmail' + os.sep + 'MyActivity.html'
MY_ACTIVITY_GOOGLE_ANALYTICS_PATH = 'My Activity' + os.sep + 'Google Analytics' + os.sep + 'MyActivity.html'
MY_ACTIVITY_YOUTUBE_PATH = 'My Activity' + os.sep + 'YouTube' + os.sep + 'MyActivity.html'

class Case(object):
	def __init__(self, args):
		self.input_dir_path = args.input_dir
		self.output_dir_path = args.output_dir
		self.takeout_path = args.input_dir + os.sep + 'Takeout'
		self.takeout_android_device_configuration_service_path = self.takeout_path + os.sep + ANDROID_DEVICE_CONFIGURATION_SERVICE_PATH
		self.takeout_my_activity_assistant_path = self.takeout_path + os.sep + MY_ACTIVITY_ASSISTANT_PATH
		self.takeout_my_activity_gmail_path = self.takeout_path + os.sep + MY_ACTIVITY_GMAIL_PATH
		self.takeout_my_activity_google_analytics_path = self.takeout_path + os.sep + MY_ACTIVITY_GOOGLE_ANALYTICS_PATH
		self.takeout_my_activity_youtube_path = self.takeout_path + os.sep + MY_ACTIVITY_YOUTUBE_PATH

		self.takeout_archive_browser_path = args.input_dir + os.sep + 'Takeout' + os.sep + 'archive_browser.html'

		# self.archive_browser_path = self.input_dir_path + os.sep + "Takeout" + os.sep + archive_browser.html


#---------------------------------------------------------------------------------------------------------------
	def find_takeout_file_path(self):
		if os.path.exists(self.takeout_path) == False:
			logger.error('Takeout data not exist.')
			return False

		# takout_service_dirs = os.listdir(self.takeout_path)
		# for root, dirs, files in os.walk(self.takeout_path):
			# print("root: ", root)
			# print("dirs: ", dirs)
			# print("files: ", files)



		# if takout_service_dirs == []:
		# 	logger.error('Takeout data not exist.')
		# 	return False

		# print(takout_service_dirs)





	# def find_takeout_file_path():
	# 	if os.path.exists(self.archive_browser_path):
	# 		print("ddd")


import os
import logging
from modules.utils.takeout_sqlite3 import SQLite3
import multiprocessing

logger = logging.getLogger('gtForensics')

# TAKEOUTD_PATH = 'Takeout'
# ARCHIVE_BROWSER_PATH = 'Takeout' + os.sep + 'archive_browser.html'
ANDROID_DEVICE_CONFIGURATION_SERVICE_PATH = 'Android Device Configuration Service'
MY_ACTIVITY_ASSISTANT_PATH = 'My Activity' + os.sep + 'Assistant' + os.sep + 'MyActivity.html'
MY_ACTIVITY_GMAIL_PATH = 'My Activity' + os.sep + 'Gmail' + os.sep + 'MyActivity.html'
MY_ACTIVITY_GOOGLE_ANALYTICS_PATH = 'My Activity' + os.sep + 'Google Analytics' + os.sep + 'MyActivity.html'
MY_ACTIVITY_YOUTUBE_PATH = 'My Activity' + os.sep + 'YouTube' + os.sep + 'MyActivity.html'
MY_ACTIVITY_VIDEO_SEARCH_PATH = 'My Activity' + os.sep + 'Video Search' + os.sep + 'MyActivity.html'
MY_ACTIVITY_VOICE_AUDIO_PATH = 'My Activity' + os.sep + 'Voice and Audio' + os.sep + 'MyActivity.html'
MY_ACTIVITY_MAPS_PATH = 'My Activity' + os.sep + 'Maps' + os.sep + 'MyActivity.html'
MY_ACTIVITY_ANDROID_PATH = 'My Activity' + os.sep + 'Android' + os.sep + 'MyActivity.html'

class Case(object):
	def __init__(self, args):
		self.number_of_system_processes = 0
		self.number_of_input_processes = args.number_process
		self.input_dir_path = args.input_dir
		self.output_dir_path = args.output_dir
		self.takeout_path = args.input_dir + os.sep + 'Takeout'

		# self.archive_browser_path = self.input_dir_path + os.sep + "Takeout" + os.sep + archive_browser.html

#---------------------------------------------------------------------------------------------------------------
	def check_number_process(self):
		self.number_of_system_processes = multiprocessing.cpu_count()
		if self.number_of_input_processes == None:
			self.number_of_input_processes = 1
		else:
			self.number_of_input_processes = int(self.number_of_input_processes)
			if self.number_of_input_processes > self.number_of_system_processes:
				return False

#---------------------------------------------------------------------------------------------------------------
	def set_file_path(self):
		if os.path.exists(self.takeout_path) == False:
			logger.error('Takeout data not exist.')
			return False

		if self.input_dir_path[-1] == os.sep:
			self.input_dir_path = self.input_dir_path[:-1]
		if self.output_dir_path[-1] == os.sep:
			self.output_dir_path = self.output_dir_path[:-1]

		self.takeout_android_device_configuration_service_path = self.takeout_path + os.sep + ANDROID_DEVICE_CONFIGURATION_SERVICE_PATH
		self.takeout_my_activity_assistant_path = self.takeout_path + os.sep + MY_ACTIVITY_ASSISTANT_PATH
		self.takeout_my_activity_gmail_path = self.takeout_path + os.sep + MY_ACTIVITY_GMAIL_PATH
		self.takeout_my_activity_google_analytics_path = self.takeout_path + os.sep + MY_ACTIVITY_GOOGLE_ANALYTICS_PATH
		self.takeout_my_activity_youtube_path = self.takeout_path + os.sep + MY_ACTIVITY_YOUTUBE_PATH
		self.takeout_my_activity_video_search_path = self.takeout_path + os.sep + MY_ACTIVITY_VIDEO_SEARCH_PATH
		self.takeout_my_activity_voice_audio_path = self.takeout_path + os.sep + MY_ACTIVITY_VOICE_AUDIO_PATH
		self.takeout_my_activity_maps_path = self.takeout_path + os.sep + MY_ACTIVITY_MAPS_PATH
		self.takeout_my_activity_android_path = self.takeout_path + os.sep + MY_ACTIVITY_ANDROID_PATH

		# self.takeout_archive_browser_path = args.input_dir + os.sep + 'Takeout' + os.sep + 'archive_browser.html'

		self.output_dir_path = self.output_dir_path + os.sep + os.path.basename(self.input_dir_path)
		self.analysis_db_path = self.output_dir_path + os.sep + 'analysis_' + os.path.basename(self.input_dir_path) + '.db'

		if os.path.exists(self.output_dir_path) == False:
			os.makedirs(self.output_dir_path)

		# print(self.output_dir_path)
		# print(self.analysis_db_path)

#---------------------------------------------------------------------------------------------------------------
	def create_analysis_db(self):
		# if os.path.exists(self.analysis_db_path):
		# 	print("exist")
		# 	ret = SQLite3.is_exist_table('parse_my_activity_assistant', self.analysis_db_path)
		# 	print('table: ', ret)
			# return self.analysis_db_path

		list_query = list()
		# query_create_parse_my_activity_assistant = "CREATE TABLE parse_my_activity_assistant (service TEXT, timestamp INTEGER, type TEXT, keyword TEXT, url TEXT, geodata_latitude TEXT, geodata_longitude TEXT, geodata_description TEXT, attachment_voice_file TEXT)"
		query_create_parse_my_activity_assistant = "CREATE TABLE IF NOT EXISTS parse_my_activity_assistant (service TEXT, timestamp INTEGER, type TEXT, keyword TEXT, url TEXT, geodata_latitude TEXT, geodata_longitude TEXT, geodata_description TEXT, attachment_voice_file TEXT)"
		query_create_parse_my_activity_gmail = "CREATE TABLE IF NOT EXISTS parse_my_activity_gmail (service TEXT, timestamp INTEGER, type TEXT, keyword TEXT, url TEXT)"
		query_create_parse_my_activity_analytics = "CREATE TABLE IF NOT EXISTS parse_my_activity_analytics (service TEXT, timestamp INTEGER, type TEXT, keyword TEXT, url TEXT)"
		query_create_parse_my_activity_youtube = "CREATE TABLE IF NOT EXISTS parse_my_activity_youtube (service TEXT, timestamp INTEGER, type TEXT, keyword TEXT, url TEXT, channel_name TEXT, channel_url TEXT)"
		query_create_parse_my_activity_video_search = "CREATE TABLE IF NOT EXISTS parse_my_activity_video_search (service TEXT, timestamp INTEGER, type TEXT, search_service TEXT, keyword TEXT, url TEXT)"
		query_create_parse_my_activity_voice_audio = "CREATE TABLE IF NOT EXISTS parse_my_activity_voice_audio (service TEXT, timestamp INTEGER, type TEXT, keyword TEXT, url TEXT, attachment_voice_file TEXT)"
		query_create_parse_my_activity_map = "CREATE TABLE IF NOT EXISTS parse_my_activity_map (service TEXT, timestamp INTEGER, type TEXT, keyword TEXT, url TEXT, search_location TEXT, geodata_search_latitude TEXT, geodata_search_longitude TEXT, geodata_latitude TEXT, geodata_longitude TEXT, geodata_description TEXT)"
		query_create_parse_my_activity_android = "CREATE TABLE IF NOT EXISTS parse_my_activity_android (service TEXT, timestamp INTEGER, type TEXT, keyword TEXT, url TEXT, package_name TEXT)"


		# dic_my_activity_assistant = {'service':"", 'type':"", 'url':"", 'keyword':"", 'answer':"", 'timestamp':"", 'geodata_latitude':"", 'geodata_longitude':"", 'geodata_description':"", 'attachment_voice_file':""}

		# query_create_application_list_table = "CREATE TABLE application_list (is_deleted INTEGER, category TEXT, package_name TEXT, app_name TEXT, version TEXT, installed_time INTEGER, apk_changed_time INTEGER, updated_time INTEGER, deleted_time INTEGER, fs_ctime INTEGER, fs_crtime INTEGER, fs_atime INTEGER, fs_mtime INTEGER, is_updated INTEGER, source TEXT)"
		# query_create_id_password_hash_table = "CREATE TABLE id_password_hash (package_name TEXT, url TEXT, account TEXT, pwd TEXT, contents TEXT, timestamp TEXT, source TEXT)"
		# query_create_call_history_table = "CREATE TABLE call_history (package_name TEXT, timestamp TEXT, time_duration TEXT, phonenumber TEXT, account TEXT, digit_positive TEXT, file TEXT, contents TEXT, source TEXT)"
		# query_create_geodata_table = "CREATE TABLE geodata (package_name TEXT, timestamp TEXT, geodata TEXT, file TEXT, contents TEXT, source TEXT)"
		# query_create_web_brwoser_history_table = "CREATE TABLE web_browser_history (package_name TEXT, timestamp TEXT, url TEXT, account TEXT, digit_positive TEXT, file TEXT, contents TEXT, source TEXT)"
		# query_create_file_history_table = "CREATE TABLE file_history (package_name TEXT, timestamp TEXT, file TEXT, phonenumber TEXT, account TEXT, contents TEXT, source TEXT)"
		# query_create_embedded_filetable = "CREATE TABLE embedded_file (is_compressed INTEGER, parent_path TEXT, name TEXT, extension TEXT, mod_time TEXT, size INTEGER, compressed_size INTEGER, CRC INTEGER, create_system TEXT, source_path TEXT, source TEXT)"



		list_query.append(query_create_parse_my_activity_assistant)
		list_query.append(query_create_parse_my_activity_gmail)
		list_query.append(query_create_parse_my_activity_analytics)
		list_query.append(query_create_parse_my_activity_youtube)
		list_query.append(query_create_parse_my_activity_video_search)
		list_query.append(query_create_parse_my_activity_voice_audio)
		list_query.append(query_create_parse_my_activity_map)
		list_query.append(query_create_parse_my_activity_android)


		# list_query.append(query_create_application_list_table)
		# list_query.append(query_create_id_password_hash_table)
		# list_query.append(query_create_call_history_table)
		# list_query.append(query_create_geodata_table)
		# list_query.append(query_create_web_brwoser_history_table)
		# list_query.append(query_create_file_history_table)
		# list_query.append(query_create_embedded_filetable)

		SQLite3.execute_commit_query(list_query, self.analysis_db_path)


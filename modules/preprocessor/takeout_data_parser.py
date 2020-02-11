import os
import logging
# from modules.preprocessor.takeout_parse_android-device-configuration-service import AndroidDeviceConfigurationService

from modules.preprocessor.takeout_parse_android_device_configuration_service import AndroidDeviceConfigurationService
from modules.preprocessor.takeout_parse_myactivity_assistant import MyActivityAssistant
from modules.preprocessor.takeout_parse_myactivity_gmail import MyActivityGmail
from modules.preprocessor.takeout_parse_myactivity_google_analytics import MyActivityGoogleAnalytics
from modules.preprocessor.takeout_parse_myactivity_youtube import MyActivityYouTube
from modules.preprocessor.takeout_parse_myactivity_video_search import MyActivityVideoSearch
from modules.preprocessor.takeout_parse_myactivity_voice_audio import MyActivityVoiceAudio
from modules.preprocessor.takeout_parse_myactivity_maps import MyActivityMaps

logger = logging.getLogger('gtForensics')

class DataParser(object):
	def parse_takeout_data(case):
		# AndroidDeviceConfigurationService.parse_device_info(case)

		if os.path.exists(case.takeout_my_activity_assistant_path):
			MyActivityAssistant.parse_assistant(case)

		if os.path.exists(case.takeout_my_activity_gmail_path):
			MyActivityGmail.parse_gmail(case)

		if os.path.exists(case.takeout_my_activity_google_analytics_path):
			MyActivityGoogleAnalytics.parse_google_analytics(case)

		if os.path.exists(case.takeout_my_activity_youtube_path):
			MyActivityYouTube.parse_youtube(case)

		# if os.path.exists(case.takeout_my_activity_video_search_path):
		# 	MyActivityVideoSearch.parse_video_search(case)

		# if os.path.exists(case.takeout_my_activity_voice_audio_path):
		# 	MyActivityVoiceAudio.parse_voice_audio(case)

		# if os.path.exists(case.takeout_my_activity_maps_path):
		# 	MyActivityMaps.parse_maps(case)

		# print("aaa")

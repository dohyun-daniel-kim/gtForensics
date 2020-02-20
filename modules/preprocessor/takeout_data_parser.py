import os
import logging
# from modules.preprocessor.takeout_parse_android-device-configuration-service import AndroidDeviceConfigurationService

from modules.preprocessor.takeout_parse_android_device_configuration_service import AndroidDeviceConfigurationService
from modules.preprocessor.takeout_parse_contacts import Contacts
from modules.preprocessor.takeout_parse_drive import Drive
from modules.preprocessor.takeout_parse_hangouts import Hangouts
from modules.preprocessor.takeout_parse_location_history import LocationHistory

from modules.preprocessor.takeout_parse_myactivity_android import MyActivityAndroid
from modules.preprocessor.takeout_parse_myactivity_assistant import MyActivityAssistant
from modules.preprocessor.takeout_parse_myactivity_gmail import MyActivityGmail
from modules.preprocessor.takeout_parse_myactivity_chrome import MyActivityChrome
from modules.preprocessor.takeout_parse_myactivity_google_analytics import MyActivityGoogleAnalytics
from modules.preprocessor.takeout_parse_myactivity_maps import MyActivityMaps
from modules.preprocessor.takeout_parse_myactivity_video_search import MyActivityVideoSearch
from modules.preprocessor.takeout_parse_myactivity_voice_audio import MyActivityVoiceAudio
from modules.preprocessor.takeout_parse_myactivity_youtube import MyActivityYouTube


logger = logging.getLogger('gtForensics')

class DataParser(object):
	def parse_takeout_data(case):
		# Takeout -----------------------------------------------------------------------------------------------------
		# if os.path.exists(case.takeout_android_device_configuration_service_path):
		# 	AndroidDeviceConfigurationService.parse_device_info(case)
		
		Contacts.parse_contacts(case)
		Drive.parse_drive(case)
		
		# Hangouts.parse_hangouts(case)
		
		# LocationHistory.parse_location_history(case)



		# Takeout My Activity -----------------------------------------------------------------------------------------
		MyActivityAndroid.parse_android(case)
		MyActivityAssistant.parse_assistant(case)
		MyActivityGmail.parse_gmail(case)
		MyActivityChrome.parse_chrome(case)
		MyActivityGoogleAnalytics.parse_google_analytics(case)
		MyActivityMaps.parse_maps(case)
		MyActivityVideoSearch.parse_video_search(case)
		MyActivityVoiceAudio.parse_voice_audio(case)
		MyActivityYouTube.parse_youtube(case)


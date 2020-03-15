import os
import logging
# from modules.preprocessor.takeout_parse_android-device-configuration-service import AndroidDeviceConfigurationService

from modules.preprocessor.takeout_parse_android_device_configuration_service import AndroidDeviceConfigurationService

from modules.preprocessor.takeout_parse_chrome import Chrome

from modules.preprocessor.takeout_parse_contacts import Contacts
from modules.preprocessor.takeout_parse_drive import Drive
from modules.preprocessor.takeout_parse_google_photo import GooglePhoto
from modules.preprocessor.takeout_parse_location_history import LocationHistory
from modules.preprocessor.takeout_parse_semantic_location_history import SemanticLocationHistory



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
		#--- working........
		# if os.path.exists(case.takeout_android_device_configuration_service_path):
		# 	AndroidDeviceConfigurationService.parse_device_info(case)
		#--- working........


		Chrome.parse_browser_history(case)
		Contacts.parse_contacts(case)
		Drive.parse_drive(case)
		GooglePhoto.parse_google_photo(case)
		LocationHistory.parse_location_history(case)
		SemanticLocationHistory.parse_activity_place(case)
		
		#--- working........
		# Hangouts.parse_hangouts(case)		
		# LocationHistory.parse_location_history(case)
		#--- working........


		# Takeout My Activity -----------------------------------------------------------------------------------------
		MyActivityAndroid.parse_android(case)
		MyActivityAssistant.parse_assistant(case)
		MyActivityChrome.parse_chrome(case)
		MyActivityGmail.parse_gmail(case)
		MyActivityGoogleAnalytics.parse_google_analytics(case)
		MyActivityMaps.parse_maps(case)
		MyActivityVideoSearch.parse_video_search(case)
		MyActivityVoiceAudio.parse_voice_audio(case)
		MyActivityYouTube.parse_youtube(case)


import os

# from modules.preprocessor.takeout_parse_android-device-configuration-service import AndroidDeviceConfigurationService

from modules.preprocessor.takeout_parse_android_device_configuration_service import AndroidDeviceConfigurationService
from modules.preprocessor.takeout_parse_myactivity_assistant import MyActivityAssistant


class DataParser(object):
	def parse_takeout_data(case):
		# AndroidDeviceConfigurationService.parse_device_info(case)

		if os.path.exists(case.takeout_my_activity_assistant_path):
			MyActivityAssistant.parse_assistant_said(case)
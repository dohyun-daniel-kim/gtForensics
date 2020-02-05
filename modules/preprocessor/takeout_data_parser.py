

# from modules.preprocessor.takeout_parse_android-device-configuration-service import AndroidDeviceConfigurationService

from modules.preprocessor.takeout_parse_android_device_configuration_service import AndroidDeviceConfigurationService


class DataParser(object):
	def parse_takeout_data(case):
		AndroidDeviceConfigurationService.parse_device_info(case)		

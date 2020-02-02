

from modules.preprocessor.takeout_parse_android-device-configuration-service import AndroidDeviceConfigurationService


class DataParser(object):
	def parse_takeout_data(case):
		AndroidDeviceConfigurationService.parse_device_info(case)

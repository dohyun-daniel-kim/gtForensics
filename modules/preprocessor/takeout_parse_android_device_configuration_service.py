import os
import logging
# from bs4 import BeautifulSoup
# from lxml import html
# from lxml import etree
# import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
from urllib.parse import urlparse, unquote
from modules.utils.takeout_html_parser import TakeoutHtmlParser
from modules.utils.takeout_sqlite3 import SQLite3
from tqdm import trange

# ANDROID_DEVICE_CONFIGURATION_SERVICE_PATH = 'Android Device Configuration Service'

logger = logging.getLogger('gtForensics')


class AndroidDeviceConfigurationService(object):
	def parse_network_info

#---------------------------------------------------------------------------------------------------------------	
	def parse_system_software_info

#---------------------------------------------------------------------------------------------------------------	
	def parse_device_attrib

#---------------------------------------------------------------------------------------------------------------
	def parse_device_account_info

#---------------------------------------------------------------------------------------------------------------	
	def parse_device_info(case):
		# print("input dir: ", case.takeout_android_device_configuration_service_path)
		list_target_files = os.listdir(case.takeout_android_device_configuration_service_path)
		if list_target_files == []:
			logger.error('Takeout data not exist.')
			return False
		for file_name in list_target_files:
			if file_name.startswith('Device-') == False:
				continue

			file_path = case.takeout_android_device_configuration_service_path + os.sep + file_name

			with open(file_path, 'r', encoding='utf-8') as f:
				file_contents = f.read()
				soup = BeautifulSoup(file_contents, 'lxml')
				list_device_conf_logs = TakeoutHtmlParser.find_category_title(soup)
				print(list_device_conf_logs)



			# print("file_path: ", file_path)

			# soup = BeautifulSoup(file_path, 'html.parser')
			# dt = soup.find(class_ ={"category-title"})
			# print(dt)




			# tree = ET.parse(file_path)
			# root = tree.getroot()
			# parser = etree.HTMLParser()
			# tree = etree.parse(file_path, parser)
			# root = tree.getroot()
			# if root.tag == 'html':
			# 	print('root.tag: ', root.tag)
			# 	for component in root.iter('div'):
			# 		print('component: ', component.tag)


					# for item in component.iter('Android'):
					# 	print(itme)
					# 	print(item.xpath('text()'))


					# tmp = component.xpath('text()')

			# elements = tree.xpath('//div[@class="title"]/text()')
			# elements = tree.xpath('//h3[@class="category-title"]')
			# print(elements.text)


			# elements = tree.xpath('//h3[@class="category-title"]')
			# print(elements)

			# # tmp = elements[0].xpath('Android ID:')
			# # print(tmp)


			# print(elements)
			# if elements == 'Device and Account Identifiers':
			# 	print(elements)





			# result = etree.tostring(tree.getroot(), pretty_print=True, method="html")
			# print(result)
			# with open(file_path, 'r') as file:
			# 	# root = etree.parse(file_path)
			# 	dom = html.fromstring(file.read())
				# title = dom.xpath('//h3[@class="category-title"]/text()')
				# print(title)

			# 	print("file")
			# 	tree = et.parse(file_path)







		# files = os.listdir(case.takeout_path + os.sep + 'Android Device Configuration Service')
		# for file in files:
		# 	if file.startswith('Device-') and file.endswith('.html'):

		# print("parse_device_info")


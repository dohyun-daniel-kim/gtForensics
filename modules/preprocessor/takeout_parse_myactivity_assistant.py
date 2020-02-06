import os
import logging
# from lxml import html

from bs4 import BeautifulSoup
import time
from urllib.parse import urlparse


# import xml.etree.ElementTree as et
# from lxml import etree

# from bs4 import BeautifulSoup
# from lxml import html
# from lxml import etree
# import xml.etree.ElementTree as ET

logger = logging.getLogger('gtForensics')

class MyActivityAssistant(object):
    def parse_assistant_said(case):
        file_path = case.takeout_my_activity_assistant_path
        print("my activity assistant")
        print("file_path: ", file_path)

        with open(file_path, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')
            list_assistant_logs = soup.find_all('div', class_ ={"outer-cell mdl-cell mdl-cell--12-col mdl-shadow--2dp"})
            if list_assistant_logs != []:
                for assistant_logs in list_assistant_logs:
                    print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
                    dic_my_activity_assistant = {'type':"", 'url':"", 'keyword':"", 'timestamp':"", 'geodata_latitude':"", 'geodata_longitude':"", 'geodata_description':""}
                    # print(assistant_logs)

                    list_assistant_search_logs = assistant_logs.find('div', class_ ={"content-cell mdl-cell mdl-cell--6-col mdl-typography--body-1"})
                    if list_assistant_search_logs != []:
                        for content in list_assistant_search_logs:
                            # print("----------------------------------------------")
                            content = str(content).strip()
                            # print(content)
                            if content == '<br/>':  continue
                            if content == 'Said':
                                dic_my_activity_assistant['type'] = 'Assistant Search'
                            elif content.startswith('<a href="'):
                                idx = content.find('">')
                                dic_my_activity_assistant['url'] = content[9:idx]
                                dic_my_activity_assistant['keyword'] = content[idx+2:content.find('</a>')]
                            elif content.endswith('UTC'):
                                dic_my_activity_assistant['timestamp'] = content

                    list_assistant_geodata_logs = assistant_logs.find('div', class_ ={"content-cell mdl-cell mdl-cell--12-col mdl-typography--caption"})
                    if list_assistant_geodata_logs != []:
                        for content in list_assistant_geodata_logs:
                            print("----------------------------------------------")
                            content = str(content).strip()
                            if content == '<br/>':  continue
                            if content.startswith('<a href="https://www.google.com/maps/'):
                                idx = content.find('">')
                                url = content[9:idx]

                                o = urlparse(url)
                                print('query: ', o.query)
                                if o.query.find(';center'):
                                    print('center: ', o.query)
                                elif o.query.find(';query'):
                                    print('query: ', o.query)
                                else:
                                    print('unknown: ', o.query)



                                # print(content)
                                # print(url)
                                # print(o.geturl())
                                # print(o.query)
                                # print(o.fragment)

                                # idx_start = content.find('center=')
                                # idx_end = content.find('center=')
                                # latitude = content[]
                                
                                


                            # print(content)



                    # print(dic_my_activity_assistant)




                        # for log in list_assistant_search_logs:
                            # print("----------------------------------------------")
                            # print(len(log))
                            # print(log)


                            # dic_my_activity_assistant = {'type':"", 'url':"", 'keyword':"", 'timestamp':""}
                            # list_log = log.contents
                            # # print(len(list_log))
                            # for content in list_log:
                            #     content = str(content).strip()
                            #     # print(content)
                            #     # if content == '<br/>':  continue
                            #     if content == 'Said':
                            #         dic_my_activity_assistant['type'] = 'Assistant Search'
                            #     elif content.startswith('<a href="'):
                            #         idx = content.find('">')
                            #         dic_my_activity_assistant['url'] = content[9:idx]
                            #         dic_my_activity_assistant['keyword'] = content[idx+2:content.find('</a>')]
                            #     elif content.endswith('UTC'):
                            #         dic_my_activity_assistant['timestamp'] = content
                    # print(log)
                    # print(dic_my_activity_assistant)

            # list_assistant_location_logs = soup.find_all('div', class_ ={"content-cell mdl-cell mdl-cell--12-col mdl-typography--caption"})
            # if list_assistant_location_logs != []:
            #     for log in list_assistant_location_logs:
            #         print("----------------------------------------------")
            #         print(log)
            #         print("----------------------------------------------")





# content-cell mdl-cell mdl-cell--12-col mdl-typography--caption


                #     # if content.find('<br/>'): continue
                #     # print(content)
                #     print(content)
                #     # if content.find('Said'):



                # print("----------------------------------------------")













                # print(item.contents[1])
                # print(item.get('class'))

                # print(item.attrib)








            # print("--------------------")
            # dt = soup.find(class_ ={"content-cell mdl-cell mdl-cell--6-col mdl-typography--body-1"})
            # print(dt)
            # print(dt.text.strip())
            # print("--------------------")
            # print(dt.text.strip())

            # print("--------------------")




        # with open(file_path, 'r', encoding='utf-8') as f:
        #     tree = html.parse(f)
        #     root = tree.getroot()
        #     for child in root.iter('html'):
        #         for child2 in child.iter('body'):
        #             # for child3 in child2.iter('a'):
        #             #     print(child3.items())


        #             for child3 in child2.iter('div'):
        #                 # if child3.text == "Said":
        #                 #     print("aa")
        #                 # for child4 in child3.iter('a'):
        #                 #     print(child4.text)


        #                 if child3.get('class') == 'content-cell mdl-cell mdl-cell--6-col mdl-typography--body-1':
        #                     tmp = child3.text.strip()
        #                     print(tmp)
        #                     print(tmp.encode("utf8"))
        #                     print(tmp.decode("utf8"))

                            # print(child3.getchildren())
                            # if child3.find("Said"):
                        # item = child3.get('class') == 'content-cell mdl-cell mdl-cell--6-col mdl-typography--body-1'
                        # print(item)
                        # for child4 in child3.iter('br'):
                        #     print(child4.items())









                        # print(child3.attrib["content-cell mdl-cell mdl-cell--6-col mdl-typography--body-1"])
                        # if child3.get('class') == 'content-cell mdl-cell mdl-cell--6-col mdl-typography--body-1':

                        # print(child3)
                        # if child3.get('class') == 'content-cell mdl-cell mdl-cell--6-col mdl-typography--body-1':
                            # for item in child3.getchildren():
                            #     print(item)

                            # print(child3.getchildren())

                            # tmp = child3.getchildren()[0].text
                            # print(type(tmp))
                            # # unicode(tmp)
                            # print(tmp)
                            # print(tmp.encode("utf8"))


                            # tmp.unicode(encoding='UTF-8',errors='strict')
                            # print(tmp.decode(encoding='UTF-8',errors='strict'))
                            # print(child3.getchildren()[0].text)

                        # if child3.attrib["content-cell mdl-cell mdl-cell--6-col mdl-typography--body-1"]:
                        #     print("aa")
                        # print(child3.get('class'))
                        # print(child3.items()[0][1])
                        # tmp = child3.get('{class="content-cell mdl-cell mdl-cell--6-col mdl-typography--body-1"}')

                        # print(child3.items()[0][1])
                        # print(child3.get('header-cell mdl-cell mdl-cell--12-col'))
                        # print(child3.get(child3.items()[0][1]))
                        # print('child3.attrib: ', child3.attrib)

                        # print(type(child3.attrib))
                        # print('child3.attrib: ', child3.attrib)
                        # if child3.attrib.find('cass'):
                        #     print(type(child3.attrib))
                        # if child3.attrib == 'content-cell mdl-cell mdl-cell--6-col mdl-typography--body-1':
                            # print('content-cell mdl-cell mdl-cell--6-col mdl-typography--body-1')
                        # elif child3.attrib == 'content-cell mdl-cell mdl-cell--6-col mdl-typography--body-1':
                        #     print('content-cell mdl-cell mdl-cell--6-col mdl-typography--body-1')


                        # # print('root.tag: ', root.tag)
                        # # print('root.attrib: ', root.attrib)
                        # # print('child.tag: ', child.tag)
                        # # print('child.attrib: ', child.attrib)
                        # # print('child2.tag: ', child2.tag)
                        # # print('child2.attrib: ', child2.attrib)
                        # print('child3.tag: ', child3.tag)
                        # print('child3.attrib: ', child3.attrib)


            # print(root)


            # html_info = et.fromstring(f.read())
            # html_info = html.fromstring(f.read())
            # print(type(html_info))
            # {http://www.w3.org/1999/xhtml}







        # parser = etree.HTMLParser()
        # tree = etree.parse(file_path, parser)
        # root = tree.getroot()
        # if root.tag == 'html':
        #     print('root.tag: ', root.tag)
        #     for component in root.iter('p'):
        #         print('component.tag: ', component.tag)
        #         print('component: ', component.get('div class'))

    # def parse_device_info(case):
	# 	print("input dir: ", case.takeout_android_device_configuration_service_path)
	# 	list_target_files = os.listdir(case.takeout_android_device_configuration_service_path)
	# 	if list_target_files == []:
	# 		logger.error('Takeout data not exist.')
	# 		return False
	# 	for file_name in list_target_files:
	# 		if file_name.startswith('Device-') == False:
	# 			continue

	# 		file_path = case.takeout_android_device_configuration_service_path + os.sep + file_name
	# 		print("file_path: ", file_path)

			# soup = BeautifulSoup(file_path, 'html.parser')
			# dt = soup.find(class_ ={"category-title"})
			# print(dt)




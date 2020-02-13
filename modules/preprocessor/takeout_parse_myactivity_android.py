import os
import logging
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from modules.utils.takeout_html_parser import TakeoutHtmlParser
from modules.utils.takeout_sqlite3 import SQLite3
from tqdm import trange

logger = logging.getLogger('gtForensics')

class MyActivityAndroid(object):
    def parse_android_log_caption(dic_my_activity_android, android_logs):
        list_android_logs = TakeoutHtmlParser.find_log_caption(android_logs)
        if list_android_logs != []:
            for content in list_android_logs:
                content = str(content).strip()
                if content.startswith('This'):
                    dic_my_activity_android['keyword'] += ': ' + content

#---------------------------------------------------------------------------------------------------------------
    def parse_android_log_body(dic_my_activity_android, android_logs):
        list_android_event_logs = TakeoutHtmlParser.find_log_body(android_logs)
        if list_android_event_logs != []:
            idx = 0
            for content in list_android_event_logs:
                # print("----------------------------------------------")
                content = str(content).strip()
                content = content.replace(u'\xa0', ' ')
                # print(content)
                if idx == 0:
                    if content.startswith('Used'):
                        dic_my_activity_android['type'] = 'Use'
                        if len(content) >= 5 and content.find(' ') >= 1 :
                            keyword = content.split(' ')[1]
                            dic_my_activity_android['keyword'] = keyword
                            dic_my_activity_android['package_name'] = keyword

                    elif content.startswith('Interacted'):
                        dic_my_activity_android['type'] = 'Interact'
                        dic_my_activity_android['keyword'] = content
                    else:
                        dic_my_activity_android['type'] = content
                else:
                    if idx == 1:
                        if content.startswith('<a href="'):
                            idx2 = content.find('">')
                            # dic_my_activity_android['keyword'] = content[idx+2:content.find('</a>')].replace("\"", "\'")
                            dic_my_activity_android['keyword'] = content[idx2+2:content.find('</a>')].replace("\"", "\'").replace("&amp;", "&")
                            url = content[9:idx2]
                            dic_my_activity_android['url'] = url
                            o = urlparse(url)
                            if o.query.find('=') >= 1:
                                dic_my_activity_android['package_name'] = o.query.split('=')[1]
                    elif content.endswith('UTC'):
                        dic_my_activity_android['timestamp'] = TakeoutHtmlParser.convert_datetime_to_unixtime(content)
                idx += 1

#---------------------------------------------------------------------------------------------------------------
    def parse_android_log_title(dic_my_activity_android, android_logs):
        dic_my_activity_android['service'] = 'Android Usage'

#---------------------------------------------------------------------------------------------------------------
    def insert_log_info_to_analysis_db(dic_my_activity_android, analysis_db_path):
        query = 'INSERT INTO parse_my_activity_android \
                (service, timestamp, type, keyword, url, package_name) \
                VALUES("%s", %d, "%s", "%s", "%s", "%s")' % \
                (dic_my_activity_android['service'], int(dic_my_activity_android['timestamp']), dic_my_activity_android['type'], \
                dic_my_activity_android['keyword'], dic_my_activity_android['url'], dic_my_activity_android['package_name'])
        SQLite3.execute_commit_query(query, analysis_db_path)

#---------------------------------------------------------------------------------------------------------------
    def parse_android(case):
        file_path = case.takeout_my_activity_android_path
        # print("my activity android")
        # print("file_path: ", file_path)

        with open(file_path, 'r', encoding='utf-8') as f:
            file_contents = f.read()
            soup = BeautifulSoup(file_contents, 'lxml')
            list_android_logs = TakeoutHtmlParser.find_log(soup)
            print("loading finished.")
            if list_android_logs != []:
                for i in trange(len(list_android_logs), desc="[Parsing the My Activity -> Android data............]", unit="epoch"):
                # for voice_audio_logs in list_voice_audio_logs:
                    # print("..........................................................................")
                    dic_my_activity_android = {'service':"", 'type':"", 'url':"", 'keyword':"", 'timestamp':"", 'package_name':""}
                    MyActivityAndroid.parse_android_log_title(dic_my_activity_android, list_android_logs[i])
                    MyActivityAndroid.parse_android_log_body(dic_my_activity_android, list_android_logs[i])
                    MyActivityAndroid.parse_android_log_caption(dic_my_activity_android, list_android_logs[i])
                    MyActivityAndroid.insert_log_info_to_analysis_db(dic_my_activity_android, case.analysis_db_path)
                    # print(dic_my_activity_android)




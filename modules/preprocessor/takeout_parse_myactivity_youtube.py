import os
import logging
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from modules.utils.takeout_html_parser import TakeoutHtmlParser
from modules.utils.takeout_sqlite3 import SQLite3

logger = logging.getLogger('gtForensics')

class MyActivityYouTube(object):
    def parse_youtube_log_body(dic_my_activity_youtube, youtube_logs):
        list_youtube_event_logs = TakeoutHtmlParser.find_log_body(youtube_logs)
        if list_youtube_event_logs != []:
            idx = 0
            for content in list_youtube_event_logs:
                # print("----------------------------------------------")
                content = str(content).strip()
                content = content.replace(u'\xa0', ' ')
                # print(content)
                if idx == 0:
                    if content == 'Searched for':
                        dic_my_activity_youtube['type'] = 'Search'
                    elif content == 'Watched':
                        dic_my_activity_youtube['type'] = 'Watch'
                    elif content == 'Watched a video that has been removed':
                        dic_my_activity_youtube['type'] = 'Watch'
                        dic_my_activity_youtube['keyword'] ='Watched a video that has been removed'
                    elif content == 'Visited YouTube Music':
                        dic_my_activity_youtube['type'] = 'Visit'
                        dic_my_activity_youtube['keyword'] ='Visited YouTube Music'
                    else:
                        # print("!!! ", content)
                        dic_my_activity_youtube['type'] = content
                else:
                    if idx == 1:
                        if content.startswith('<a href="'):
                            idx = content.find('">')
                            dic_my_activity_youtube['url'] = content[9:idx]
                            # dic_my_activity_youtube['keyword'] = content[idx+2:content.find('</a>')]
                            dic_my_activity_youtube['keyword'] = content[idx+2:content.find('</a>')].replace("\"", "\'")
                    else:
                        if dic_my_activity_youtube['type'] == 'Watch':
                            if content.startswith('<a href="'):
                                idx = content.find('">')
                                dic_my_activity_youtube['channel_url'] = content[9:idx]
                                dic_my_activity_youtube['channel_name'] = content[idx+2:content.find('</a>')]
                        if content.endswith('UTC'):
                            dic_my_activity_youtube['timestamp'] = TakeoutHtmlParser.convert_datetime_to_unixtime(content)
                idx += 1

#---------------------------------------------------------------------------------------------------------------
    def parse_youtube_log_title(dic_my_activity_youtube, youtube_logs):
        list_youtube_title_logs = TakeoutHtmlParser.find_log_title(youtube_logs)
        if list_youtube_title_logs != []:
            for content in list_youtube_title_logs:
                content = str(content).strip()
                dic_my_activity_youtube['service'] = content.split('>')[1].split('<br')[0]

#---------------------------------------------------------------------------------------------------------------
    def insert_log_info_to_analysis_db(dic_my_activity_youtube, analysis_db_path):
        query = 'INSERT INTO parse_my_activity_youtube \
                (service, timestamp, type, keyword, url, channel_name, channel_url) \
                VALUES("%s", %d, "%s", "%s", "%s", "%s", "%s")' % \
                (dic_my_activity_youtube['service'], int(dic_my_activity_youtube['timestamp']), dic_my_activity_youtube['type'], \
                dic_my_activity_youtube['keyword'], dic_my_activity_youtube['url'], \
                dic_my_activity_youtube['channel_name'], dic_my_activity_youtube['channel_url'])
        SQLite3.execute_commit_query(query, analysis_db_path)


#---------------------------------------------------------------------------------------------------------------
    def parse_youtube(case):
        # print('youtube')
        file_path = case.takeout_my_activity_youtube_path
        with open(file_path, 'r', encoding='utf-8') as f:
            file_contents = f.read()
            soup = BeautifulSoup(file_contents, 'lxml')
            # soup = BeautifulSoup(f, 'html.parser')
            list_youtube_logs = TakeoutHtmlParser.find_log(soup)
            if list_youtube_logs != []:
                NUMBER_OF_PROCESSES = case.number_of_input_processes
                print('NUMBER_OF_PROCESSES: ', NUMBER_OF_PROCESSES)


                for youtube_logs in list_youtube_logs:
                    # print("..........................................................................")
                    dic_my_activity_youtube = {'service':"", 'type':"", 'url':"", 'keyword':"", 'channel_url':"", 'channel_name':"", 'timestamp':""}
                    MyActivityYouTube.parse_youtube_log_title(dic_my_activity_youtube, youtube_logs)
                    MyActivityYouTube.parse_youtube_log_body(dic_my_activity_youtube, youtube_logs)
                    # MyActivityYouTube.insert_log_info_to_analysis_db(dic_my_activity_youtube, case.analysis_db_path)
                    # print(dic_my_activity_youtube)

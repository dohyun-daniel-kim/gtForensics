import os
import logging
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from modules.utils.takeout_html_parser import TakeoutHtmlParser

logger = logging.getLogger('gtForensics')

class MyActivityVideoSearch(object):
    def parse_video_search_log_body(dic_my_activity_video_search, video_search_logs):
        list_video_search_event_logs = TakeoutHtmlParser.find_log_body(video_search_logs)
        if list_video_search_event_logs != []:
            idx = 0
            for content in list_video_search_event_logs:
                # print("----------------------------------------------")
                content = str(content).strip()
                content = content.replace(u'\xa0', ' ')
                # print(content)
                if idx == 0:
                    if content == 'Searched for':
                        dic_my_activity_video_search['type'] = 'Search'
                    elif content == 'Watched':
                        dic_my_activity_video_search['type'] = 'Watch'
                    else:
                        # print("!!! ", content)
                        dic_my_activity_video_search['type'] = content
                else:
                    if idx == 1:
                        if content.startswith('<a href="'):
                            idx = content.find('">')
                            dic_my_activity_video_search['url'] = content[9:idx]
                            dic_my_activity_video_search['keyword'] = content[idx+2:content.find('</a>')]
                    else:
                        if content.endswith('UTC'):
                            dic_my_activity_video_search['timestamp'] = TakeoutHtmlParser.convert_datetime_to_unixtime(content)
                idx += 1

#---------------------------------------------------------------------------------------------------------------
    def parse_video_search_log_title(dic_my_activity_video_search, video_search_logs):
        list_video_search_title_logs = TakeoutHtmlParser.find_log_title(video_search_logs)
        if list_video_search_title_logs != []:
            for content in list_video_search_title_logs:
                content = str(content).strip()
                dic_my_activity_video_search['service'] = content.split('>')[1].split('<br')[0]

#---------------------------------------------------------------------------------------------------------------
    def parse_video_search(case):
        print('video search')
        file_path = case.takeout_my_activity_video_search_path
        with open(file_path, 'r', encoding='utf-8') as f:
            file_contents = f.read()
            soup = BeautifulSoup(file_contents, 'lxml')
            list_video_search_logs = TakeoutHtmlParser.find_log(soup)
            if list_video_search_logs != []:
                for video_search_logs in list_video_search_logs:
                    print("..........................................................................")
                    dic_my_activity_video_search = {'service':"", 'type':"", 'url':"", 'keyword':"", 'timestamp':""}
                    MyActivityVideoSearch.parse_video_search_log_title(dic_my_activity_video_search, video_search_logs)
                    MyActivityVideoSearch.parse_video_search_log_body(dic_my_activity_video_search, video_search_logs)
                    print(dic_my_activity_video_search)

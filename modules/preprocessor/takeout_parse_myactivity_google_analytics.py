import os
import logging
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from modules.utils.takeout_html_parser import TakeoutHtmlParser

logger = logging.getLogger('gtForensics')

class MyActivityGoogleAnalytics(object):
    def parse_analytics_log_body(dic_my_activity_analytics, analytics_logs):
        list_analytics_event_logs = TakeoutHtmlParser.find_log_body(analytics_logs)
        if list_analytics_event_logs != []:
            idx = 0
            for content in list_analytics_event_logs:
                # print("----------------------------------------------")
                content = str(content).strip()
                content = content.replace(u'\xa0', ' ')
                # print(content)
                if idx == 0:
                    if content == 'Used':
                        dic_my_activity_analytics['type'] = 'Use'
                    elif content == 'Visited':
                        dic_my_activity_analytics['type'] = 'Visit'
                    else:
                        dic_my_activity_analytics['type'] = content
                else:
                    if idx == 1:
                        if content.startswith('<a href="'):
                            idx = content.find('">')
                            dic_my_activity_analytics['url'] = content[9:idx]
                            dic_my_activity_analytics['keyword'] = content[idx+2:content.find('</a>')]
                    elif content.endswith('UTC'):
                        dic_my_activity_analytics['timestamp'] = TakeoutHtmlParser.convert_datetime_to_unixtime(content)
                idx += 1

#---------------------------------------------------------------------------------------------------------------
    def parse_google_analytics(case):
        file_path = case.takeout_my_activity_google_analytics_path
        with open(file_path, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')
            list_analytics_logs = TakeoutHtmlParser.find_log(soup)
            if list_analytics_logs != []:
                for analytics_logs in list_analytics_logs:
                    print("..........................................................................")
                    dic_my_activity_analytics = {'type':"", 'url':"", 'keyword':"", 'timestamp':""}
                    MyActivityGoogleAnalytics.parse_analytics_log_body(dic_my_activity_analytics, analytics_logs)
                    print(dic_my_activity_analytics)

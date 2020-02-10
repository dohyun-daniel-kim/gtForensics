import os
import logging
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from modules.utils.takeout_html_parser import TakeoutHtmlParser

logger = logging.getLogger('gtForensics')

class MyActivityGmail(object):
    def parse_gmail_log_body(dic_my_activity_gmail, gmail_logs):
        list_gmail_search_logs = TakeoutHtmlParser.find_log_body(gmail_logs)
        if list_gmail_search_logs != []:
            idx = 0
            for content in list_gmail_search_logs:
                # print("----------------------------------------------")
                content = str(content).strip()
                content = content.replace(u'\xa0', ' ')
                # print(content)
                if idx == 0:
                    if content == 'Searched for':
                        dic_my_activity_gmail['type'] = 'Search'
                    else:
                        dic_my_activity_gmail['type'] = content
                else:
                    if idx == 1:
                        if content.startswith('<a href="'):
                            idx = content.find('">')
                            dic_my_activity_gmail['url'] = content[9:idx]
                            dic_my_activity_gmail['keyword'] = content[idx+2:content.find('</a>')]
                    elif content.endswith('UTC'):
                        dic_my_activity_gmail['timestamp'] = TakeoutHtmlParser.convert_datetime_to_unixtime(content)
                idx += 1

#---------------------------------------------------------------------------------------------------------------
    def parse_gmail_log_title(dic_my_activity_gmail, gmail_logs):
        list_gmail_title_logs = TakeoutHtmlParser.find_log_title(gmail_logs)
        if list_gmail_title_logs != []:
            for content in list_gmail_title_logs:
                content = str(content).strip()
                dic_my_activity_gmail['service'] = content.split('>')[1].split('<br')[0]
                # print(dic_my_activity_gmail['service'])

#---------------------------------------------------------------------------------------------------------------
    def parse_gmail(case):
        file_path = case.takeout_my_activity_gmail_path
        with open(file_path, 'r', encoding='utf-8') as f:
            # soup = BeautifulSoup(f, 'html.parser')
            file_contents = f.read()
            soup = BeautifulSoup(file_contents, 'lxml')
            list_gmail_logs = TakeoutHtmlParser.find_log(soup)
            if list_gmail_logs != []:
                for gmail_logs in list_gmail_logs:
                    # print("..........................................................................")
                    dic_my_activity_gmail = {'service':"", 'type':"", 'url':"", 'keyword':"", 'timestamp':""}
                    MyActivityGmail.parse_gmail_log_title(dic_my_activity_gmail, gmail_logs)
                    MyActivityGmail.parse_gmail_log_body(dic_my_activity_gmail, gmail_logs)
                    print(dic_my_activity_gmail)

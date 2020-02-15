import os
import logging
from bs4 import BeautifulSoup
from urllib.parse import urlparse, unquote
from modules.utils.takeout_html_parser import TakeoutHtmlParser
from modules.utils.takeout_sqlite3 import SQLite3
from tqdm import trange

logger = logging.getLogger('gtForensics')

class MyActivityVideoSearch(object):
    def parse_video_search_log_body(dic_my_activity_video_search, video_search_logs):
        list_video_search_event_logs = TakeoutHtmlParser.find_log_body(video_search_logs)
        if list_video_search_event_logs != []:
            idx = 0
            for content in list_video_search_event_logs:
                content = str(content).strip()
                content = content.replace(u'\xa0', ' ')
                if idx == 0:
                    if content == 'Searched for':
                        dic_my_activity_video_search['type'] = 'Search'
                    elif content == 'Watched':
                        dic_my_activity_video_search['type'] = 'Watch'
                    else:
                        dic_my_activity_video_search['type'] = content
                else:
                    if idx == 1:
                        if content.startswith('<a href="'):
                            idx2 = content.find('">')
                            url = content[9:idx2]
                            url = unquote(url)
                            dic_my_activity_video_search['keyword_url'] = url
                            o = urlparse(url)
                            if o.netloc.startswith('m.'):
                                dic_my_activity_video_search['used_device'] = 'mobile'
                            if dic_my_activity_video_search['type'] != 'Search':
                                if o.query.startswith('q=') and o.query.find('&amp;'):
                                    real_url = o.query[2:o.query.find('&amp;')]                                    
                                    real_url = unquote(real_url)
                                    dic_my_activity_video_search['keyword_url'] = real_url
                                    o = urlparse(real_url)
                                    if o.netloc.startswith('m.'):
                                        dic_my_activity_video_search['used_device'] = 'mobile'
                            keyword = content[idx2+2:content.find('</a>')]
                            dic_my_activity_video_search['keyword'] = TakeoutHtmlParser.remove_special_char(keyword)
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
    def insert_log_info_to_analysis_db(dic_my_activity_video_search, analysis_db_path):
        query = 'INSERT INTO parse_my_activity_video_search \
                (timestamp, service, type, keyword, keyword_url, used_device) \
                VALUES(%d, "%s", "%s", "%s", "%s", "%s")' % \
                (int(dic_my_activity_video_search['timestamp']), dic_my_activity_video_search['service'], dic_my_activity_video_search['type'], \
                dic_my_activity_video_search['keyword'], dic_my_activity_video_search['keyword_url'], dic_my_activity_video_search['used_device'])
        SQLite3.execute_commit_query(query, analysis_db_path)

#---------------------------------------------------------------------------------------------------------------
    def parse_video_search(case):
        file_path = case.takeout_my_activity_video_search_path
        if os.path.exists(file_path) == False:
            return False
        with open(file_path, 'r', encoding='utf-8') as f:
            file_contents = f.read()
            soup = BeautifulSoup(file_contents, 'lxml')
            list_video_search_logs = TakeoutHtmlParser.find_log(soup)
            if list_video_search_logs != []:
                for i in trange(len(list_video_search_logs), desc="[Parsing the My Activity -> Video Search data.......]", unit="epoch"):
                    # print("..........................................................................")
                    dic_my_activity_video_search = {'service':"", 'type':"", 'keyword_url':"", 'keyword':"", 'timestamp':"", 'used_device':""}
                    MyActivityVideoSearch.parse_video_search_log_title(dic_my_activity_video_search, list_video_search_logs[i])
                    MyActivityVideoSearch.parse_video_search_log_body(dic_my_activity_video_search, list_video_search_logs[i])
                    MyActivityVideoSearch.insert_log_info_to_analysis_db(dic_my_activity_video_search, case.analysis_db_path)
                    # print(dic_my_activity_video_search)

import os
import logging
import json
from urllib.parse import urlparse, unquote
from modules.utils.takeout_html_parser import TakeoutHtmlParser
from modules.utils.takeout_sqlite3 import SQLite3
from tqdm import trange

logger = logging.getLogger('gtForensics')

class Chrome(object):
    def parse_history_logs(dic_browser_history, history_logs):
        for k, v in history_logs.items():
            if k == 'time_usec':
                dic_browser_history['timestamp'] = int(v)//1000000
            elif k == 'page_transition':
                dic_browser_history['page_transition'] = v
            elif k == 'url':
                dic_browser_history['url'] = TakeoutHtmlParser.remove_special_char(unquote(v))
                o = urlparse(v)
                if o.netloc.startswith('m.'):
                    dic_browser_history['used_device'] = 'mobile'
            elif k == 'title':
                dic_browser_history['title'] = v.replace("\"", "\'")
            elif k == 'client_id':
                dic_browser_history['client_id'] = v
            elif k == 'favicon_url':
                dic_browser_history['favicon_url'] = v

#---------------------------------------------------------------------------------------------------------------
    def insert_log_info_to_preprocess_db(dic_browser_history, preprocess_db_path):
        query = 'INSERT INTO parse_chrome \
                (timestamp, page_transition, url, title, client_id, favicon_url, used_device) \
                VALUES(%d, "%s", "%s", "%s", "%s", "%s", "%s")' % \
                (int(dic_browser_history['timestamp']), dic_browser_history['page_transition'], dic_browser_history['url'], \
                dic_browser_history['title'], dic_browser_history['client_id'], dic_browser_history['favicon_url'], dic_browser_history['used_device'])
        SQLite3.execute_commit_query(query, preprocess_db_path)

#---------------------------------------------------------------------------------------------------------------
    def parse_browser_history(case):
        file_path = case.takeout_chrome_path
        if os.path.exists(file_path) == False:
            return False
        
        data = json.load(open(file_path,'r', encoding='utf-8'))
        history_logs = data['Browser History']
        for i in trange(len(history_logs), desc="[Parsing the Chrome History Data....................]", unit="epoch"):
            dic_browser_history = {'timestamp':0, 'page_transition':"", 'url':"", 'title':"", 'client_id':"", 'favicon_url':"", 'used_device':""}
            Chrome.parse_history_logs(dic_browser_history, history_logs[i])
            Chrome.insert_log_info_to_preprocess_db(dic_browser_history, case.preprocess_db_path)

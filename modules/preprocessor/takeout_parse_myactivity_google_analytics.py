import os
import logging
from bs4 import BeautifulSoup
from urllib.parse import urlparse, unquote
from modules.utils.takeout_html_parser import TakeoutHtmlParser
from modules.utils.takeout_sqlite3 import SQLite3
from tqdm import trange

logger = logging.getLogger('gtForensics')

class MyActivityGoogleAnalytics(object):
    def parse_analytics_log_body(dic_my_activity_google_analytics, analytics_logs):
        list_analytics_event_logs = TakeoutHtmlParser.find_log_body(analytics_logs)
        if list_analytics_event_logs != []:
            idx = 0
            for content in list_analytics_event_logs:
                content = str(content).strip()
                content = content.replace(u'\xa0', ' ')
                if idx == 0:
                    if content == 'Used':
                        dic_my_activity_google_analytics['type'] = 'Use'
                    elif content == 'Visited':
                        dic_my_activity_google_analytics['type'] = 'Visit'
                    else:
                        dic_my_activity_google_analytics['type'] = content
                else:
                    if idx == 1:
                        if content.startswith('<a href="'):
                            idx2 = content.find('">')
                            keyword = content[idx2+2:content.find('</a>')]
                            dic_my_activity_google_analytics['keyword'] = TakeoutHtmlParser.remove_special_char(keyword)
                            url = content[9:idx2]
                            url = unquote(url)
                            dic_my_activity_google_analytics['keyword_url'] = url
                            o = urlparse(url)
                            if o.query.startswith('q=') and o.query.find('&amp;'):
                                real_url = o.query[2:o.query.find('&amp;')]
                                real_url = unquote(real_url)
                                dic_my_activity_google_analytics['keyword_url'] = real_url
                                o = urlparse(real_url)
                                if o.netloc.startswith('m.'):
                                    dic_my_activity_google_analytics['used_device'] = 'mobile'

                            if o.netloc.startswith('m.'):
                                dic_my_activity_google_analytics['used_device'] = 'mobile'
                    elif content.endswith('UTC'):
                        dic_my_activity_google_analytics['timestamp'] = TakeoutHtmlParser.convert_datetime_to_unixtime(content)
                idx += 1

#---------------------------------------------------------------------------------------------------------------
    def parse_ganalytics_log_title(dic_my_activity_google_analytics, analytics_logs):
        list_analytics_title_logs = TakeoutHtmlParser.find_log_title(analytics_logs)
        if list_analytics_title_logs != []:
            for content in list_analytics_title_logs:
                content = str(content).strip()
                dic_my_activity_google_analytics['service'] = content.split('>')[1].split('<br')[0]

#---------------------------------------------------------------------------------------------------------------
    def insert_log_info_to_preprocess_db(dic_my_activity_google_analytics, preprocess_db_path):
        query = 'INSERT INTO parse_my_activity_google_analytics \
                (timestamp, service, type, keyword, keyword_url, used_device) \
                VALUES(%d, "%s", "%s", "%s", "%s", "%s")' % \
                (int(dic_my_activity_google_analytics['timestamp']), dic_my_activity_google_analytics['service'], dic_my_activity_google_analytics['type'], \
                dic_my_activity_google_analytics['keyword'], dic_my_activity_google_analytics['keyword_url'], dic_my_activity_google_analytics['used_device'])
        SQLite3.execute_commit_query(query, preprocess_db_path)

#---------------------------------------------------------------------------------------------------------------
    # def do_parse(list_analytics_logs, preprocess_db_path, result):
    #     for analytics_logs in list_analytics_logs:
    #         # print("..........................................................................")
    #         # print(analytics_logs)
            # dic_my_activity_google_analytics = {'service':"", 'type':"", 'url':"", 'keyword':"", 'timestamp':""}
            # MyActivityGoogleAnalytics.parse_ganalytics_log_title(dic_my_activity_google_analytics, analytics_logs)
            # MyActivityGoogleAnalytics.parse_analytics_log_body(dic_my_activity_google_analytics, analytics_logs)
            # MyActivityGoogleAnalytics.insert_log_info_to_preprocess_db(dic_my_activity_google_analytics, preprocess_db_path)
            # print(dic_my_activity_google_analytics)

    #     result.put(len(list_analytics_logs))

#---------------------------------------------------------------------------------------------------------------
    def parse_google_analytics(case):
        file_path = case.takeout_my_activity_google_analytics_path
        if os.path.exists(file_path) == False:
            return False
        with open(file_path, 'r', encoding='utf-8') as f:
            file_contents = f.read()
            soup = BeautifulSoup(file_contents, 'lxml')
            list_analytics_logs = TakeoutHtmlParser.find_log(soup)
            if list_analytics_logs != []:
                for i in trange(len(list_analytics_logs), desc="[Parsing the My Activity -> Google Analytics data...]", unit="epoch"):
                    # print("..........................................................................")
                    dic_my_activity_google_analytics = {'service':"", 'type':"", 'keyword_url':"", 'keyword':"", 'timestamp':"", 'used_device':""}
                    MyActivityGoogleAnalytics.parse_ganalytics_log_title(dic_my_activity_google_analytics, list_analytics_logs[i])
                    MyActivityGoogleAnalytics.parse_analytics_log_body(dic_my_activity_google_analytics, list_analytics_logs[i])
                    MyActivityGoogleAnalytics.insert_log_info_to_preprocess_db(dic_my_activity_google_analytics, case.preprocess_db_path)    


                # for analytics_logs in list_analytics_logs:
                #     # print("..........................................................................")
                #     dic_my_activity_google_analytics = {'service':"", 'type':"", 'url':"", 'keyword':"", 'timestamp':""}
                #     MyActivityGoogleAnalytics.parse_ganalytics_log_title(dic_my_activity_google_analytics, analytics_logs)
                #     MyActivityGoogleAnalytics.parse_analytics_log_body(dic_my_activity_google_analytics, analytics_logs)
                #     MyActivityGoogleAnalytics.insert_log_info_to_preprocess_db(dic_my_activity_google_analytics, case.preprocess_db_path)
                    # print(dic_my_activity_google_analytics)



            # if list_analytics_logs == []:
            #     return False
            
            # length = len(list_analytics_logs)
            # NUMBER_OF_PROCESSES = case.number_of_input_processes
            # MAX_NUMBER_OF_PROCESSES_THIS_MODULE = math.ceil(length/2)

            # if NUMBER_OF_PROCESSES*2 > length:
            #     NUMBER_OF_PROCESSES = MAX_NUMBER_OF_PROCESSES_THIS_MODULE

            # if length < NUMBER_OF_PROCESSES:
            #     result = Queue()
            #     MyActivityGoogleAnalytics.do_parse(list_analytics_logs, case.preprocess_db_path, result)
            # else:
            #     num_item_per_list = math.ceil(length/NUMBER_OF_PROCESSES)
            #     start_pos = 0
            #     divied_list = list()
            #     for idx in range(start_pos, length, num_item_per_list):
            #         out = list_analytics_logs[start_pos:start_pos+num_item_per_list]
            #         if out != []:
            #             divied_list.append(out)
            #         start_pos += num_item_per_list

            #     result = Queue()
            #     procs = []

            #     for i in range(len(divied_list)):
            #         proc = Process(target=MyActivityGoogleAnalytics.do_parse, args=(divied_list[i], case.preprocess_db_path, result))
            #         procs.append(proc)
            #         proc.start()

            #     for proc in procs:
            #         proc.join()

            #     result.put('STOP')
            #     while True:
            #         tmp = result.get()
            #         if tmp == 'STOP':
            #             break




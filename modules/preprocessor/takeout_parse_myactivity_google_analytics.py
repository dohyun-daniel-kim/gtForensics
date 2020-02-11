import os
import logging
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from modules.utils.takeout_html_parser import TakeoutHtmlParser
from modules.utils.takeout_sqlite3 import SQLite3
from multiprocessing import Process, Queue
import math

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
                            # dic_my_activity_analytics['keyword'] = content[idx+2:content.find('</a>')]
                            dic_my_activity_analytics['keyword'] = content[idx+2:content.find('</a>')].replace("\"", "\'")
                    elif content.endswith('UTC'):
                        dic_my_activity_analytics['timestamp'] = TakeoutHtmlParser.convert_datetime_to_unixtime(content)
                idx += 1

#---------------------------------------------------------------------------------------------------------------
    def parse_ganalytics_log_title(dic_my_activity_analytics, analytics_logs):
        dic_my_activity_analytics['service'] = 'Google Analytics'
        # list_analytics_title_logs = TakeoutHtmlParser.find_log_title(analytics_logs)
        # if list_analytics_title_logs != []:
        #     for content in list_analytics_title_logs:
        #         content = str(content).strip()
        #         dic_my_activity_analytics['service'] = content.split('>')[1].split('<br')[0]

#---------------------------------------------------------------------------------------------------------------
    def insert_log_info_to_analysis_db(dic_my_activity_analytics, analysis_db_path):
        query = 'INSERT INTO parse_my_activity_analytics \
                (service, timestamp, type, keyword, url) \
                VALUES("%s", %d, "%s", "%s", "%s")' % \
                (dic_my_activity_analytics['service'], int(dic_my_activity_analytics['timestamp']), dic_my_activity_analytics['type'], \
                dic_my_activity_analytics['keyword'], dic_my_activity_analytics['url'])
        SQLite3.execute_commit_query(query, analysis_db_path)

#---------------------------------------------------------------------------------------------------------------
    def do_parse(list_analytics_logs, analysis_db_path, result):
        for analytics_logs in list_analytics_logs:
            print("..........................................................................")
            print(analytics_logs)
            dic_my_activity_analytics = {'service':"", 'type':"", 'url':"", 'keyword':"", 'timestamp':""}
            MyActivityGoogleAnalytics.parse_ganalytics_log_title(dic_my_activity_analytics, analytics_logs)
            MyActivityGoogleAnalytics.parse_analytics_log_body(dic_my_activity_analytics, analytics_logs)
            MyActivityGoogleAnalytics.insert_log_info_to_analysis_db(dic_my_activity_analytics, analysis_db_path)
            print(dic_my_activity_analytics)

        result.put(len(list_analytics_logs))

#---------------------------------------------------------------------------------------------------------------
    def parse_google_analytics(case):
        file_path = case.takeout_my_activity_google_analytics_path
        with open(file_path, 'r', encoding='utf-8') as f:
            # soup = BeautifulSoup(f, 'html.parser')
            file_contents = f.read()
            soup = BeautifulSoup(file_contents, 'lxml')
            list_analytics_logs = TakeoutHtmlParser.find_log(soup)
            if list_analytics_logs != []:
                length = len(list_analytics_logs)
                NUMBER_OF_PROCESSES = case.number_of_input_processes

                MAX_NUMBER_OF_PROCESSES_THIS_MODULE = math.ceil(length/2)
                if NUMBER_OF_PROCESSES*2 > length:
                    NUMBER_OF_PROCESSES = MAX_NUMBER_OF_PROCESSES_THIS_MODULE

                result = Queue()
                MyActivityGoogleAnalytics.do_parse(list_analytics_logs, case.analysis_db_path, result)

                # if length < NUMBER_OF_PROCESSES:
                #     # print(length)
                #     result = Queue()
                #     MyActivityGoogleAnalytics.do_parse(list_analytics_logs, case.analysis_db_path, result)
                # else:
                #     num_item_per_list = math.ceil(length/NUMBER_OF_PROCESSES)
                #     print('num_item_per_list: ', num_item_per_list)

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
                #         print(divied_list[0])
                #         proc = Process(target=MyActivityGoogleAnalytics.do_parse, args=(divied_list[i], case.analysis_db_path, result))
                #         procs.append(proc)
                #         proc.start()

                #     for proc in procs:
                #         proc.join()

                #     result.put('STOP')
                #     while True:
                #         tmp = result.get()
                #         if tmp == 'STOP':
                #             break




                # for analytics_logs in list_analytics_logs:
                #     # print("..........................................................................")
                #     dic_my_activity_analytics = {'service':"", 'type':"", 'url':"", 'keyword':"", 'timestamp':""}
                #     MyActivityGoogleAnalytics.parse_ganalytics_log_title(dic_my_activity_analytics, analytics_logs)
                #     MyActivityGoogleAnalytics.parse_analytics_log_body(dic_my_activity_analytics, analytics_logs)
                #     # MyActivityGoogleAnalytics.insert_log_info_to_analysis_db(dic_my_activity_analytics, case.analysis_db_path)
                #     # print(dic_my_activity_analytics)

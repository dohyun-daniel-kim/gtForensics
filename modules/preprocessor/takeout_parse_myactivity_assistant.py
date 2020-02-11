import os
import logging
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from modules.utils.takeout_html_parser import TakeoutHtmlParser
from modules.utils.takeout_sqlite3 import SQLite3
from tqdm import trange
# from tqdm import tqdm

logger = logging.getLogger('gtForensics')

class MyActivityAssistant(object):
    def parse_assistant_log_caption(dic_my_activity_assistant, assistant_logs):
        list_assistant_geodata_logs = TakeoutHtmlParser.find_log_caption(assistant_logs)
        if list_assistant_geodata_logs != []:
            for content in list_assistant_geodata_logs:
                content = str(content).strip()

                # if dic_my_activity_assistant['keyword'] == 'my next flight':
                if content == '<br/>':  continue
                if content.startswith('<a href="https://www.google.com/maps/'):
                    idx = content.find('">')
                    url = content[9:idx]
                    o = urlparse(url)
                    list_query_value = o.query.split(';')
                    if list_query_value != []:
                        for query_value in list_query_value:
                            if query_value.startswith('center='):
                                geodata = query_value.lstrip('center=').rstrip('&amp')
                                dic_my_activity_assistant['geodata_latitude'] = geodata.split(',')[0]
                                dic_my_activity_assistant['geodata_longitude'] = geodata.split(',')[1]
                            elif query_value.startswith('query='):
                                geodata = query_value.lstrip('query=')
                                dic_my_activity_assistant['geodata_latitude'] = geodata.split(',')[0]
                                dic_my_activity_assistant['geodata_longitude'] = geodata.split(',')[1]
                    if dic_my_activity_assistant['geodata_description'] == "":
                        dic_my_activity_assistant['geodata_description'] = content[idx+2:content.find('</a>')]
                        # print(dic_my_activity_assistant['geodata_description'])

#---------------------------------------------------------------------------------------------------------------
    def parse_assistant_log_body_text(dic_my_activity_assistant, assistant_logs):
        # print('voice logs')
        list_assistant_trained_logs = TakeoutHtmlParser.find_log_body_text(assistant_logs)
        if list_assistant_trained_logs != []:
            for content in list_assistant_trained_logs:
                content = str(content).strip()
                if content.startswith('<audio controls'):
                    # print(content)
                    dic_my_activity_assistant['attachment_voice_file'] = content.split('>')[2].split('<')[0].lstrip('Audio file: ')
                    # print(dic_my_activity_assistant['attachment_voice_file'])

#---------------------------------------------------------------------------------------------------------------
    def parse_assistant_log_body(dic_my_activity_assistant, assistant_logs):
        list_assistant_search_logs = TakeoutHtmlParser.find_log_body(assistant_logs)
        if list_assistant_search_logs != []:
            idx = 0
            for content in list_assistant_search_logs:
                # print("----------------------------------------------")
                content = str(content).strip()
                content = content.replace(u'\xa0', ' ')
                # print(content)
                if idx == 0:
                    dic_my_activity_assistant['type'] = content
                else:
                    if idx == 1 and dic_my_activity_assistant['type'] == 'Said':
                        dic_my_activity_assistant['type'] = 'Search'
                        if content.startswith('<a href="'):
                            idx = content.find('">')
                            dic_my_activity_assistant['url'] = content[9:idx]
                            dic_my_activity_assistant['keyword'] = content[idx+2:content.find('</a>')]
                    elif idx == 1 and (dic_my_activity_assistant['type'].startswith('Selected') or dic_my_activity_assistant['type'].startswith('Listened') or dic_my_activity_assistant['type'].startswith('Used') or dic_my_activity_assistant['type'].startswith('Trained')):
                        dic_my_activity_assistant['keyword'] = dic_my_activity_assistant['type']
                        dic_my_activity_assistant['type'] = 'Use'

                    elif content.endswith('UTC'):
                        dic_my_activity_assistant['timestamp'] = TakeoutHtmlParser.convert_datetime_to_unixtime(content)
                    elif idx != 1 and content != '<br/>':
                        dic_my_activity_assistant['answer'] += content
                idx += 1

#---------------------------------------------------------------------------------------------------------------
    def parse_assistant_log_title(dic_my_activity_assistant, assistant_logs):
        list_assistant_title_logs = TakeoutHtmlParser.find_log_title(assistant_logs)
        if list_assistant_title_logs != []:
            for content in list_assistant_title_logs:
                content = str(content).strip()
                dic_my_activity_assistant['service'] = content.split('>')[1].split('<br')[0]
                # print(dic_my_activity_assistant['service'])

#---------------------------------------------------------------------------------------------------------------
    def insert_log_info_to_analysis_db(dic_my_activity_assistant, analysis_db_path):
        query = 'INSERT INTO parse_my_activity_assistant \
            (service, timestamp, type, keyword, url, geodata_latitude, geodata_longitude, geodata_description, attachment_voice_file) \
            VALUES("%s", %d, "%s", "%s", "%s", "%s", "%s", "%s", "%s")' % \
            (dic_my_activity_assistant['service'], int(dic_my_activity_assistant['timestamp']), dic_my_activity_assistant['type'], \
            dic_my_activity_assistant['keyword'], dic_my_activity_assistant['url'], dic_my_activity_assistant['geodata_latitude'], \
            dic_my_activity_assistant['geodata_longitude'], dic_my_activity_assistant['geodata_description'], dic_my_activity_assistant['attachment_voice_file'])
        SQLite3.execute_commit_query(query, analysis_db_path)

#---------------------------------------------------------------------------------------------------------------
    def parse_assistant(case):
        file_path = case.takeout_my_activity_assistant_path
        # print("my activity assistant")
        # print("file_path: ", file_path)

        with open(file_path, 'r', encoding='utf-8') as f:
            file_contents = f.read()
            soup = BeautifulSoup(file_contents, 'lxml')
            # soup = BeautifulSoup(f, 'html.parser')
            list_assistant_logs = TakeoutHtmlParser.find_log(soup)
            if list_assistant_logs != []:
                # for i in tqdm(range(len(list_assistant_logs))):
                for i in trange(len(list_assistant_logs), desc="[Parsing the My Activity -> Assistant data..........]", unit="epoch"):
                    # print("..........................................................................")
                    dic_my_activity_assistant = {'service':"", 'type':"", 'url':"", 'keyword':"", 'answer':"", 'timestamp':"", 'geodata_latitude':"", 'geodata_longitude':"", 'geodata_description':"", 'attachment_voice_file':""}
                    MyActivityAssistant.parse_assistant_log_title(dic_my_activity_assistant, list_assistant_logs[i])
                    MyActivityAssistant.parse_assistant_log_body(dic_my_activity_assistant, list_assistant_logs[i])
                    MyActivityAssistant.parse_assistant_log_body_text(dic_my_activity_assistant, list_assistant_logs[i])
                    MyActivityAssistant.parse_assistant_log_caption(dic_my_activity_assistant, list_assistant_logs[i])
                    MyActivityAssistant.insert_log_info_to_analysis_db(dic_my_activity_assistant, case.analysis_db_path)


                # for assistant_logs in list_assistant_logs:
                #     # print("..........................................................................")
                #     dic_my_activity_assistant = {'service':"", 'type':"", 'url':"", 'keyword':"", 'answer':"", 'timestamp':"", 'geodata_latitude':"", 'geodata_longitude':"", 'geodata_description':"", 'attachment_voice_file':""}
                #     MyActivityAssistant.parse_assistant_log_title(dic_my_activity_assistant, assistant_logs)
                #     MyActivityAssistant.parse_assistant_log_body(dic_my_activity_assistant, assistant_logs)
                #     MyActivityAssistant.parse_assistant_log_body_text(dic_my_activity_assistant, assistant_logs)
                #     MyActivityAssistant.parse_assistant_log_caption(dic_my_activity_assistant, assistant_logs)
                #     MyActivityAssistant.insert_log_info_to_analysis_db(dic_my_activity_assistant, case.analysis_db_path)

                    # print(case.analysis_db_path)
                    # if dic_my_activity_assistant['attachment_voice_file'] == "":
                    #     MyActivityAssistant.insert_log_info_to_analysis_db(dic_my_activity_assistant, case.analysis_db_path)
                        # print(dic_my_activity_assistant)




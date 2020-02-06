import os
import logging
from bs4 import BeautifulSoup
import time
from urllib.parse import urlparse

logger = logging.getLogger('gtForensics')

class MyActivityAssistant(object):
    def parse_assistant_said(case):
        file_path = case.takeout_my_activity_assistant_path
        print("my activity assistant")
        print("file_path: ", file_path)

        with open(file_path, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')
            list_assistant_logs = soup.find_all('div', class_ ={"outer-cell mdl-cell mdl-cell--12-col mdl-shadow--2dp"})
            if list_assistant_logs != []:
                for assistant_logs in list_assistant_logs:
                    print("..........................................................................")
                    dic_my_activity_assistant = {'type':"", 'url':"", 'keyword':"", 'answer':"", 'timestamp':"", 'geodata_latitude':"", 'geodata_longitude':"", 'geodata_description':"", 'attachment_voice_file':""}
                    list_assistant_search_logs = assistant_logs.find('div', class_ ={"content-cell mdl-cell mdl-cell--6-col mdl-typography--body-1"})
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
                                    if content.startswith('<a href="'):
                                        idx = content.find('">')
                                        dic_my_activity_assistant['url'] = content[9:idx]
                                        dic_my_activity_assistant['keyword'] = content[idx+2:content.find('</a>')]
                                elif content.endswith('UTC'):
                                    dic_my_activity_assistant['timestamp'] = content
                                elif idx != 1 and content != '<br/>':
                                    dic_my_activity_assistant['answer'] += content
                            idx += 1

                    list_assistant_trained_logs = assistant_logs.find('div', class_ ={"content-cell mdl-cell mdl-cell--6-col mdl-typography--body-1 mdl-typography--text-right"})
                    if list_assistant_trained_logs != []:
                        for content in list_assistant_trained_logs:
                            content = str(content).strip()
                            if content.startswith('<audio controls'):
                                dic_my_activity_assistant['attachment_voice_file'] = content.split('/>')[1].rstrip('</audio>')

                    list_assistant_geodata_logs = assistant_logs.find('div', class_ ={"content-cell mdl-cell mdl-cell--12-col mdl-typography--caption"})
                    if list_assistant_geodata_logs != []:
                        for content in list_assistant_geodata_logs:
                            content = str(content).strip()
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
                                dic_my_activity_assistant['geodata_description'] = content[idx+2:content.find('</a>')]
                        print(dic_my_activity_assistant)




import os
import logging
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from modules.utils.takeout_html_parser import TakeoutHtmlParser
from modules.utils.takeout_sqlite3 import SQLite3
from tqdm import trange

logger = logging.getLogger('gtForensics')

class MyActivityMaps(object):
    def parse_maps_log_caption(dic_my_activity_maps, maps_logs):
        list_maps_logs = TakeoutHtmlParser.find_log_caption(maps_logs)
        if list_maps_logs != []:
            for content in list_maps_logs:
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
                                dic_my_activity_maps['geodata_latitude'] = geodata.split(',')[0]
                                dic_my_activity_maps['geodata_longitude'] = geodata.split(',')[1]
                            elif query_value.startswith('query='):
                                geodata = query_value.lstrip('query=')
                                dic_my_activity_maps['geodata_latitude'] = geodata.split(',')[0]
                                dic_my_activity_maps['geodata_longitude'] = geodata.split(',')[1]
                    dic_my_activity_maps['geodata_description'] = content[idx+2:content.find('</a>')]

#---------------------------------------------------------------------------------------------------------------
    def parse_maps_log_body(dic_my_activity_maps, maps_logs):
        list_maps_event_logs = TakeoutHtmlParser.find_log_body(maps_logs)
        if list_maps_event_logs != []:
            idx = 0
            for content in list_maps_event_logs:
                content = str(content).strip()
                content = content.replace(u'\xa0', ' ')
                # print(content)
                if idx == 0:
                    if content.startswith('<a href="'):
                        url = content[9:content.find('">')]
                        keyword = content.split('>')[1].split('</a')[0]
                        dic_my_activity_maps['keyword'] = keyword.replace("\"", "\'")

                        if keyword.startswith('View'):
                            dic_my_activity_maps['type'] = 'View'
                        else:
                            dic_my_activity_maps['type'] = 'Search'

                        dic_my_activity_maps['url'] = url
                        o = urlparse(url)
                        if o.path.startswith('/maps/@'):
                            list_value = o.path.lstrip('/maps/@').split(',')
                            if list_value != []:
                                # print(list_value)
                                latitude = list_value[0]
                                longitude = list_value[1]
                                dic_my_activity_maps['geodata_search_latitude'] = latitude
                                dic_my_activity_maps['geodata_search_longitude'] = longitude
                        elif o.path.find('@') >= 1:
                            list_value = o.path.split('@')[1].split(',')
                            if list_value != []:
                                latitude = list_value[0]
                                longitude = list_value[1]
                                dic_my_activity_maps['geodata_search_latitude'] = latitude
                                dic_my_activity_maps['geodata_search_longitude'] = longitude
                    else:
                        if content == 'Searched for':
                            dic_my_activity_maps['type'] = 'Search'
                        elif content.startswith('Shared'):
                            dic_my_activity_maps['type'] = 'Share'
                        elif content.startswith('Viewed'):
                            dic_my_activity_maps['type'] = 'View'
                            if content == 'Viewed For you':
                                dic_my_activity_maps['keyword'] = content
                        elif content == 'Used Maps':
                            dic_my_activity_maps['type'] = 'Use'
                            dic_my_activity_maps['keyword'] = content
                        elif content.startswith('Answered'):
                            dic_my_activity_maps['type'] = 'Answer'
                            dic_my_activity_maps['keyword'] = content
                        else:
                            dic_my_activity_maps['type'] = content
                else:
                    if idx == 1:
                        if content.startswith('<a href="'):
                            idx = content.find('">')
                            dic_my_activity_maps['keyword'] = content[idx+2:content.find('</a>')].replace("\"", "\'")
                            url = content[9:idx]
                            dic_my_activity_maps['url'] = url
                            o = urlparse(url)
                            if o.path.startswith('/maps/') and o.path.find('@') >= 1:
                                list_value = o.path.split('@')[1].split(',')
                                if list_value != []:
                                    latitude = list_value[0]
                                    longitude = list_value[1]
                                    dic_my_activity_maps['geodata_search_latitude'] = latitude
                                    dic_my_activity_maps['geodata_search_longitude'] = longitude
                    else:
                        if content.endswith('UTC'):
                            dic_my_activity_maps['timestamp'] = TakeoutHtmlParser.convert_datetime_to_unixtime(content)
                        elif idx == 4 and dic_my_activity_maps['type'] == '1 notification':
                            dic_my_activity_maps['keyword'] = content
                idx += 1

#---------------------------------------------------------------------------------------------------------------
    def parse_maps_log_title(dic_my_activity_maps, maps_logs):
        list_maps_title_logs = TakeoutHtmlParser.find_log_title(maps_logs)
        if list_maps_title_logs != []:
            for content in list_maps_title_logs:
                content = str(content).strip()
                dic_my_activity_maps['service'] = content.split('>')[1].split('<br')[0]

#---------------------------------------------------------------------------------------------------------------
    def insert_log_info_to_analysis_db(dic_my_activity_maps, analysis_db_path):
        query = 'INSERT INTO parse_my_activity_map \
                (service, timestamp, type, keyword, url, search_location, geodata_search_latitude, \
                geodata_search_longitude, geodata_latitude, geodata_longitude, geodata_description) \
                VALUES("%s", %d, "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s")' % \
                (dic_my_activity_maps['service'], int(dic_my_activity_maps['timestamp']), dic_my_activity_maps['type'], \
                dic_my_activity_maps['keyword'], dic_my_activity_maps['url'], dic_my_activity_maps['search_location'], \
                dic_my_activity_maps['geodata_search_latitude'], dic_my_activity_maps['geodata_search_longitude'], \
                dic_my_activity_maps['geodata_latitude'], dic_my_activity_maps['geodata_longitude'], dic_my_activity_maps['geodata_description'])
        SQLite3.execute_commit_query(query, analysis_db_path)

#---------------------------------------------------------------------------------------------------------------
    def parse_maps(case):
        # print('video search')
        file_path = case.takeout_my_activity_maps_path
        with open(file_path, 'r', encoding='utf-8') as f:
            file_contents = f.read()
            soup = BeautifulSoup(file_contents, 'lxml')
            list_maps_logs = TakeoutHtmlParser.find_log(soup)
            if list_maps_logs != []:
                for i in trange(len(list_maps_logs), desc="[Parsing the My Activity -> Maps data...............]", unit="epoch"):
                # for maps_logs in list_maps_logs:
                    # print("..........................................................................")
                    dic_my_activity_maps = {'service':"", 'type':"", 'url':"", 'keyword':"", 'timestamp':"", \
                        'search_location':"", 'geodata_search_latitude':"", 'geodata_search_longitude':"",\
                        'geodata_latitude':"", 'geodata_longitude':"", 'geodata_description':""}
                    MyActivityMaps.parse_maps_log_title(dic_my_activity_maps, list_maps_logs[i])
                    MyActivityMaps.parse_maps_log_body(dic_my_activity_maps, list_maps_logs[i])
                    MyActivityMaps.parse_maps_log_caption(dic_my_activity_maps, list_maps_logs[i])
                    MyActivityMaps.insert_log_info_to_analysis_db(dic_my_activity_maps, case.analysis_db_path)
                    # print(dic_my_activity_maps)
                    # if dic_my_activity_maps['type'] == 'View':
                    #     print("..........................................................................")
                    #     print(dic_my_activity_maps)

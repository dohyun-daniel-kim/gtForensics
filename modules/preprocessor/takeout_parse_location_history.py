import os
import logging
import json

# from bs4 import BeautifulSoup
# from urllib.parse import urlparse, unquote
# from modules.utils.takeout_html_parser import TakeoutHtmlParser
from modules.utils.takeout_sqlite3 import SQLite3
from tqdm import trange

logger = logging.getLogger('gtForensics')

class LocationHistory(object):
    def parse_logs(dic_location, location_logs):
        for log in location_logs:
            print(log['timestampMs'])
            # timestamp = int(log['timestampMs'])//1000
            # timestamp = log['timestampMs']
            # print(timestamp)


        # for participants in conversation_logs['conversation']['conversation']['participant_data']:
        #     try:
        #         print("===========================================================")
        #         print("participants user_name: ", participants['fallback_name'])
        #         print("participants gaia_id: ", participants['id']['gaia_id'])
        #     except KeyError:
        #         pass
        # for messages in conversation_logs['events']:
        #     try:
        #         # print("------------------")
        #         dic_hangouts['timestamp'] = int(messages['timestamp'])//1000000
        #         dic_hangouts['sender_id'] = messages['sender_id']['gaia_id']
        #         dic_hangouts['message'] = messages['chat_message']['message_content']['segment'][0]['text']
        #     except KeyError:
        #         pass
        #     try:                
        #         attachment_type = messages['chat_message']['message_content']['attachment'][0]['embed_item']['type'][0]
        #         if attachment_type == 'PLUS_PHOTO':
        #             attachment_type = messages['chat_message']['message_content']['attachment'][0]['embed_item']['plus_photo']['media_type']
        #             dic_hangouts['attachment_type'] = attachment_type
        #             # print(attachment_type)
        #             # dic_hangouts['attachment']
        #             # print("attachment_photo_id: ", messages['chat_message']['message_content']['attachment'][0]['embed_item']['plus_photo']['photo_id'])
        #             # print("attachment_photo_url: ", messages['chat_message']['message_content']['attachment'][0]['embed_item']['plus_photo']['url'])
        #         elif attachment_type == 'PLACE_V2':
        #             latitude = messages['chat_message']['message_content']['attachment'][0]['embed_item']['place_v2']['geo']['geo_coordinates_v2']['latitude']
        #             dic_hangouts['latitude'] = latitude
        #             longitude = messages['chat_message']['message_content']['attachment'][0]['embed_item']['place_v2']['geo']['geo_coordinates_v2']['longitude']
        #             dic_hangouts['longitude'] = longitude
        #             # print("attachment_place: ", messages['chat_message']['message_content']['attachment'][0]['embed_item']['type'][0])
        #         else:
        #             print(attachment_type)
        #     except KeyError:
        #         pass
        #     print(dic_hangouts)

#---------------------------------------------------------------------------------------------------------------
    def insert_log_info_to_preprocess_db(dic_my_activity_android, preprocess_db_path):
        query = 'INSERT INTO parse_my_activity_android \
                (timestamp, service, type, keyword, keyword_url, package_name, used_device) \
                VALUES(%d, "%s", "%s", "%s", "%s", "%s", "%s")' % \
                (int(dic_my_activity_android['timestamp']), dic_my_activity_android['service'], dic_my_activity_android['type'], \
                dic_my_activity_android['keyword'], dic_my_activity_android['keyword_url'], dic_my_activity_android['package_name'], \
                dic_my_activity_android['used_device'])
        SQLite3.execute_commit_query(query, preprocess_db_path)

#---------------------------------------------------------------------------------------------------------------
    def parse_location_history(case):
        file_path = case.takeout_location_history_path
        if os.path.exists(file_path) == False:
            return False

        data = json.load(open(file_path,'r', encoding='utf-8'))
        location_logs = data['locations']

        for i in trange(len(location_logs)):
            dic_location = {'timestamp':"", 'sender_name':"", 'sender_id':"", 'message':"", 'url':"", 'latitude':"", 'longitude':"", 'attachment_type':""}
            LocationHistory.parse_logs(dic_location, location_logs[i])


        # print(location_logs)

        # print(conversation_logs)
        # for conversation_logs in data['conversations']:
        #     # print(conversation)
        
        
        
        # for i in trange(len(conversation_logs)):
        #     dic_hangouts = {'timestamp':"", 'sender_name':"", 'sender_id':"", 'message':"", 'url':"", 'latitude':"", 'longitude':"", 'attachment_type':""}
        #     Hangouts.parse_chatroom_logs(dic_hangouts, conversation_logs[i])
            
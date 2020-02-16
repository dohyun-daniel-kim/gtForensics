import os
import logging
import json

# from bs4 import BeautifulSoup
# from urllib.parse import urlparse, unquote
# from modules.utils.takeout_html_parser import TakeoutHtmlParser
from modules.utils.takeout_sqlite3 import SQLite3
from tqdm import trange

logger = logging.getLogger('gtForensics')

class Hangouts(object):
    def parse_chatroom_logs(dic_hangouts, conversation_logs):
        for participants in conversation_logs['conversation']['conversation']['participant_data']:
            try:
                print("===========================================================")
                print("participants user_name: ", participants['fallback_name'])
                print("participants gaia_id: ", participants['id']['gaia_id'])
            except KeyError:
                pass
        for messages in conversation_logs['events']:
            try:
                # print("------------------")
                dic_hangouts['timestamp'] = int(messages['timestamp'])//1000000
                dic_hangouts['sender_id'] = messages['sender_id']['gaia_id']
                dic_hangouts['message'] = messages['chat_message']['message_content']['segment'][0]['text']
            except KeyError:
                pass
            try:                
                attachment_type = messages['chat_message']['message_content']['attachment'][0]['embed_item']['type'][0]
                if attachment_type == 'PLUS_PHOTO':
                    attachment_type = messages['chat_message']['message_content']['attachment'][0]['embed_item']['plus_photo']['media_type']
                    dic_hangouts['attachment_type'] = attachment_type
                    # print(attachment_type)
                    # dic_hangouts['attachment']
                    # print("attachment_photo_id: ", messages['chat_message']['message_content']['attachment'][0]['embed_item']['plus_photo']['photo_id'])
                    # print("attachment_photo_url: ", messages['chat_message']['message_content']['attachment'][0]['embed_item']['plus_photo']['url'])
                elif attachment_type == 'PLACE_V2':
                    latitude = messages['chat_message']['message_content']['attachment'][0]['embed_item']['place_v2']['geo']['geo_coordinates_v2']['latitude']
                    dic_hangouts['latitude'] = latitude
                    longitude = messages['chat_message']['message_content']['attachment'][0]['embed_item']['place_v2']['geo']['geo_coordinates_v2']['longitude']
                    dic_hangouts['longitude'] = longitude
                    # print("attachment_place: ", messages['chat_message']['message_content']['attachment'][0]['embed_item']['type'][0])
                else:
                    print(attachment_type)
            except KeyError:
                pass
            print(dic_hangouts)

#---------------------------------------------------------------------------------------------------------------
    def insert_log_info_to_analysis_db(dic_my_activity_android, analysis_db_path):
        query = 'INSERT INTO parse_my_activity_android \
                (timestamp, service, type, keyword, keyword_url, package_name, used_device) \
                VALUES(%d, "%s", "%s", "%s", "%s", "%s", "%s")' % \
                (int(dic_my_activity_android['timestamp']), dic_my_activity_android['service'], dic_my_activity_android['type'], \
                dic_my_activity_android['keyword'], dic_my_activity_android['keyword_url'], dic_my_activity_android['package_name'], \
                dic_my_activity_android['used_device'])
        SQLite3.execute_commit_query(query, analysis_db_path)

#---------------------------------------------------------------------------------------------------------------
    def parse_hangouts(case):
        file_path = case.takeout_hangouts_path
        if os.path.exists(file_path) == False:
            return False

        data = json.load(open(file_path,'r', encoding='utf-8'))
        conversation_logs = data['conversations']
        # print(conversation_logs)
        # for conversation_logs in data['conversations']:
        #     # print(conversation)
        for i in trange(len(conversation_logs)):
            # print(conversation_logs[i])
        #         print(conversation_logs[i])
            dic_hangouts = {'timestamp':"", 'sender_name':"", 'sender_id':"", 'message':"", 'url':"", 'latitude':"", 'longitude':"", 'attachment_type':""}
            Hangouts.parse_chatroom_logs(dic_hangouts, conversation_logs[i])
            # print(type(conversation))
        # print(dic_hangouts)

            # for participants in conversation['conversation']['conversation']['participant_data']:
            #     try:
            #         print("===========================================================")
            #         print("participants user_name: ", participants['fallback_name'])
            #         print("participants chat_id: ", participants['id']['chat_id'])
            #     except KeyError:
            #         pass
            # for messages in conversation['events']:
            #     try:
            #         print("------------------")
            #         print("timestamp: ", int(messages['timestamp'])//1000000)
            #         print("sender_id(chat_id): ", messages['sender_id']['chat_id'])
            #         print("chat_message: ", messages['chat_message']['message_content']['segment'][0]['text'])
            #     except KeyError:
            #         pass
            #     try:
            #         attachment_type = messages['chat_message']['message_content']['attachment'][0]['embed_item']['type'][0]
            #         if attachment_type == 'PLUS_PHOTO':
            #             print("attachment_photo_id: ", messages['chat_message']['message_content']['attachment'][0]['embed_item']['plus_photo']['photo_id'])
            #             print("attachment_photo_url: ", messages['chat_message']['message_content']['attachment'][0]['embed_item']['plus_photo']['url'])
            #         elif attachment_type == 'PLACE_V2':
            #             print("attachment_place: ", messages['chat_message']['message_content']['attachment'][0]['embed_item']['type'][0])
            #     except KeyError:
            #         pass
                
                


        # with open(file_path, 'r', encoding='utf-8') as f:
        #     file_contents = f.read()
        #     soup = BeautifulSoup(file_contents, 'lxml')
        #     list_android_logs = TakeoutHtmlParser.find_log(soup)
        #     if list_android_logs != []:
        #         for i in trange(len(list_android_logs), desc="[Parsing the My Activity -> Android data............]", unit="epoch"):
        #             # print("..........................................................................")
        #             dic_my_activity_android = {'service':"", 'type':"", 'keyword_url':"", 'keyword':"", 'timestamp':"", 'package_name':"", 'used_device':""}
        #             # MyActivityAndroid.parse_android_log_title(dic_my_activity_android, list_android_logs[i])
        #             # MyActivityAndroid.parse_android_log_body(dic_my_activity_android, list_android_logs[i])
        #             # MyActivityAndroid.parse_android_log_caption(dic_my_activity_android, list_android_logs[i])
        #             # MyActivityAndroid.insert_log_info_to_analysis_db(dic_my_activity_android, case.analysis_db_path)
        #             # print(dic_my_activity_android)



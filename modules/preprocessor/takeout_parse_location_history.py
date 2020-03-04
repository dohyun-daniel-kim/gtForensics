import os
import logging
import json

from modules.utils.takeout_sqlite3 import SQLite3
from tqdm import trange

logger = logging.getLogger('gtForensics')

class LocationHistory(object):
    def parse_logs(dic_location_history, location_logs):
        # print(location_logs.items())
        for k, v in location_logs.items():
            if k == 'timestampMs':
                dic_location_history['timestamp'] = v
            elif k == 'latitudeE7':
                dic_location_history['latitude'] = v
            elif k == 'longitudeE7':
                dic_location_history['longitude'] = v
            elif k == 'accuracy':
                dic_location_history['accuracy'] = v
            elif k == 'altitude':
                dic_location_history['altitude'] = v
            
#---------------------------------------------------------------------------------------------------------------
    def insert_log_info_to_preprocess_db(dic_location_history, preprocess_db_path):
        query = 'INSERT INTO parse_location_history \
                (timestamp, latitude, longitude, altitude, accuracy) \
                VALUES(%d, "%s", "%s", "%s", "%s")' % \
                (int(dic_location_history['timestamp']), dic_location_history['latitude'], dic_location_history['longitude'], \
                dic_location_history['altitude'], dic_location_history['accuracy'])
        SQLite3.execute_commit_query(query, preprocess_db_path)

#---------------------------------------------------------------------------------------------------------------
    def parse_location_history(case):
        file_path = case.takeout_location_history_path
        if os.path.exists(file_path) == False:
            return False

        data = json.load(open(file_path,'r', encoding='utf-8'))
        location_logs = data['locations']
        for i in trange(len(location_logs), desc="[Parsing the Location History Data..................]", unit="epoch"):
            dic_location_history = {'timestamp':"", 'latitude':"", 'longitude':"", 'altitude':"", 'accuracy':""}
            LocationHistory.parse_logs(dic_location_history, location_logs[i])
            LocationHistory.insert_log_info_to_preprocess_db(dic_location_history, case.preprocess_db_path)



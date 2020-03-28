import os
import logging
import json
from modules.utils.takeout_sqlite3 import SQLite3
from tqdm import trange

logger = logging.getLogger('gtForensics')

class SemanticLocationHistory(object):
    def parse_place(dic_semantic_location_history, k, v):
        if k == 'location':
            dic_semantic_location_history['slatitude'] = v['latitudeE7']/10000000
            dic_semantic_location_history['slongitude'] = v['longitudeE7']/10000000
            dic_semantic_location_history['confidence'] = v['locationConfidence']
            for k2, v2 in v.items():
                if k2 == 'address':
                    dic_semantic_location_history['place_addr'] = v2.replace('\n', ' ').replace("\"", "\'")
                elif k2 == 'name':
                    dic_semantic_location_history['place_name'] = v2.replace('\n', ' ').replace("\"", "\'")
                elif k2 == 'sourceInfo':
                    for k3, v3 in v2.items():
                        if k3 == 'deviceTag':
                            dic_semantic_location_history['device_tag'] = v3
        elif k == 'duration':
            dic_semantic_location_history['stimestamp'] = int(v['startTimestampMs'])//1000
            dic_semantic_location_history['etimestamp'] = int(v['endTimestampMs'])//1000
            dic_semantic_location_history['duration'] = dic_semantic_location_history['etimestamp'] - dic_semantic_location_history['stimestamp']
        elif k == 'placeConfidence':
            confidence = dic_semantic_location_history['confidence']
            dic_semantic_location_history['confidence'] = v + '(' + str(confidence) + ')'

#---------------------------------------------------------------------------------------------------------------
    def parse_main_sub_place(case, dic_semantic_location_history, placeVisit_logs):
        for k, v in placeVisit_logs.items():
            if k != 'childVisits':
                dic_semantic_location_history['type'] = 'main_place'
                SemanticLocationHistory.parse_place(dic_semantic_location_history, k, v)
        SemanticLocationHistory.insert_log_info_to_preprocess_db(dic_semantic_location_history, case.preprocess_db_path)

        for k, v in placeVisit_logs.items():
            if k == 'childVisits':
                for placeVisit_log in v:
                    for k2, v2 in placeVisit_log.items():
                        dic_semantic_location_history['type'] = 'sub_place'
                        SemanticLocationHistory.parse_place(dic_semantic_location_history, k2, v2)
                    SemanticLocationHistory.insert_log_info_to_preprocess_db(dic_semantic_location_history, case.preprocess_db_path)

#---------------------------------------------------------------------------------------------------------------
    def parse_activity(case, dic_semantic_location_history, activitySegment_logs):
        dic_semantic_location_history['type'] = 'route'
        for k, v in activitySegment_logs.items():
            if k == 'startLocation':
                dic_semantic_location_history['slatitude'] = v['latitudeE7']/10000000
                dic_semantic_location_history['slongitude'] = v['longitudeE7']/10000000
                for k2, v2 in v.items():
                    if k2 == 'sourceInfo':
                        for k3, v3 in v2.items():
                            if k3 == 'deviceTag':
                                dic_semantic_location_history['device_tag'] = v3
            elif k == 'endLocation':
                dic_semantic_location_history['elatitude'] = v['latitudeE7']/10000000
                dic_semantic_location_history['elongitude'] = v['longitudeE7']/10000000
                for k2, v2 in v.items():
                    if k2 == 'sourceInfo':
                        for k3, v3 in v2.items():
                            if k3 == 'deviceTag':
                                dic_semantic_location_history['device_tag'] = v3
            elif k == 'duration':
                dic_semantic_location_history['stimestamp'] = int(v['startTimestampMs'])//1000
                dic_semantic_location_history['etimestamp'] = int(v['endTimestampMs'])//1000
                dic_semantic_location_history['duration'] = dic_semantic_location_history['etimestamp'] - dic_semantic_location_history['stimestamp']
            elif k == 'distance':
                dic_semantic_location_history['distance'] = v
            elif k == 'activityType':
                dic_semantic_location_history['transportation'] = v
            elif k == 'confidence':
                dic_semantic_location_history['confidence'] = v
            elif k == 'activities':
                if v[0]['activityType'] == dic_semantic_location_history['transportation']:
                    dic_semantic_location_history['confidence'] += '(' + str(v[0]['probability']) + ')'
        SemanticLocationHistory.insert_log_info_to_preprocess_db(dic_semantic_location_history, case.preprocess_db_path)

#---------------------------------------------------------------------------------------------------------------
    def insert_log_info_to_preprocess_db(dic_semantic_location_history, preprocess_db_path):
        query = 'INSERT INTO parse_semantic_location_history \
                (type, stimestamp, slatitude, slongitude, place_name, place_addr, \
                etimestamp, elatitude, elongitude, duration, distance, \
                transportation, confidence, device_tag) \
                VALUES("%s", %d, "%s", "%s", "%s", "%s", %d, "%s", "%s", %d, %d, "%s", "%s", "%s")' % \
                (dic_semantic_location_history['type'], int(dic_semantic_location_history['stimestamp']), dic_semantic_location_history['slatitude'], dic_semantic_location_history['slongitude'], \
                dic_semantic_location_history['place_name'], dic_semantic_location_history['place_addr'], \
                dic_semantic_location_history['etimestamp'], dic_semantic_location_history['elatitude'], dic_semantic_location_history['elongitude'], \
                dic_semantic_location_history['duration'], dic_semantic_location_history['distance'], dic_semantic_location_history['transportation'], dic_semantic_location_history['confidence'],\
                dic_semantic_location_history['device_tag'])
        SQLite3.execute_commit_query(query, preprocess_db_path)

#---------------------------------------------------------------------------------------------------------------
    def parse_activity_place(case):
        file_path = case.takeout_semantic_location_history_path
        if os.path.exists(file_path) == False:
            return False
        
        list_filepath = []
        for dirpath, dirnames, filenames in os.walk(file_path):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                list_filepath.append(filepath)
        if list_filepath == []: return False

        for i in trange(len(list_filepath), desc="[Parsing the Semantic Location History Data.........]", unit="epoch"):
            data = json.load(open(list_filepath[i],'r', encoding='utf-8'))
            location_history_logs = data['timelineObjects']
            # print(list_filepath[i])
            for i in range(len(location_history_logs)):
                dic_semantic_location_history = {'type':"", 'stimestamp':0, 'slatitude':"", 'slongitude':"", 'place_name':"", 'place_addr':"", \
                                            'etimestamp':0, 'elatitude':"", 'elongitude':"", 'duration':0, 'distance':0, \
                                            'transportation':"", 'confidence':"", 'device_tag':""}
                for k, v in location_history_logs[i].items():
                    if k == 'activitySegment':
                        SemanticLocationHistory.parse_activity(case, dic_semantic_location_history, v)
                    elif k == 'placeVisit':
                        SemanticLocationHistory.parse_main_sub_place(case, dic_semantic_location_history, v)

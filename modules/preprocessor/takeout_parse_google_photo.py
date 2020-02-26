import os
import logging
from modules.utils.takeout_sqlite3 import SQLite3
from tqdm import trange
import json

logger = logging.getLogger('gtForensics')

class GooglePhoto(object):
    def parse_filesystem_info(case, dic_google_photo, file_info):
        filename = os.path.basename(file_info)
        album_name = file_info.split(case.takeout_google_photo_path, 1)[1].strip(filename)
        parentpath = 'Google Photos' + album_name
        album_name = album_name.split(os.sep)[1]
        modified_time = int(os.stat(file_info).st_mtime)
        size = os.path.getsize(file_info)
        idx_ext = filename.rfind('.')
        if idx_ext >= 1:
            extension = filename[idx_ext+1:]

        dic_google_photo['filepath'] = file_info
        dic_google_photo['parentpath'] = parentpath
        dic_google_photo['album_name'] = album_name
        dic_google_photo['filename'] = filename
        dic_google_photo['extension'] = extension
        dic_google_photo['bytes'] = size
        dic_google_photo['file_modified_time'] = modified_time

        if GooglePhoto.is_exist_record(dic_google_photo['filepath'], case.preprocess_db_path) == 0:
            GooglePhoto.insert_log_info_to_preprocess_db(dic_google_photo, case.preprocess_db_path)
        else:
            query = 'UPDATE parse_google_photo set \
                    parentpath = "%s", album_name = "%s", filename = "%s", extension = "%s", \
                    bytes = %d, file_modified_time = %d \
                    WHERE filepath = "%s"' % \
                    (dic_google_photo['parentpath'], dic_google_photo['album_name'], dic_google_photo['filename'], dic_google_photo['extension'], \
                    int(dic_google_photo['bytes']), int(dic_google_photo['file_modified_time']), dic_google_photo['filepath'])
            SQLite3.execute_commit_query(query, case.preprocess_db_path)

#---------------------------------------------------------------------------------------------------------------
    def pasrse_google_photo_json(case, dic_google_photo, file_info):
        data = json.load(open(file_info,'r', encoding='utf-8'))
        filepath = file_info.rstrip('.json')
        dic_google_photo['filepath'] = filepath
        if os.path.exists(filepath) == False:
            if filepath[-1] == ')' and filepath[-3] == '(':
                idx_ext = filepath[:-3].rfind('.')
                number = filepath[-3:]
                abnormal_filepath = filepath[:idx_ext] + number + filepath[idx_ext:-3]
                if os.path.exists(abnormal_filepath):
                    dic_google_photo['filepath'] = abnormal_filepath
            elif os.path.exists(filepath + '.MOV'):
                dic_google_photo['filepath'] = filepath + '.MOV'

        for k, v in data.items():
            if k == 'creationTime':
                dic_google_photo['photo_created_time'] = v['timestamp']
            elif k == 'modificationTime':
                dic_google_photo['photo_modified_time'] = v['timestamp']
            elif k == 'photoTakenTime':
                dic_google_photo['photo_taken_time'] = v['timestamp']
            elif k == 'geoData':
                dic_google_photo['latitude'] = v['latitude']
                dic_google_photo['longitude'] = v['longitude']
                dic_google_photo['latitude_span'] = v['latitudeSpan']
                dic_google_photo['longitude_span'] = v['longitudeSpan']
            elif k == 'geoDataExif':
                dic_google_photo['exif_latitude'] = v['latitude']
                dic_google_photo['exif_longitude'] = v['longitude']
                dic_google_photo['exif_latitude_span'] = v['latitudeSpan']
                dic_google_photo['exif_longitude_span'] = v['longitudeSpan']

        if GooglePhoto.is_exist_record(dic_google_photo['filepath'], case.preprocess_db_path) == 0:
            GooglePhoto.insert_log_info_to_preprocess_db(dic_google_photo, case.preprocess_db_path)
        else:
            query = 'UPDATE parse_google_photo set \
                    photo_created_time = %d, photo_modified_time = %d, photo_taken_time = %d, \
                    latitude = "%s", longitude = "%s", latitude_span = "%s", longitude_span = "%s", \
                    exif_latitude = "%s", exif_longitude = "%s", exif_latitude_span = "%s", exif_longitude_span = "%s" \
                    WHERE filepath = "%s"' % \
                    (int(dic_google_photo['photo_created_time']), int(dic_google_photo['photo_modified_time']), int(dic_google_photo['photo_taken_time']), \
                    dic_google_photo['latitude'], dic_google_photo['longitude'], dic_google_photo['latitude_span'], dic_google_photo['longitude_span'], \
                    dic_google_photo['exif_latitude'], dic_google_photo['exif_longitude'], dic_google_photo['exif_latitude_span'], dic_google_photo['exif_longitude_span'], dic_google_photo['filepath'])
            SQLite3.execute_commit_query(query, case.preprocess_db_path)

#---------------------------------------------------------------------------------------------------------------
    def pasrse_google_photo_album_json(case, file_info, list_album_info):
        data = json.load(open(file_info,'r', encoding='utf-8'))
        filename = os.path.basename(file_info)
        album_name = file_info.split(case.takeout_google_photo_path, 1)[1].strip(filename)
        album_name = album_name.split(os.sep)[1]

        dic_album_info = {'album_name':"", "album_created_time":0}
        dic_album_info['album_name'] = album_name
        dic_album_info['album_created_time'] = data['albumData']['date']['timestamp']
        list_album_info.append(dic_album_info)

#---------------------------------------------------------------------------------------------------------------
    def is_exist_record(filepath, preprocess_db_path):
        query = 'SELECT count(*) FROM parse_google_photo WHERE filepath = "%s"' % filepath
        return SQLite3.execute_fetch_query(query, preprocess_db_path)[0]

#---------------------------------------------------------------------------------------------------------------
    def insert_log_info_to_preprocess_db(dic_google_photo, preprocess_db_path):
        query = 'INSERT INTO parse_google_photo \
                (parentpath, album_name, filename, extension, bytes, \
			    album_created_time, photo_taken_time, photo_created_time, photo_modified_time, file_modified_time, \
			    latitude, longitude, latitude_span, longitude_span, \
			    exif_latitude, exif_longitude, exif_latitude_span, exif_longitude_span, filepath) \
                VALUES("%s", "%s", "%s", "%s", %d, %d, %d, %d, %d, %d, "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s")' % \
                (dic_google_photo['parentpath'], dic_google_photo['album_name'], dic_google_photo['filename'], dic_google_photo['extension'], int(dic_google_photo['bytes']),\
                int(dic_google_photo['album_created_time']), int(dic_google_photo['photo_taken_time']), int(dic_google_photo['photo_created_time']), int(dic_google_photo['photo_modified_time']), int(dic_google_photo['file_modified_time']), \
                dic_google_photo['latitude'], dic_google_photo['longitude'], dic_google_photo['latitude_span'], dic_google_photo['longitude_span'], \
                dic_google_photo['exif_latitude'], dic_google_photo['exif_longitude'], dic_google_photo['exif_latitude_span'], dic_google_photo['exif_longitude_span'], dic_google_photo['filepath'])
        SQLite3.execute_commit_query(query, preprocess_db_path)

#---------------------------------------------------------------------------------------------------------------
    def insert_album_info_to_preprocess_db(dic_album_info, preprocess_db_path):
        query = 'UPDATE parse_google_photo set album_created_time = %d WHERE album_name = "%s"' % \
                (int(dic_album_info['album_created_time']), dic_album_info['album_name'])
        SQLite3.execute_commit_query(query, preprocess_db_path)

#---------------------------------------------------------------------------------------------------------------
    def parse_google_photo(case):
        file_path = case.takeout_google_photo_path
        if os.path.exists(file_path) == False:
            return False
        list_filepath = []
        for dirpath, dirnames, filenames in os.walk(file_path):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                list_filepath.append(filepath)
                
        list_album_info = []
        for i in trange(len(list_filepath), desc="[Parsing the Google Photo Data......................]", unit="epoch"):
            # print("..........................................................................")
            dic_google_photo = {'parentpath':"", 'album_name':"", 'filename':"", 'extension':"", 'bytes':0, \
                                'album_created_time':0, 'photo_taken_time':0, 'photo_created_time':0, 'photo_modified_time':0, 'file_modified_time':0, \
                                'latitude':"", 'longitude':"", 'latitude_span':"", 'longitude_span':"", \
                                'exif_latitude':"", 'exif_longitude':"", 'exif_latitude_span':"", 'exif_longitude_span':"", 'filepath':""}
            
            filename = os.path.basename(list_filepath[i])
            if filename == 'shared_album_comments.json':    continue
            idx_ext = filename.rfind('.')
            if idx_ext >= 1:
                extension = filename[idx_ext+1:]

            if filename == 'metadata.json':
                GooglePhoto.pasrse_google_photo_album_json(case, list_filepath[i], list_album_info)
            elif extension == 'json':
                GooglePhoto.pasrse_google_photo_json(case, dic_google_photo, list_filepath[i])
            else:
                GooglePhoto.parse_filesystem_info(case, dic_google_photo, list_filepath[i])

        for i in trange(len(list_album_info), desc="[Parsing the Google Photo Data(Album information)...]", unit="epoch"):
            GooglePhoto.insert_album_info_to_preprocess_db(list_album_info[i], case.preprocess_db_path)
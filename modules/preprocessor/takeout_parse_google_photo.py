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
        extension = 'json'

        dic_google_photo['parentpath'] = parentpath
        dic_google_photo['album_name'] = album_name
        dic_google_photo['filename'] = filename
        dic_google_photo['extension'] = extension
        dic_google_photo['bytes'] = size
        dic_google_photo['real_file_modified_time'] = modified_time

#---------------------------------------------------------------------------------------------------------------
    def pasrse_google_photo_json(dic_google_photo, file_info):
        data = json.load(open(file_info,'r', encoding='utf-8'))

        for k, v in data.items():
            if k == 'title':
                print(v)






        # tmp = data.keys()
        # keylist = []
        # keylist.extend(iter(tmp))
        # print(keylist[0])
        # print(type(tmp))
        # print(data.keys())
        # data['title'][0]
        # data[0]
        # print(data.keys()['title'])
        # print(data['modificationTime'])
        # conversation_logs = data['conversations']
        # print(data)


#---------------------------------------------------------------------------------------------------------------
    def pasrse_google_photo_album_json(dic_google_photo, file_info):
        data = json.load(open(file_info,'r', encoding='utf-8'))
        dic_google_photo['album_created_time'] = data['albumData']['date']['timestamp']

#---------------------------------------------------------------------------------------------------------------
    def insert_log_info_to_preprocess_db(dic_drive, preprocess_db_path):
        query = 'INSERT INTO parse_drive \
                (parentpath, filename, extension, modified_time, bytes, filepath) \
                VALUES("%s", "%s", "%s", %d, %d, "%s")' % \
                (dic_drive['parentpath'], dic_drive['filename'], dic_drive['extension'], dic_drive['modified_time'], dic_drive['bytes'], dic_drive['filepath'])
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
                # if filepath.rsplit('.', 1)[1] == 'json':
                

        for i in trange(len(list_filepath), desc="[Parsing the Google Photo Data......................]", unit="epoch"):
            print("..........................................................................")
            dic_google_photo = {'parentpath':"", 'album_name':"", 'filename':"", 'extension':"", 'bytes':0, \
                                'album_created_time':0, 'photo_taken_time':0, 'file_created_time':0, 'real_file_modified_time':0, 'file_modified_time':0, \
                                'latitude':"", 'longitude':"", 'latitude_span':"", 'longitude_span':"", \
                                'exif_latitude':"", 'exif_longitude':"", 'exif_latitude_span':"", 'exif_longitude_span':"", 'filepath':""}
            
            filename = os.path.basename(list_filepath[i])
            idx_ext = filename.rfind('.')
            if idx_ext >= 1:
                extension = filename[idx_ext+1:]
            
            if filename == 'metadata.json':
                GooglePhoto.pasrse_google_photo_album_json(dic_google_photo, list_filepath[i])
            elif extension == 'json':
                GooglePhoto.pasrse_google_photo_json(dic_google_photo, list_filepath[i])
            else:
                GooglePhoto.parse_filesystem_info(case, dic_google_photo, list_filepath[i])








                    # print(filepath)



            # for filename in filenames:
            # print(filenames)
            # for filename in filenames:
            #     filepath = os.path.join(dirpath, filename)
            #     print(file_path)
                # list_filepath.append(filepath)




        # for i in trange(len(list_filepath), desc="[Parsing the Drive data.............................]", unit="epoch"):
        #         # print("..........................................................................")
        #         dic_drive = {'parentpath':"", 'filename':"", 'extenstion':"", 'modified_time':0, 'bytes':0, 'filepath':""}
        #         Drive.parse_filesystem_info(dic_drive, list_filepath[i])
        #         Drive.insert_log_info_to_preprocess_db(dic_drive, case.preprocess_db_path)
        #         # print(dic_drive)
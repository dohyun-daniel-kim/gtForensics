import os
import logging
from modules.utils.takeout_sqlite3 import SQLite3
from tqdm import trange

logger = logging.getLogger('gtForensics')

class GooglePhoto(object):
    def parse_filesystem_info(dic_drive, file_info):
        filename = os.path.basename(file_info)
        parentpath = file_info.split('Drive' + os.sep, 1)[1].strip(filename)
        idx_ext = filename.rfind('.')
        if idx_ext >= 1:
            extension = filename[idx_ext+1:]
        modified_time = int(os.stat(file_info).st_mtime)
        size = os.path.getsize(file_info)
        
        dic_drive['parentpath'] = 'Drive' + os.sep + str(parentpath)
        dic_drive['filename'] = str(filename)
        dic_drive['extension'] = str(extension)
        dic_drive['modified_time'] = modified_time
        dic_drive['bytes'] = int(size)
        dic_drive['filepath'] = str(file_info)

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
                if filepath.rsplit('.', 1)[1] == 'json':
                    list_filepath.append(filepath)

        for i in trange(len(list_filepath), desc="[Parsing the Google Photo Data......................]", unit="epoch"):
            # print("..........................................................................")
            dic_google_photo = {'parentpath':"", 'album_name':"", 'filename':"", 'extension':"", 'bytes':0, \
                                'album_created_time':0, 'photo_taken_time':0, 'file_created_time':0, 'file_modified_time':0, \
                                'latitude':"", 'longitude':"", 'altitude':"", 'latitude_span':"", 'longitude_span':"", \
                                'exif_latitude':"", 'exif_longitude':"", 'exif_altitude':"", 'exif_latitude_span':"", 'exif_longitude_span':"", 'filepath':""}

            GooglePhoto.parse_filesystem_info(dic_drive, list_filepath[i])
            GooglePhoto.insert_log_info_to_preprocess_db(dic_drive, case.preprocess_db_path)
            # print(dic_drive)





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
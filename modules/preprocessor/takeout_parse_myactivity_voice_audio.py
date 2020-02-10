import os
import logging
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from modules.utils.takeout_html_parser import TakeoutHtmlParser

logger = logging.getLogger('gtForensics')

class MyActivityVoiceAudio(object):
    def parse_voice_audio_log_body_text(dic_my_activity_voice_audio, voice_audio_logs):
        # print('voice logs')
        list_assistant_trained_logs = TakeoutHtmlParser.find_log_body_text(voice_audio_logs)
        if list_assistant_trained_logs != []:
            for content in list_assistant_trained_logs:
                content = str(content).strip()
                if content.startswith('<audio controls'):
                    # print(content)
                    dic_my_activity_voice_audio['attachment_voice_file'] = content.split('>')[2].split('<')[0].lstrip('Audio file: ')
                    # print(dic_my_activity_voice_audio['attachment_voice_file'])

#---------------------------------------------------------------------------------------------------------------
    def parse_voice_audio_log_body(dic_my_activity_voice_audio, voice_audio_logs):
        list_voice_audio_event_logs = TakeoutHtmlParser.find_log_body(voice_audio_logs)
        if list_voice_audio_event_logs != []:
            idx = 0
            for content in list_voice_audio_event_logs:
                # print("----------------------------------------------")
                content = str(content).strip()
                content = content.replace(u'\xa0', ' ')
                # print(content)
                if idx == 0:
                    dic_my_activity_voice_audio['type'] = content
                else:
                    if idx == 1 and dic_my_activity_voice_audio['type'] == 'Said':
                        if content.startswith('<a href="'):
                            idx = content.find('">')
                            dic_my_activity_voice_audio['url'] = content[9:idx]
                            dic_my_activity_voice_audio['keyword'] = content[idx+2:content.find('</a>')]
                    elif content.endswith('UTC'):
                        dic_my_activity_voice_audio['timestamp'] = TakeoutHtmlParser.convert_datetime_to_unixtime(content)
                idx += 1

#---------------------------------------------------------------------------------------------------------------
    def parse_voice_audio_log_title(dic_my_activity_voice_audio, voice_audio_logs):
        list_voice_audio_title_logs = TakeoutHtmlParser.find_log_title(voice_audio_logs)
        if list_voice_audio_title_logs != []:
            for content in list_voice_audio_title_logs:
                content = str(content).strip()
                dic_my_activity_voice_audio['service'] = content.split('>')[1].split('<br')[0]
                # print(dic_my_activity_voice_audio['service'])

#---------------------------------------------------------------------------------------------------------------
    def parse_voice_audio(case):
        file_path = case.takeout_my_activity_voice_audio_path
        # print("my activity assistant")
        # print("file_path: ", file_path)

        with open(file_path, 'r', encoding='utf-8') as f:
            file_contents = f.read()
            soup = BeautifulSoup(file_contents, 'lxml')
            list_voice_audio_logs = TakeoutHtmlParser.find_log(soup)
            if list_voice_audio_logs != []:
                for voice_audio_logs in list_voice_audio_logs:
                    print("..........................................................................")
                    dic_my_activity_voice_audio = {'service':"", 'type':"", 'url':"", 'keyword':"", 'timestamp':"", 'attachment_voice_file':""}
                    MyActivityVoiceAudio.parse_voice_audio_log_title(dic_my_activity_voice_audio, voice_audio_logs)
                    MyActivityVoiceAudio.parse_voice_audio_log_body(dic_my_activity_voice_audio, voice_audio_logs)
                    MyActivityVoiceAudio.parse_voice_audio_log_body_text(dic_my_activity_voice_audio, voice_audio_logs)
                    print(dic_my_activity_voice_audio)




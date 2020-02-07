import logging
from bs4 import BeautifulSoup

logger = logging.getLogger('gtForensics')

class TakeoutHtmlParser(object):
    def find_log(soup):
        return soup.find_all('div', class_ ={"outer-cell mdl-cell mdl-cell--12-col mdl-shadow--2dp"})

    def find_log_body(logs):
        return logs.find('div', class_ ={"content-cell mdl-cell mdl-cell--6-col mdl-typography--body-1"})

    def find_log_body_text(logs):
        return logs.find('div', class_ ={"content-cell mdl-cell mdl-cell--6-col mdl-typography--body-1 mdl-typography--text-right"})

    def find_log_caption(logs):
        return logs.find('div', class_ ={"content-cell mdl-cell mdl-cell--12-col mdl-typography--caption"})



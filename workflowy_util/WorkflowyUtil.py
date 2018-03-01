"""
WorkflowyUtil.py
~~~~~~~~~~~~~~~~
this utility is used to login to workflowy and get all the items.

"""
import json
import requests


class WorkflowyUtil(object):

    WORKFLOWY_URL = 'https://workflowy.com/get_initialization_data?client_version=18'
    WORKFLOWY_LOGIN_URL = 'https://workflowy.com/accounts/login/'
    HEADERS = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.8,en;q=0.6',
        'cache-control': 'max-age=0',
        'content-type': 'application/x-www-form-urlencoded',
        'dnt': '1',
        'origin': 'https://workflowy.com',
        'referer': 'https://workflowy.com/accounts/login/',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/60.0.3112.113 Safari/537.36'}

    def __init__(self, username, password):
        self.workflowy_username = username
        self.workflowy_password = password
        self.session = None
        self.login_in_workflowy()

    def login_in_workflowy(self):
        print('login to workflowy...')
        if not self.session:
            self.session = requests.Session()
        self.session.post(self.WORKFLOWY_LOGIN_URL,
                          data={'username': self.workflowy_username,
                                'password': self.workflowy_password,
                                'next': ''})
        return True

    def get_outline(self):
        print('start to get the outline...')
        outlines_json = self.session.get(self.WORKFLOWY_URL).text
        outlines_dict = json.loads(outlines_json)
        project_list = outlines_dict.get('projectTreeData', {}) \
            .get('mainProjectTreeInfo', {}) \
            .get('rootProjectChildren', [])
        return project_list

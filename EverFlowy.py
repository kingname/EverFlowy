import json
from json.decoder import JSONDecodeError
import requests
from evernote.api.client import EvernoteClient
from evernote.edam.type import ttypes as Types
from xml.etree import ElementTree as ET
from xml.dom.minidom import parseString


class EverFlowy(object):
    def __init__(self):
        self.workflowy_url = 'https://workflowy.com/get_initialization_data?client_version=18'
        self.workflowy_login_url = 'https://workflowy.com/accounts/login/'
        self.headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.8,en;q=0.6',
            'cache-control': 'max-age=0',
            'content-type': 'application/x-www-form-urlencoded',
            'dnt': '1',
            'origin': 'https://workflowy.com',
            'referer': 'https://workflowy.com/accounts/login/',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}
        self.workflowy_username = ''
        self.workflowy_password = ''
        self.dev_token = ''
        self.template = ''
        self.session = None
        self.read_config()

    def read_config(self):
        with open('config.json', encoding='utf-8') as f:
            config = f.read()
            try:
                config_dict = json.loads(config)
            except JSONDecodeError:
                print('Config is invalid.')
                return

        workflowy_config = config_dict.get('Workflowy', {})
        self.workflowy_username = workflowy_config.get('username', '')
        self.workflowy_password = workflowy_config.get('password', '')

        self.template = config_dict.get('Content_template', '')
        self.dev_token = config_dict.get('dev_token', '')

    def login_in_workflowy(self):
        print('login to workflowy...')
        if not self.session:
            self.session = requests.Session()
        self.session.post(self.workflowy_login_url,
                          data={'username': self.workflowy_username,
                                'password': self.workflowy_password,
                                'next': ''})
        return True

    def get_outline(self):
        print('start to get the outline...')
        outlines_json = self.session.get(self.workflowy_url).text
        outlines_dict = json.loads(outlines_json)
        project_list = outlines_dict.get('projectTreeData', {})\
            .get('mainProjectTreeInfo', {})\
            .get('rootProjectChildren', [])
        return project_list

    def sync_project(self):
        print('start to construct body...')
        project_list = self.get_outline()
        item_list = self.construct_body(project_list)
        print('sync project to evernote.')
        self.write_to_evernote(item_list)

    def construct_body(self, project_list):
        item_list = []
        for project in project_list:
            title = project['nm']
            detail = project.get('ch', [])
            item_list.append({'title': title, 'body': self.generate_body(detail)})
        return item_list

    def generate_body(self, detail):
        ul = ET.Element('ul')
        for item in detail:
            name = item['nm']
            ch = item.get('ch', [])
            li = ET.Element('li')
            li.text = name
            if ch:
                li.append(self.generate_body(ch))
            ul.append(li)
        return ul

    def write_to_evernote(self, item_list):
        client = EvernoteClient(token=self.dev_token)
        client.get_access_token()
        note_store = client.get_note_store()
        for item in item_list:
            body = ET.tostring(item['body']).decode()
            pretty_body = parseString(body).toprettyxml(indent='    ')
            note = Types.Note()
            note.title = item['title']
            note.content = self.template.format(body='\n'.join(pretty_body.split('\n')[1:]))
            note_store.createNote(note)
            print(item['title'])

if __name__ == '__main__':
    ever_flowy = EverFlowy()
    ever_flowy.login_in_workflowy()
    ever_flowy.sync_project()

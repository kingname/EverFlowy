"""
Everflowy.py
~~~~~~~~~~~~

Everflowy is a tools to sync items from workflowy to Evernote.

And This is the entrance of this tool.
"""
import json
from sql_util.SqlUtil import SqlUtil
from evernote_util.EverNoteUtil import EverNoteUtil
from json.decoder import JSONDecodeError
from workflowy_util.WorkflowyUtil import WorkflowyUtil


class EverFlowy(object):
    def __init__(self):
        self.workflowy_username = ''
        self.workflowy_password = ''
        self.dev_token = ''
        self.template = ''
        self.read_config()
        self.workflowy = WorkflowyUtil(self.workflowy_username, self.workflowy_password)
        self.evernote = EverNoteUtil(self.dev_token, self.template)
        self.sql_util = SqlUtil('history.db')

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

    def sync_project(self):
        print('start to construct body...')
        project_list = self.workflowy.get_outline()
        item_list = self.evernote.construct_body(project_list)
        self.sql_util.insert_history(item_list)
        print('sync project to evernote.')
        self.evernote.write_to_evernote(item_list)


if __name__ == '__main__':
    ever_flowy = EverFlowy()
    ever_flowy.sync_project()

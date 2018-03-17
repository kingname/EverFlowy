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
        self.sql_util = SqlUtil('history_product.db')

    def read_config(self):
        with open('config_dev.json', encoding='utf-8') as f:
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
        item_to_update = self.filter_item_to_update(item_list)
        if not item_to_update:
            print('all item are up-to-date.')
            return
        print('sync project to evernote.')
        self.evernote.write_to_evernote(item_to_update)
        self.sql_util.insert_many_history(item_to_update)

    def filter_item_to_update(self, item_list):
        update_queue = []
        for item in item_list:
            workflowy_id = item['id']
            exists_item = self.sql_util.query_by_workflowy_id(workflowy_id)
            if not exists_item:
                update_queue.append(item)
                continue

            old_enml = exists_item['detail_json']
            if old_enml != item['detail_json']:
                item['evernote_id'] = exists_item['evernote_id']
                update_queue.append(item)
        return update_queue


if __name__ == '__main__':
    ever_flowy = EverFlowy()
    ever_flowy.sync_project()

import sqlite3
import datetime


class SqlUtil(object):
    def __init__(self, db_path):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self.prepare()

    def prepare(self):
        self.conn.execute('CREATE TABLE IF NOT EXISTS history '
                          '(id integer PRIMARY KEY,'
                          'workflowy_id text,'
                          'evernote_id varchar(64),'
                          'workflowy_item_json text,'
                          'item_enml text,'
                          'create_time varchar(20))')
        self.conn.commit()

    def insert_history(self, history):
        self.conn.execute('insert into history values (null, ?, ?, ?, ?, ?)',
                          (history['workflowy_id'],
                           history['evernote_id'],
                           history['workflowy_item_json'],
                           history['item_enml'],
                           datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        self.conn.commit()

    def insert_many_history(self, history_list):
        parameter_list = [(history['id'],
                           history['evernote_id'],
                           history['detail_json'],
                           history['body'],
                           datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')) for history in history_list]
        self.conn.executemany('insert into history values (null, ?, ?, ?, ?, ?)', parameter_list)
        self.conn.commit()

    def query_by_workflowy_id(self, workflowy_id):
        result_generator = self.conn.execute('select * from history where workflowy_id=? ORDER BY id limit 1', (workflowy_id, ))
        for row in result_generator:
            return {'evernote_id': row['evernote_id'], 'detail_json': row['workflowy_item_json']}
        return None

    def close(self):
        self.conn.close()


if __name__ == '__main__':
    util = SqlUtil('test4.db')
    util.prepare()
    util.insert_history({'workflowy_id': 'abc',
                         'evernote_id': 'bbb',
                         'workflowy_item_json': 'ccc',
                         'item_enml': 'ddd'})
    print(util.query_by_workflowy_id('abc'))

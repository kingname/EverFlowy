import sqlite3


class SqlUtil(object):
    def __init__(self, db_path):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row

    def prepare(self):
        cursor = self.conn.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS history '
                       '(id integer PRIMARY KEY,'
                       'workflowy_id text,'
                       'evernote_id varchar(64),'
                       'workflowy_item_json text,'
                       'item_enml text)')
        self.conn.commit()

    def insert_history(self, history):
        cursor = self.conn.cursor()
        cursor.execute('insert into history values (null, ?, ?, ?, ?)', (history['workflowy_id'],
                                                                         history['evernote_id'],
                                                                         history['workflowy_item_json'],
                                                                         history['item_enml']))
        self.conn.commit()
        cursor.close()

    def query_by_workflowy_id(self, workflowy_id):
        cursor = self.conn.cursor()
        cursor.execute('select * from history where workflowy_id=?', (workflowy_id, ))
        row = cursor.fetchone()
        if row:
            return {'evernote_id': row['evernote_id'], 'item_enml': row['item_enml']}
        return None


if __name__ == '__main__':
    util = SqlUtil('test3.db')
    util.prepare()
    util.insert_history({'workflowy_id': 'abc',
                         'evernote_id': 'bbb',
                         'workflowy_item_json': 'ccc',
                         'item_enml': 'ddd'})
    print(util.query_by_workflowy_id('abc'))
from xml.etree import ElementTree as ET
from xml.dom.minidom import parseString
from evernote.api.client import EvernoteClient
from evernote.edam.type import ttypes as Types


class EverNoteUtil(object):
    def __init__(self, dev_token, template):
        self.dev_token = dev_token
        self.template = template

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
